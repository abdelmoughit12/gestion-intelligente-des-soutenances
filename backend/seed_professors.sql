-- Insert professor users
INSERT INTO
    users (
        cni,
        last_name,
        first_name,
        email,
        hashed_password,
        role
    )
VALUES (
        'CNI001',
        'Alami',
        'Ahmed',
        'ahmed.alami@university.ma',
        '$2b$12$hashedpassword1',
        'professor'
    ),
    (
        'CNI002',
        'Bennani',
        'Fatima',
        'fatima.bennani@university.ma',
        '$2b$12$hashedpassword2',
        'professor'
    ),
    (
        'CNI003',
        'El Idrissi',
        'Mohamed',
        'mohamed.elidrissi@university.ma',
        '$2b$12$hashedpassword3',
        'professor'
    );

-- Insert professor details
INSERT INTO
    professors (user_id, specialty)
SELECT
    id,
    CASE
        WHEN last_name = 'Alami' THEN 'Artificial Intelligence & Machine Learning'
        WHEN last_name = 'Bennani' THEN 'Web Development & Cloud Computing'
        WHEN last_name = 'El Idrissi' THEN 'IoT & Embedded Systems'
    END
FROM users
WHERE
    role = 'professor';

-- Verify
SELECT u.id, u.first_name, u.last_name, p.specialty
FROM users u
    JOIN professors p ON u.id = p.user_id;