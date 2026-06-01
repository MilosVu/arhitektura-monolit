import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import AppLayout from "./components/AppLayout";
import { AuthProvider } from "./context/AuthContext";
import AuditLogPage from "./pages/AuditLogPage";
import CaseDetailPage from "./pages/CaseDetailPage";
import CasesListPage from "./pages/CasesListPage";
import ChatPage from "./pages/ChatPage";
import DocumentViewPage from "./pages/DocumentViewPage";
import LawsPage from "./pages/LawsPage";
import AuthCallbackPage from "./pages/AuthCallbackPage";
import LoginPage from "./pages/LoginPage";
import SearchPage from "./pages/SearchPage";
import SyncStatusPage from "./pages/SyncStatusPage";
import SystemStatusPage from "./pages/SystemStatusPage";
import TranslatePage from "./pages/TranslatePage";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/auth/callback" element={<AuthCallbackPage />} />
          <Route element={<AppLayout />}>
            <Route path="/" element={<Navigate to="/cases" replace />} />
            <Route path="/cases" element={<CasesListPage />} />
            <Route path="/cases/:caseId" element={<CaseDetailPage />} />
            <Route path="/cases/:caseId/documents/:documentId" element={<DocumentViewPage />} />
            <Route
              path="/cases/:caseId/documents/:documentId/translate"
              element={<TranslatePage />}
            />
            <Route path="/cases/:caseId/chat" element={<ChatPage />} />
            <Route path="/cases/:caseId/chat/:threadId" element={<ChatPage />} />
            <Route path="/cases/:caseId/search" element={<SearchPage />} />
            <Route path="/sync/:jobId" element={<SyncStatusPage />} />
            <Route path="/laws" element={<LawsPage />} />
            <Route path="/system" element={<SystemStatusPage />} />
            <Route path="/audit" element={<AuditLogPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
