"""Baseline šema — usklađena sa infra/postgres/init.sql (bez seed podataka)."""

from typing import Sequence, Union

from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL,
            ad_username VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    op.execute("""
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
    """)
    op.execute("""
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
    """)
    op.execute("""
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
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            action VARCHAR(100) NOT NULL,
            resource_type VARCHAR(100) NOT NULL,
            resource_id VARCHAR(100) NOT NULL,
            details TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS audit_logs CASCADE;")
    op.execute("DROP TABLE IF EXISTS sync_jobs CASCADE;")
    op.execute("DROP TABLE IF EXISTS documents CASCADE;")
    op.execute("DROP TABLE IF EXISTS cases CASCADE;")
    op.execute("DROP TABLE IF EXISTS users CASCADE;")
