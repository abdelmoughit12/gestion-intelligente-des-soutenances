-- Seed data for Ai_Soutenance (PostgreSQL)
-- Run: psql -h <host> -U <user> -d <db> -f seed.sql

-- 1) Users
INSERT INTO users (id, cni, last_name, first_name, email, hashed_password, role)
VALUES
  (1, 'CNI123456', 'El', 'Prof', 'prof1@example.com', 'hashed', 'professor'),
  (2, 'CNE987654', 'Student', 'Alice', 'student1@example.com', 'hashed', 'student'),
  (3, 'CNI222333', 'Prof2', 'Bob', 'prof2@example.com', 'hashed', 'professor')
ON CONFLICT DO NOTHING;

-- 2) Professors (user_id references users.id)
INSERT INTO professors (user_id, specialty)
VALUES
  (1, 'Machine Learning'),
  (3, 'Distributed Systems')
ON CONFLICT DO NOTHING;

-- 3) Students
INSERT INTO students (user_id, major, cne, year)
VALUES
  (2, 'Computer Science', 'CNE2025001', 5)
ON CONFLICT DO NOTHING;

-- 4) Reports (file_name must match a file in backend/storage/reports/)
INSERT INTO reports (id, file_name, ai_summary, ai_domain, ai_similarity_score, student_id)
VALUES
  (1, 'sample_report.pdf', 'Résumé IA: Excellent travail.', 'AI', 0.12, 2)
ON CONFLICT DO NOTHING;

-- 5) Thesis Defenses
INSERT INTO thesis_defenses (id, student_id, title, description, status, defense_date, defense_time, report_id)
VALUES
  (1, 2, 'AI-Powered Cloud', 'Projet sur IA et Cloud', 'scheduled', '2025-12-20', '10:00:00', 1)
ON CONFLICT DO NOTHING;

-- 6) Jury Members
INSERT INTO jury_members (thesis_defense_id, professor_id, role)
VALUES
  (1, 1, 'president'),
  (1, 3, 'member')
ON CONFLICT DO NOTHING;

-- 7) Notifications
INSERT INTO notifications (id, user_id, title, message, action_type, is_read, creation_date)
VALUES
  (1, 1, 'Soutenance assignée', 'Vous avez été assigné à la soutenance AI-Powered Cloud', 'assignment', false, '2025-12-15 09:00:00'),
  (2, 1, 'Rapport reçu', 'Le rapport pour AI-Powered Cloud a été déposé', 'report', false, '2025-12-14 18:30:00')
ON CONFLICT DO NOTHING;



COMMIT;
