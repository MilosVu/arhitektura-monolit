"""OCR adapter stub."""

from cortex_core.ports.ocr import ExtractionResult, ExtractedPage, OCRPort


class StubOCRAdapter(OCRPort):
    async def extract_text(self, filename: str, content: bytes) -> ExtractionResult:
        _ = content
        text = f"[Mock OCR from {filename}] Die Parteien vereinbaren..."
        return ExtractionResult(
            filename=filename,
            pages=[ExtractedPage(page_number=1, text=text, confidence=0.95)],
            plain_text=text,
        )

    async def chunk(self, plain_text: str, *, max_tokens: int = 512) -> list[str]:
        _ = max_tokens
        return [plain_text[i : i + 120] for i in range(0, len(plain_text), 120)] or [plain_text]
