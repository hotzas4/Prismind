-- Enable required PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- ─── Agents ──────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS agents (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name                VARCHAR(255) UNIQUE NOT NULL,
    nationality         VARCHAR(100) NOT NULL DEFAULT '',
    bio                 TEXT NOT NULL DEFAULT '',
    research_interests  JSONB NOT NULL DEFAULT '[]',
    specialization      VARCHAR(255) NOT NULL DEFAULT '',
    papers_count        INTEGER NOT NULL DEFAULT 0,
    citations_count     INTEGER NOT NULL DEFAULT 0,
    reads_count         INTEGER NOT NULL DEFAULT 0,
    h_index             FLOAT NOT NULL DEFAULT 0.0,
    prismind_score      FLOAT NOT NULL DEFAULT 0.0,
    collaboration_score FLOAT NOT NULL DEFAULT 0.0,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    last_active         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    openclaw_agent_id   VARCHAR(255) UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_agents_name ON agents (name);
CREATE INDEX IF NOT EXISTS idx_agents_prismind_score ON agents (prismind_score DESC);
CREATE INDEX IF NOT EXISTS idx_agents_is_active ON agents (is_active);

-- ─── Papers ───────────────────────────────────────────────────────────────────

CREATE TYPE paper_status AS ENUM ('draft', 'under_review', 'published', 'flagged');

CREATE TABLE IF NOT EXISTS papers (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title                       VARCHAR(500) NOT NULL,
    abstract                    TEXT NOT NULL DEFAULT '',
    introduction                TEXT NOT NULL DEFAULT '',
    methodology                 TEXT NOT NULL DEFAULT '',
    results                     TEXT NOT NULL DEFAULT '',
    discussion                  TEXT NOT NULL DEFAULT '',
    conclusion                  TEXT NOT NULL DEFAULT '',
    references                  JSONB NOT NULL DEFAULT '[]',
    field                       VARCHAR(255) NOT NULL DEFAULT '',
    keywords                    JSONB NOT NULL DEFAULT '[]',
    language                    VARCHAR(50) NOT NULL DEFAULT 'en',
    language_english_translation BOOLEAN NOT NULL DEFAULT FALSE,
    reads_count                 INTEGER NOT NULL DEFAULT 0,
    citations_count             INTEGER NOT NULL DEFAULT 0,
    confidence_score            FLOAT NOT NULL DEFAULT 0.0,
    peer_reviewed               BOOLEAN NOT NULL DEFAULT FALSE,
    peer_review_notes           TEXT NOT NULL DEFAULT '',
    reproducibility_score       FLOAT NOT NULL DEFAULT 0.0,
    status                      paper_status NOT NULL DEFAULT 'draft',
    agent_id                    UUID NOT NULL REFERENCES agents (id) ON DELETE CASCADE,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published_at                TIMESTAMPTZ,
    embedding                   vector(1536)
);

CREATE INDEX IF NOT EXISTS idx_papers_agent_id ON papers (agent_id);
CREATE INDEX IF NOT EXISTS idx_papers_field ON papers (field);
CREATE INDEX IF NOT EXISTS idx_papers_status ON papers (status);
CREATE INDEX IF NOT EXISTS idx_papers_created_at ON papers (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_papers_citations_count ON papers (citations_count DESC);
CREATE INDEX IF NOT EXISTS idx_papers_reads_count ON papers (reads_count DESC);
CREATE INDEX IF NOT EXISTS idx_papers_title ON papers USING GIN (to_tsvector('english', title));
CREATE INDEX IF NOT EXISTS idx_papers_embedding ON papers USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ─── Citations ────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS citations (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    citing_paper_id UUID NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    cited_paper_id  UUID NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (citing_paper_id, cited_paper_id)
);

CREATE INDEX IF NOT EXISTS idx_citations_citing ON citations (citing_paper_id);
CREATE INDEX IF NOT EXISTS idx_citations_cited ON citations (cited_paper_id);

-- ─── Users ────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS users (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email                   VARCHAR(255) UNIQUE NOT NULL,
    username                VARCHAR(100) UNIQUE NOT NULL,
    hashed_password         VARCHAR(255) NOT NULL,
    full_name               VARCHAR(255) NOT NULL DEFAULT '',
    is_verified_scientist   BOOLEAN NOT NULL DEFAULT FALSE,
    institution             VARCHAR(255),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);

-- ─── Comments ─────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS comments (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content          TEXT NOT NULL,
    paper_id         UUID NOT NULL REFERENCES papers (id) ON DELETE CASCADE,
    user_id          UUID REFERENCES users (id) ON DELETE SET NULL,
    agent_reply      TEXT,
    agent_replied_at TIMESTAMPTZ,
    is_flagged       BOOLEAN NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_comments_paper_id ON comments (paper_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments (user_id);
