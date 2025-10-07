-- ============================================
-- Interactive Story Generator - Database Schema
-- SQLite DDL (Data Definition Language)
-- ============================================
-- Use este arquivo para:
-- 1. Criar banco de dados do zero
-- 2. Visualizar em DBeaver/MySQL Workbench
-- 3. Documentação da estrutura
-- ============================================

-- ============================================
-- DROP TABLES (if exists)
-- ============================================
DROP TABLE IF EXISTS story_jobs;
DROP TABLE IF EXISTS story_nodes;
DROP TABLE IF EXISTS stories;
DROP TABLE IF EXISTS users;

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE users (
    -- Primary Key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Authentication Fields
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CHECK (email LIKE '%@%'),
    CHECK (LENGTH(email) >= 3)
);

-- Indexes for users
CREATE INDEX idx_users_email ON users(email);

-- Comments (SQLite doesn't support inline comments, so documented here)
-- id: Auto-incrementing primary key
-- email: User email address for authentication (unique, validated)
-- hashed_password: Bcrypt hashed password (never store plain text!)
-- created_at: Account creation timestamp

-- ============================================
-- STORIES TABLE
-- ============================================
CREATE TABLE stories (
    -- Primary Key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Story Information
    title VARCHAR(500),
    session_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for stories
CREATE INDEX idx_stories_title ON stories(title);
CREATE UNIQUE INDEX idx_stories_session_id ON stories(session_id);

-- Comments
-- id: Auto-incrementing primary key
-- title: AI-generated story title
-- session_id: Unique session identifier (UUID format)
-- created_at: Story creation timestamp

-- ============================================
-- STORY_NODES TABLE
-- ============================================
CREATE TABLE story_nodes (
    -- Primary Key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Key
    story_id INTEGER NOT NULL,
    
    -- Node Content
    content TEXT,
    
    -- Node Type Flags
    is_root BOOLEAN DEFAULT 0,
    is_ending BOOLEAN DEFAULT 0,
    is_winning_ending BOOLEAN DEFAULT 0,
    
    -- Choices (stored as JSON)
    options TEXT, -- JSON array of choices
    
    -- Foreign Key Constraint
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE CASCADE,
    
    -- Validation
    CHECK (is_root IN (0, 1)),
    CHECK (is_ending IN (0, 1)),
    CHECK (is_winning_ending IN (0, 1))
);

-- Indexes for story_nodes
CREATE INDEX idx_story_nodes_story_id ON story_nodes(story_id);

-- Comments
-- id: Auto-incrementing primary key
-- story_id: Foreign key to parent story (CASCADE DELETE)
-- content: Narrative text content of this node
-- is_root: 1 if this is the starting node, 0 otherwise
-- is_ending: 1 if this is a final node, 0 otherwise
-- is_winning_ending: 1 if this is a winning ending, 0 otherwise
-- options: JSON array of available choices
--   Format: [{"text": "Choice text", "next_node_id": 2}]

-- ============================================
-- STORY_JOBS TABLE
-- ============================================
CREATE TABLE story_jobs (
    -- Primary Key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Job Identification
    job_id VARCHAR(100) UNIQUE NOT NULL,
    session_id VARCHAR(100),
    
    -- Job Details
    theme VARCHAR(500),
    status VARCHAR(50) NOT NULL,
    
    -- Result
    story_id INTEGER,
    error TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Foreign Key Constraint
    FOREIGN KEY (story_id) REFERENCES stories(id) ON DELETE SET NULL,
    
    -- Status Validation
    CHECK (status IN ('pending', 'completed', 'failed'))
);

-- Indexes for story_jobs
CREATE UNIQUE INDEX idx_story_jobs_job_id ON story_jobs(job_id);
CREATE INDEX idx_story_jobs_session_id ON story_jobs(session_id);
CREATE INDEX idx_story_jobs_status ON story_jobs(status);

-- Comments
-- id: Auto-incrementing primary key
-- job_id: Unique job identifier (UUID format)
-- session_id: Session identifier linking to story
-- theme: User-provided story theme/prompt
-- status: Job status (pending, completed, failed)
-- story_id: Foreign key to generated story (NULL until complete)
-- error: Error message if job failed
-- created_at: Job creation timestamp
-- completed_at: Job completion timestamp

-- ============================================
-- SAMPLE DATA (for testing)
-- ============================================

-- Sample User
INSERT INTO users (email, hashed_password) VALUES
('demo@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyWpQXbxK3Ke');
-- Password: demo123 (hashed with bcrypt)

-- Sample Story
INSERT INTO stories (title, session_id) VALUES
('The Dragon Quest', 'session-abc-123');

-- Sample Story Nodes
INSERT INTO story_nodes (story_id, content, is_root, is_ending, is_winning_ending, options) VALUES
(1, 'You stand before a towering castle. The air is thick with magic.', 1, 0, 0, 
 '[{"text":"Enter the castle","next_node_id":2},{"text":"Explore the forest","next_node_id":3}]'),
(1, 'Inside the castle, you meet a friendly wizard who offers help.', 0, 1, 1, '[]'),
(1, 'In the forest, you get lost and never find your way back.', 0, 1, 0, '[]');

-- Sample Job
INSERT INTO story_jobs (job_id, session_id, theme, status, story_id, completed_at) VALUES
('job-xyz-789', 'session-abc-123', 'medieval fantasy', 'completed', 1, CURRENT_TIMESTAMP);

-- ============================================
-- USEFUL QUERIES
-- ============================================

-- Get complete story with all nodes
-- SELECT 
--     s.id, s.title, s.session_id, s.created_at,
--     n.id as node_id, n.content, n.is_root, n.is_ending, n.options
-- FROM stories s
-- LEFT JOIN story_nodes n ON s.id = n.story_id
-- WHERE s.id = 1;

-- Check job status
-- SELECT job_id, status, theme, error, completed_at
-- FROM story_jobs
-- WHERE job_id = 'job-xyz-789';

-- Get all root nodes (story starts)
-- SELECT s.title, n.content
-- FROM story_nodes n
-- JOIN stories s ON n.story_id = s.id
-- WHERE n.is_root = 1;

-- Get all endings
-- SELECT s.title, n.content, n.is_winning_ending
-- FROM story_nodes n
-- JOIN stories s ON n.story_id = s.id
-- WHERE n.is_ending = 1;

-- Get pending jobs
-- SELECT job_id, theme, created_at
-- FROM story_jobs
-- WHERE status = 'pending'
-- ORDER BY created_at DESC;

-- ============================================
-- STATISTICS QUERIES
-- ============================================

-- Total stories created
-- SELECT COUNT(*) as total_stories FROM stories;

-- Total nodes created
-- SELECT COUNT(*) as total_nodes FROM story_nodes;

-- Average nodes per story
-- SELECT AVG(node_count) as avg_nodes_per_story
-- FROM (
--     SELECT story_id, COUNT(*) as node_count
--     FROM story_nodes
--     GROUP BY story_id
-- );

-- Job success rate
-- SELECT 
--     status,
--     COUNT(*) as count,
--     ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM story_jobs), 2) as percentage
-- FROM story_jobs
-- GROUP BY status;

-- ============================================
-- MAINTENANCE
-- ============================================

-- Clean up old failed jobs (older than 7 days)
-- DELETE FROM story_jobs
-- WHERE status = 'failed'
-- AND created_at < datetime('now', '-7 days');

-- Clean up orphaned nodes (shouldn't happen with CASCADE, but just in case)
-- DELETE FROM story_nodes
-- WHERE story_id NOT IN (SELECT id FROM stories);

-- ============================================
-- PERFORMANCE OPTIMIZATION
-- ============================================

-- Analyze tables for query optimization
-- ANALYZE users;
-- ANALYZE stories;
-- ANALYZE story_nodes;
-- ANALYZE story_jobs;

-- Vacuum database to reclaim space
-- VACUUM;

-- ============================================
-- BACKUP
-- ============================================

-- To backup database:
-- sqlite3 databse.db ".backup backup.db"

-- To restore:
-- sqlite3 databse.db ".restore backup.db"

-- ============================================
-- END OF SCHEMA
-- ============================================
