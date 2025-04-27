#!/usr/bin/env bash

# Collect static files and apply migrations
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Initialize the database with necessary records for SSIO
mysql -h "$DB_HOST" -u "root" -p"$DB_ROOT_PASSWORD" "$DB_NAME" <<EOF

-- Create table for violation records if it doesn't exist
CREATE TABLE IF NOT EXISTS SSIO_violation_record (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    violation_id INT NOT NULL,
    reason_id INT DEFAULT NULL,
    date_recorded DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at DATETIME DEFAULT NULL,
    resolved_by_staff_id INT DEFAULT NULL,
    remarks TEXT,
    FOREIGN KEY (violation_id) REFERENCES EVS_violation(id),
    FOREIGN KEY (reason_id) REFERENCES EVS_reason(id)
);

EOF

echo "Database and SSIO violation records initialized."

# Start Gunicorn server
python -m gunicorn --bind 0.0.0.0:8001 --workers 3 XUOSA_EVS.wsgi:application

# (Optional) Django runserver fallback
# python manage.py runserver 0.0.0.0:8000