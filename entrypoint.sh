#!/bin/bash

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

mysql -h "${DB_HOST}" -u "root" -p"$DB_ROOT_PASSWORD" "$DB_NAME" <<EOF

SET GLOBAL time_zone = 'Asia/Manila';
SET time_zone = 'Asia/Manila';

INSERT INTO TS_student VALUES 
(1, 'Alice', 'Smith', 'Marie'),
(2, 'Bob', 'Johnson', ''),
(3, 'Charlie', 'Brown', 'Lee'),
(4, 'Diana', 'Prince', 'Grace'),
(5, 'Ethan', 'Clark', 'James');

INSERT INTO TS_violation VALUES
(1, 'Uniform Violation'),
(2, 'Dress Code Violation'),
(3, 'ID Violation'),
(4, 'ID Not Claimed');

EOF

echo "Database initialized."

# Start the application using Gunicorn
python -m gunicorn --bind 0.0.0.0:8002 --workers 3 XUSSIO_EVS.wsgi:application