#USING PYTHON OS
FROM python:3.13.1

#INITIALIZE THE WORKING DIRECTORY
WORKDIR /app

#INSTALL ALL LIBRARIES/DEPENDENCIES NEEDED
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#COPY ALL FILES IN THE WORKING DIRECTORY
COPY . .

#CMD COMMANDS
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]