-- ============================================================================
-- Migration: 001_initial_civic_schema.sql
-- Description: Civic Ingestion, Verification, and NGO Mobilization Pipeline Schema
-- Engine: PostgreSQL 15+ / Supabase with pgvector
-- ============================================================================

-- 1. Enable Required PostgreSQL Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 2. Create civic_issues Table (Parent issue cluster)
CREATE TABLE IF NOT EXISTS civic_issues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (
        category IN ('Sanitation', 'Roads & Transit', 'Waterlogging', 'Public Safety', 'Environment')
    ),
    ward VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'Medium' CHECK (
        severity IN ('Low', 'Medium', 'High', 'Critical')
    ),
    authenticity_score INT NOT NULL DEFAULT 50 CHECK (
        authenticity_score >= 0 AND authenticity_score <= 100
    ),
    verification_reasoning TEXT,
    responsible_authority TEXT NOT NULL,
    source_count INT NOT NULL DEFAULT 1 CHECK (source_count >= 1),
    embedding VECTOR(768),
    status VARCHAR(30) NOT NULL DEFAULT 'flagged_unverified' CHECK (
        status IN ('flagged_unverified', 'verified_pending_ngo', 'event_active', 'resolved')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Create civic_sources Table (Raw signal ingestion items)
CREATE TABLE IF NOT EXISTS civic_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    issue_id UUID REFERENCES civic_issues(id) ON DELETE SET NULL,
    source_type VARCHAR(30) NOT NULL CHECK (
        source_type IN ('twitter', 'news', 'resident_complaint', 'municipal_notice')
    ),
    source_url TEXT,
    raw_content TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'raw' CHECK (
        status IN ('raw', 'processed', 'clustered')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Create ngos Table (Registered civic action partners)
CREATE TABLE IF NOT EXISTS ngos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    primary_causes TEXT[] NOT NULL DEFAULT '{}',
    operating_wards TEXT[] NOT NULL DEFAULT '{}',
    contact_email TEXT NOT NULL UNIQUE,
    is_verified BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Create ngo_volunteer_events Table (Mobilization drafts & live actions)
CREATE TABLE IF NOT EXISTS ngo_volunteer_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    issue_id UUID NOT NULL REFERENCES civic_issues(id) ON DELETE CASCADE,
    ngo_id UUID NOT NULL REFERENCES ngos(id) ON DELETE CASCADE,
    event_title TEXT NOT NULL,
    event_date DATE NOT NULL,
    meeting_point TEXT NOT NULL,
    target_volunteers INT NOT NULL CHECK (target_volunteers > 0),
    registered_volunteers INT NOT NULL DEFAULT 0 CHECK (registered_volunteers >= 0),
    required_gear JSONB NOT NULL DEFAULT '[]'::jsonb,
    tasks_breakdown JSONB NOT NULL DEFAULT '[]'::jsonb,
    safety_guidelines JSONB NOT NULL DEFAULT '[]'::jsonb,
    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (
        status IN ('draft', 'published', 'completed')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Indexes for High-Performance Queries
CREATE INDEX IF NOT EXISTS idx_civic_issues_ward ON civic_issues(ward);
CREATE INDEX IF NOT EXISTS idx_civic_issues_category ON civic_issues(category);
CREATE INDEX IF NOT EXISTS idx_civic_issues_status ON civic_issues(status);
CREATE INDEX IF NOT EXISTS idx_civic_issues_authenticity ON civic_issues(authenticity_score DESC);
CREATE INDEX IF NOT EXISTS idx_civic_sources_issue_id ON civic_sources(issue_id);
CREATE INDEX IF NOT EXISTS idx_civic_sources_status ON civic_sources(status);
CREATE INDEX IF NOT EXISTS idx_ngos_causes ON ngos USING GIN(primary_causes);
CREATE INDEX IF NOT EXISTS idx_ngos_wards ON ngos USING GIN(operating_wards);
CREATE INDEX IF NOT EXISTS idx_events_issue_id ON ngo_volunteer_events(issue_id);
CREATE INDEX IF NOT EXISTS idx_events_ngo_id ON ngo_volunteer_events(ngo_id);
CREATE INDEX IF NOT EXISTS idx_events_status ON ngo_volunteer_events(status);

-- Vector Cosine Distance Index (HNSW for production sub-millisecond retrieval)
CREATE INDEX IF NOT EXISTS idx_civic_issues_embedding_hnsw 
ON civic_issues USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 7. Stored Procedure: match_similar_civic_issues
-- Performs vector cosine similarity search (1 - cosine distance <=>)
-- Accepts a 768-dim query embedding and configurable similarity threshold (default > 0.82)
CREATE OR REPLACE FUNCTION match_similar_civic_issues (
    query_embedding VECTOR(768),
    similarity_threshold FLOAT DEFAULT 0.82,
    match_count INT DEFAULT 5,
    filter_ward VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    title TEXT,
    summary TEXT,
    category VARCHAR,
    ward VARCHAR,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    severity VARCHAR,
    authenticity_score INT,
    responsible_authority TEXT,
    source_count INT,
    status VARCHAR,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        ci.id,
        ci.title,
        ci.summary,
        ci.category,
        ci.ward,
        ci.latitude,
        ci.longitude,
        ci.severity,
        ci.authenticity_score,
        ci.responsible_authority,
        ci.source_count,
        ci.status,
        (1.0 - (ci.embedding <=> query_embedding))::FLOAT AS similarity
    FROM civic_issues ci
    WHERE
        ci.embedding IS NOT NULL
        AND (filter_ward IS NULL OR ci.ward = filter_ward)
        AND (1.0 - (ci.embedding <=> query_embedding)) >= similarity_threshold
    ORDER BY ci.embedding <=> query_embedding ASC
    LIMIT match_count;
END;
$$;

-- 8. Seed Initial Verified Demonstration NGOs
INSERT INTO ngos (id, name, primary_causes, operating_wards, contact_email, is_verified)
VALUES
    ('c1111111-1111-4111-8111-111111111111', 'CleanCity Green Action Foundation', ARRAY['Sanitation', 'Environment'], ARRAY['Koramangala Ward 151', 'Indiranagar Ward 82', 'HSR Layout Ward 174'], 'contact@cleancity.org', TRUE),
    ('c2222222-2222-4222-8222-222222222222', 'SafeRoads & Rapid Drainage Collective', ARRAY['Roads & Transit', 'Waterlogging', 'Public Safety'], ARRAY['Koramangala Ward 151', 'Whitefield Ward 84', 'Bellandur Ward 150'], 'actions@saferoads.org', TRUE),
    ('c3333333-3333-4333-8333-333333333333', 'Bangalore Water Watch & Flood Response', ARRAY['Waterlogging', 'Environment', 'Public Safety'], ARRAY['HSR Layout Ward 174', 'Bellandur Ward 150', 'Marathahalli Ward 85'], 'alert@waterwatch.ngo', TRUE)
ON CONFLICT (contact_email) DO NOTHING;
