-- Cortex AI mockup seed data

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    ad_username VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cases (
    id SERIAL PRIMARY KEY,
    case_number VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    alfresco_folder_id VARCHAR(255),
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES cases(id),
    filename VARCHAR(500) NOT NULL,
    mime_type VARCHAR(100) DEFAULT 'application/pdf',
    status VARCHAR(50) DEFAULT 'pending',
    alfresco_node_id VARCHAR(255),
    page_count INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sync_jobs (
    id VARCHAR(36) PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES cases(id),
    status VARCHAR(50) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    total_documents INTEGER DEFAULT 0,
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(100) NOT NULL,
    details TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Seed users
INSERT INTO users (email, full_name, role, ad_username) VALUES
    ('judge.mueller@gericht.bs.ch', 'Dr. Hans Müller', 'judge', 'hmueller'),
    ('clerk.weber@gericht.bs.ch', 'Anna Weber', 'clerk', 'aweber');

-- Seed cases (role-based ownership)
INSERT INTO cases (case_number, title, description, owner_id, alfresco_folder_id, last_synced_at) VALUES
    ('BS-2024-00142', 'Handelsstreit ABC GmbH vs. XYZ AG', 'Zivilrechtlicher Handelsstreit betreffend Vertragsbruch.', 1, 'alfresco-folder-001', NOW() - INTERVAL '2 days'),
    ('BS-2024-00287', 'Strafverfahren Schmidt', 'Betrugsverfahren gemäss StGB Art. 146.', 2, 'alfresco-folder-002', NOW() - INTERVAL '5 days'),
    ('BS-2024-00301', 'Verwaltungsstreit Weber', 'Beschwerde betreffend Baubewilligung.', 2, 'alfresco-folder-003', NOW() - INTERVAL '1 day');

-- Seed documents
INSERT INTO documents (case_id, filename, mime_type, status, alfresco_node_id, page_count) VALUES
    (1, 'Klageerwiderung.pdf', 'application/pdf', 'ready', 'alfresco-doc-001', 24),
    (1, 'Vertragsentwurf_2023.pdf', 'application/pdf', 'ready', 'alfresco-doc-002', 8),
    (1, 'Beweismittel_A.pdf', 'application/pdf', 'pending', 'alfresco-doc-003', NULL),
    (2, 'Anklageschrift.pdf', 'application/pdf', 'ready', 'alfresco-doc-004', 12),
    (2, 'Polizeibericht.pdf', 'application/pdf', 'ready', 'alfresco-doc-005', 45),
    (3, 'Baugesuch.pdf', 'application/pdf', 'pending', 'alfresco-doc-006', NULL);

-- Seed audit logs
INSERT INTO audit_logs (user_id, action, resource_type, resource_id, details) VALUES
    (1, 'view_case', 'case', '1', 'Viewed case BS-2024-00142'),
    (1, 'view_document', 'document', '1', 'Opened Klageerwiderung.pdf'),
    (1, 'start_sync', 'case', '1', 'Triggered Alfresco sync'),
    (2, 'view_case', 'case', '2', 'Viewed case BS-2024-00287'),
    (1, 'chat_message', 'thread', 'mock-thread-001', 'Asked about contract clause 3.2');
