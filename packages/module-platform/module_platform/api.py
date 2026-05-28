"""Public facade for the platform domain module."""

from datetime import UTC, datetime, timedelta
import uuid

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from cortex_core.domain.exceptions import ForbiddenError
from cortex_core.enums import SyncJobStatus
from module_platform.models import AuditLog, Case, Document, SyncJob, User
from module_platform.infrastructure.chat_store import append_message, get_messages, get_thread, save_thread
from module_platform.schemas import (
    AuditLogResponse,
    CaseDetail,
    CaseSummary,
    ChatHistoryResponse,
    ChatMessage,
    ChatThreadResponse,
    DocumentDetail,
    DocumentSummary,
    LoginRequest,
    LoginResponse,
    SyncJobCreateResponse,
    SyncJobResponse,
    SystemStatusResponse,
    UserResponse,
)
from module_ai.schemas import (
    LawNodeResponse,
    RagSearchRequest,
    RagSearchResponse,
    TranslateRequest,
    TranslateResponse,
)
from cortex_core.settings import get_settings

from module_ai.api import AiModule
from module_platform.services.case_service import CaseService
from module_platform.services.sync_service import SyncService
from module_platform.system import get_system_status

settings = get_settings()


class PlatformModule:
    """In-process facade for auth, cases, documents, sync, audit, and AI route delegation."""

    def __init__(self, ai_module: AiModule | None = None) -> None:
        self._ai = ai_module or AiModule()

    @property
    def ai(self) -> AiModule:
        return self._ai

    async def get_system_status(self) -> SystemStatusResponse:
        return await get_system_status(self._ai)

    def login(self, body: LoginRequest, db: Session) -> LoginResponse:
        user = db.query(User).filter(User.ad_username == body.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        expire = datetime.now(UTC) + timedelta(hours=8)
        token = jwt.encode(
            {"sub": str(user.id), "role": user.role, "exp": expire},
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

        audit = AuditLog(
            user_id=user.id,
            action="login",
            resource_type="user",
            resource_id=str(user.id),
            details=f"Mock login for {user.ad_username}",
        )
        db.add(audit)
        db.commit()

        return LoginResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    def list_cases(self, user: User, db: Session) -> list[CaseSummary]:
        return CaseService(db).list_for_user(user)

    def get_case(self, case_id: int, user: User, db: Session) -> CaseDetail:
        try:
            return CaseService(db).get_detail(case_id, user)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

    def list_documents(self, case_id: int, user: User, db: Session) -> list[DocumentSummary]:
        try:
            CaseService(db).assert_case_access(case_id, user)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

        docs = db.query(Document).filter(Document.case_id == case_id).order_by(Document.created_at.desc()).all()
        return [DocumentSummary.model_validate(d) for d in docs]

    def get_document(self, document_id: int, user: User, db: Session) -> DocumentDetail:
        doc = (
            db.query(Document)
            .join(Case)
            .filter(Document.id == document_id, Case.owner_id == user.id)
            .first()
        )
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        return DocumentDetail.model_validate(doc)

    def trigger_sync(self, case_id: int, user: User, db: Session) -> SyncJobCreateResponse:
        try:
            case = CaseService(db).assert_case_access(case_id, user)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

        job = SyncService(db).trigger_sync(case, user)
        return SyncJobCreateResponse(job_id=job.id)

    def get_sync_job(self, job_id: str, user: User, db: Session) -> SyncJobResponse:
        job = SyncService(db).get_job_for_user(job_id, user)
        if not job:
            raise HTTPException(status_code=404, detail="Sync job not found")
        return SyncJobResponse.model_validate(job)

    def create_chat_thread(self, case_id: int, user: User, db: Session) -> ChatThreadResponse:
        try:
            CaseService(db).assert_case_access(case_id, user)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

        thread_id = str(uuid.uuid4())
        save_thread(thread_id, case_id, user.id)
        append_message(
            thread_id,
            "assistant",
            "Willkommen bei Cortex AI. Wie kann ich Ihnen bei diesem Fall helfen?",
        )

        return ChatThreadResponse(
            thread_id=thread_id,
            case_id=case_id,
            created_at=datetime.now(UTC),
        )

    def get_chat_history(self, thread_id: str, user: User) -> ChatHistoryResponse:
        thread = get_thread(thread_id)
        if thread and thread.get("user_id") != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        messages = get_messages(thread_id)
        if not messages:
            messages = [
                ChatMessage(
                    role="assistant",
                    content="Willkommen bei Cortex AI. Wie kann ich Ihnen bei diesem Fall helfen?",
                    timestamp=datetime.now(UTC),
                )
            ]

        return ChatHistoryResponse(thread_id=thread_id, messages=messages)

    async def send_chat_message(self, thread_id: str, message: str, case_id: int, user: User):
        thread = get_thread(thread_id)
        if thread and thread.get("user_id") != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        append_message(thread_id, "user", message)
        return await self._ai.stream_chat(message, thread_id, case_id)

    def save_assistant_message(self, thread_id: str, content: str, user: User) -> dict:
        thread = get_thread(thread_id)
        if thread and thread.get("user_id") != user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        append_message(thread_id, "assistant", content)
        return {"status": "saved"}

    def search_case_documents(
        self, case_id: int, body: RagSearchRequest, user: User, db: Session
    ) -> RagSearchResponse:
        try:
            CaseService(db).assert_case_access(case_id, user)
        except ForbiddenError:
            raise HTTPException(status_code=404, detail="Case not found") from None

        return self._ai.rag_search(body.query, case_id, body.limit)

    def lookup_law(self, law_ref: str) -> LawNodeResponse:
        return self._ai.lookup_law(law_ref)

    def translate_document(
        self, document_id: int, body: TranslateRequest, user: User, db: Session
    ) -> TranslateResponse:
        doc = (
            db.query(Document)
            .join(Case)
            .filter(Document.id == document_id, Case.owner_id == user.id)
            .first()
        )
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        mock_text = f"[Mock extracted text from {doc.filename}] Die Parteien vereinbaren hiermit..."
        return self._ai.translate(
            document_id=document_id,
            text=mock_text,
            source_lang=body.source_lang,
            target_lang=body.target_lang,
        )

    def list_audit_logs(self, user: User, db: Session, limit: int = 50) -> list[AuditLogResponse]:
        logs = (
            db.query(AuditLog)
            .filter(AuditLog.user_id == user.id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )
        return [AuditLogResponse.model_validate(log) for log in logs]
