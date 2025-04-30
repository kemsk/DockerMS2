#!/bin/bash

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

mysql -h "${DB_HOST}" -u "root" -p"$DB_ROOT_PASSWORD" "$DB_NAME" <<EOF

Insert into TS_academicyear values
(1, '2024-2025', '2025-01-15', '2025-05-31', 1, 1);

INSERT INTO TS_student (first_name, last_name, middle_name)
VALUES ('Alice', 'Smith', 'Marie'),
('Bob', 'Johnson', ''),
('Charlie', 'Brown', 'Lee'),
('Diana', 'Prince', 'Grace'),
('Ethan', 'Clark', 'James');

INSERT INTO TS_violation VALUES
(1, 'Uniform Violation'),
(2, 'Dress Code Violation'),
(3, 'ID Violation'),
(4, 'ID Not Claimed');

EOF

# Start the application using Gunicorn
python -m gunicorn --bind 0.0.0.0:8002 --workers 3 XUSSIO_EVS.wsgi:application