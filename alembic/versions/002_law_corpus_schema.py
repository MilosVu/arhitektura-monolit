"""Law corpus tables — ADR 0009."""

from typing import Sequence, Union

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS law_codes (
            id SERIAL PRIMARY KEY,
            code VARCHAR(50) NOT NULL,
            title VARCHAR(500) NOT NULL,
            jurisdiction VARCHAR(20) NOT NULL,
            canton_code VARCHAR(10),
            official_uri VARCHAR(500),
            created_at TIMESTAMPTZ DEFAULT NOW(),
            CONSTRAINT uq_law_codes_scope UNIQUE (code, jurisdiction, canton_code)
        );
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS law_provisions (
            id SERIAL PRIMARY KEY,
            law_code_id INTEGER NOT NULL REFERENCES law_codes(id),
            ref VARCHAR(100) NOT NULL,
            article_number VARCHAR(50),
            title VARCHAR(500),
            CONSTRAINT uq_law_provisions_ref UNIQUE (law_code_id, ref)
        );
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS law_sync_jobs (
            id VARCHAR(36) PRIMARY KEY,
            scope VARCHAR(100) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            progress INTEGER DEFAULT 0,
            message TEXT,
            stats_json TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            finished_at TIMESTAMPTZ
        );
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS law_versions (
            id SERIAL PRIMARY KEY,
            provision_id INTEGER NOT NULL REFERENCES law_provisions(id),
            valid_from DATE NOT NULL,
            valid_to DATE,
            source VARCHAR(50) NOT NULL,
            source_version_id VARCHAR(255),
            content_checksum VARCHAR(64) NOT NULL,
            blob_path VARCHAR(500),
            content TEXT,
            law_sync_job_id VARCHAR(36) REFERENCES law_sync_jobs(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS law_versions CASCADE;")
    op.execute("DROP TABLE IF EXISTS law_sync_jobs CASCADE;")
    op.execute("DROP TABLE IF EXISTS law_provisions CASCADE;")
    op.execute("DROP TABLE IF EXISTS law_codes CASCADE;")
