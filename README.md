# Microservice Based Task Management System

A mini microservice system built with FastAPI with Auth Service and Task Service. 

### 1. Auth Service (Port 8000)
Authentication and token validation.

**Endpoints:**
- `POST /register` - Register user
- `POST /login` - Get JWT token
- `POST /validate-token` - Validate token

### 2. Task Service (Port 8001)
Task CRUD with role-based access.

**Endpoints:**
- `POST /tasks/` - Create task
- `GET /tasks/` - Get tasks (Admin sees all, User sees own)
- `PATCH /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task (Admin only)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Navigate to project:**
   ```bash
   cd "/Users/mac/Desktop/Heet Task"
   ```

2. **Install dependencies:**

   **Auth Service:**
   ```bash
   cd auth_service
   pip install -r requirements.txt
   cd ..
   ```

   **Task Service:**
   ```bash
   cd task_service
   pip install -r requirements.txt
   cd ..
   ```

3. **Environment variables:**
   
   Each service has `.env` file. You can change rate limit settings if needed.

## Running Services

Run each in separate terminal.

**Terminal 1 - Auth Service:**
```bash
cd auth_service
python main.py
```

**Terminal 2 - Task Service:**
```bash
cd task_service
python main.py
```

Services will be running at:
- Auth Service: http://localhost:8000
- Task Service: http://localhost:8001

## Testing

### Postman Collection
**Import the Postman collection: `Heet Practical Task.postman_collection.json`**

This collection includes all API endpoints with pre-configured requests.

### API Documentation
Each service has Swagger UI:
- Auth: http://localhost:8000/docs
- Task: http://localhost:8001/docs

### Testing Flow

#### 1. Register Users

**Admin:**
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "admin123",
    "role": "admin"
  }'
```

**User:**
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "user@example.com",
    "password": "user123",
    "role": "user"
  }'
```

#### 2. Login

**Admin Login:**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

**Login as User:**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "user123"
  }'
```

Save the `access_token` from the response for subsequent requests.

#### 3. Create Tasks (User Token Required)

```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_USER_TOKEN_HERE" \
  -d '{
    "title": "Complete Project Documentation",
    "description": "Write comprehensive README",
    "status": "pending"
  }'
```

#### 4. Get Tasks

**As User (see only own tasks):**
```bash
curl -X GET "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer YOUR_USER_TOKEN_HERE"
```

**As Admin (see all tasks):**
```bash
curl -X GET "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE"
```

#### 5. Update Task Status

```bash
curl -X PATCH "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_USER_TOKEN_HERE" \
  -d '{
    "status": "completed"
  }'
```

#### 6. Delete Task (Admin Only)

```bash
curl -X DELETE "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE"
```

## Security Features

### Rate Limiting

Both Auth Service and Task Service include rate limiting to prevent abuse.

### JWT Authentication

- Tokens expire after 30 minutes (configurable)
- Tokens include user_id and role
- All Task Service endpoints validate tokens with Auth Service

### Role-Based Access Control

- **Admin**: Can view all tasks and delete any task
- **User**: Can only view and update their own tasks

## Inter-Service Communication

- Task Service validates every request by calling Auth Service `/validate-token` endpoint
- Uses Python `requests` library for HTTP communication

## Database

Each service uses its own SQLite database:
- `auth_service/auth.db` - User accounts
- `task_service/tasks.db` - Tasks

Databases are created automatically on first run.

### Port Already in Use

If a port is already in use, you can change it:
1. Update the port in the service's `.env` file
2. Update references in other services' `.env` files
3. Restart all services