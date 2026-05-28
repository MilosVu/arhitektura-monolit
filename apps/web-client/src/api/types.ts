export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  ad_username: string;
}

export interface CaseSummary {
  id: number;
  case_number: string;
  title: string;
  description: string | null;
  document_count: number;
  last_synced_at: string | null;
  created_at: string;
}

export interface CaseDetail {
  id: number;
  case_number: string;
  title: string;
  description: string | null;
  owner: User;
  last_synced_at: string | null;
  created_at: string;
}

export interface DocumentSummary {
  id: number;
  case_id: number;
  filename: string;
  mime_type: string;
  status: string;
  page_count: number | null;
  created_at: string;
  updated_at: string;
}

export interface SyncJob {
  id: string;
  case_id: number;
  status: string;
  progress: number;
  total_documents: number;
  message: string | null;
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  role: string;
  content: string;
  timestamp?: string;
}

export interface AuditLog {
  id: number;
  user_id: number | null;
  action: string;
  resource_type: string;
  resource_id: string;
  details: string | null;
  created_at: string;
}

export interface TranslateResponse {
  document_id: number;
  source_lang: string;
  target_lang: string;
  translated_text: string;
}

export interface RagChunk {
  document_id: number;
  filename: string;
  content: string;
  score: number;
}

export interface RagSearchResponse {
  query: string;
  chunks: RagChunk[];
}

export interface LawNode {
  ref: string;
  title: string;
  article: string;
  content: string;
  valid_from: string;
  valid_to: string | null;
}

export interface ComponentStatus {
  name: string;
  status: string;
  latency_ms: number | null;
  detail: string | null;
}

export interface SystemStatus {
  overall: string;
  components: ComponentStatus[];
  checked_at: string;
}
