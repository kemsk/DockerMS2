# Django REST API with MySQL

This is a Django REST API project with MySQL database backend, containerized with Docker.

## Features

- Django REST Framework for API endpoints
- MySQL database integration
- JWT authentication
- Dockerized development and production environments
- Comprehensive API documentation

## Prerequisites

- Docker and Docker Compose
- Git

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file with your own settings.

3. Build and start the Docker containers:
   ```
   docker-compose up -d --build
   ```

4. The API will be available at `http://localhost:8000/`

## API Endpoints

- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{id}/` - Retrieve a specific user
- `PUT /api/users/{id}/` - Update a specific user
- `DELETE /api/users/{id}/` - Delete a specific user
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token

## Development

### Running Tests

