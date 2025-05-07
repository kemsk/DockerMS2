#!/bin/bash

# Run static collection and migrations
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# --- Insert data into SSIO_API DB ---
mysql -h "${SSIO_DATABASE_HOST}" -u "root" -p"$SSIO_DB_ROOT_PASSWORD" "$SSIO_DB_NAME" <<EOF

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

# --- Insert data into AD_DB ---
mysql -h "${AD_DATABASE_HOST}" -u "root" -p"$AD_DB_ROOT_PASSWORD" "$AD_DB_NAME" <<EOF

INSERT INTO AD_student (
    student_id, last_name, first_name, middle_name, course, year_level,
    email, address, phone_number, emergency_contact_number,
    emergency_contact_name, card_expiry_date, birthdate, school_year, college
) VALUES

(19990245, 'Smith', 'Alice', 'Marie', 'BSCS', 1,
 'alice@example.com', '123 Main St', '09171234567', '09179876543',
 'John Smith', '2025-05-31', '2003-04-10', '2024-2025', 'Engineering'),
(20190245, 'Johnson', 'Bob', '', 'BSIT', 2,
 'bob@example.com', '456 South Ave', '09181234567', '09181239876',
 'Mary Johnson', '2025-06-15', '2002-07-05', '2024-2025', 'Computing');

EOF

echo "Both databases initialized."

# Start the application using Gunicorn
python -m gunicorn --bind 0.0.0.0:8002 --workers 3 XUSSIO_EVS.wsgi:application