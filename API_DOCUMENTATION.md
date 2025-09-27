# To-Do List API Documentation

## Overview

This document provides comprehensive documentation for the To-Do List API. The API follows RESTful principles and provides endpoints for managing tasks with full CRUD operations.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
    "status": "success",
    "message": "Operation completed successfully",
    "data": {
        // Response data here
    }
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error description",
    "error": "ERROR_CODE"
}
```

## Endpoints

### 1. Create Task

**POST** `/api/tasks/`

Creates a new task.

#### Request Body
```json
{
    "title": "string (required, max 200 chars)",
    "description": "string (optional)",
    "due_date": "string (optional, YYYY-MM-DD format)"
}
```

#### Example Request
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "due_date": "2024-12-31"
  }'
```

#### Success Response (201)
```json
{
    "status": "success",
    "message": "Task created successfully",
    "data": {
        "id": 1,
        "title": "Complete project documentation",
        "description": "Write comprehensive API documentation",
        "due_date": "2024-12-31",
        "status": "pending",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

#### Error Responses
- **400 Bad Request**: Missing title, title too long, invalid date format
- **500 Internal Server Error**: Database or server error

### 2. Get All Tasks

**GET** `/api/tasks/list/`

Retrieves all tasks or filters by status.

#### Query Parameters
- `status` (optional): Filter by status (`pending`, `in_progress`, `completed`)

#### Example Request
```bash
# Get all tasks
curl http://localhost:8000/api/tasks/list/

# Get only pending tasks
curl http://localhost:8000/api/tasks/list/?status=pending
```

#### Success Response (200)
```json
{
    "status": "success",
    "message": "Retrieved 2 tasks successfully",
    "data": [
        {
            "id": 2,
            "title": "Review code",
            "description": "Code review for pull request",
            "due_date": "2024-01-20",
            "status": "in_progress",
            "created_at": "2024-01-15T11:00:00Z",
            "updated_at": "2024-01-15T11:30:00Z"
        },
        {
            "id": 1,
            "title": "Complete project documentation",
            "description": "Write comprehensive API documentation",
            "due_date": "2024-12-31",
            "status": "pending",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### Error Responses
- **400 Bad Request**: Invalid status filter
- **500 Internal Server Error**: Database or server error

### 3. Get Task by ID

**GET** `/api/tasks/{id}/`

Retrieves a specific task by its ID.

#### Path Parameters
- `id` (required): Task ID (integer)

#### Example Request
```bash
curl http://localhost:8000/api/tasks/1/
```

#### Success Response (200)
```json
{
    "status": "success",
    "message": "Task retrieved successfully",
    "data": {
        "id": 1,
        "title": "Complete project documentation",
        "description": "Write comprehensive API documentation",
        "due_date": "2024-12-31",
        "status": "pending",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
}
```

#### Error Responses
- **400 Bad Request**: Invalid task ID format
- **404 Not Found**: Task not found
- **500 Internal Server Error**: Database or server error

### 4. Update Task

**PUT** `/api/tasks/{id}/update/`

Updates an existing task. All fields are optional.

#### Path Parameters
- `id` (required): Task ID (integer)

#### Request Body
```json
{
    "title": "string (optional, max 200 chars)",
    "description": "string (optional)",
    "due_date": "string (optional, YYYY-MM-DD format)",
    "status": "string (optional: pending, in_progress, completed)"
}
```

#### Example Request
```bash
curl -X PUT http://localhost:8000/api/tasks/1/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation - Updated",
    "status": "in_progress"
  }'
```

#### Success Response (200)
```json
{
    "status": "success",
    "message": "Task updated successfully",
    "data": {
        "id": 1,
        "title": "Complete project documentation - Updated",
        "description": "Write comprehensive API documentation",
        "due_date": "2024-12-31",
        "status": "in_progress",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T12:00:00Z"
    }
}
```

#### Error Responses
- **400 Bad Request**: Invalid task ID, title too long, invalid date format, invalid status
- **404 Not Found**: Task not found
- **500 Internal Server Error**: Database or server error

### 5. Delete Task

**DELETE** `/api/tasks/{id}/delete/`

Deletes a task by its ID.

#### Path Parameters
- `id` (required): Task ID (integer)

#### Example Request
```bash
curl -X DELETE http://localhost:8000/api/tasks/1/delete/
```

#### Success Response (200)
```json
{
    "status": "success",
    "message": "Task deleted successfully"
}
```

#### Error Responses
- **400 Bad Request**: Invalid task ID format
- **404 Not Found**: Task not found
- **500 Internal Server Error**: Database or server error

## Data Models

### Task Object
```json
{
    "id": "integer (auto-generated)",
    "title": "string (required, max 200 chars)",
    "description": "string (optional)",
    "due_date": "string (optional, YYYY-MM-DD format)",
    "status": "string (pending, in_progress, completed)",
    "created_at": "string (ISO 8601 timestamp)",
    "updated_at": "string (ISO 8601 timestamp)"
}
```

### Status Values
- `pending`: Task is not yet started
- `in_progress`: Task is currently being worked on
- `completed`: Task has been finished

## Error Codes

| Code | Description |
|------|-------------|
| `JSON_DECODE_ERROR` | Invalid JSON in request body |
| `MISSING_TITLE` | Title field is required but missing |
| `TITLE_TOO_LONG` | Title exceeds 200 character limit |
| `INVALID_DATE_FORMAT` | Date format should be YYYY-MM-DD |
| `INVALID_STATUS` | Status must be one of: pending, in_progress, completed |
| `INVALID_TASK_ID` | Task ID must be a valid integer |
| `TASK_NOT_FOUND` | Task with specified ID does not exist |
| `INTERNAL_ERROR` | Internal server error |

## Rate Limiting

Currently, there are no rate limits implemented. In a production environment, consider implementing rate limiting to prevent abuse.

## CORS

The API does not currently implement CORS headers. If you need to access the API from a different domain, you may need to configure CORS settings.

## Examples

### Complete CRUD Workflow

1. **Create a task:**
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Django", "description": "Complete Django tutorial"}'
```

2. **Get all tasks:**
```bash
curl http://localhost:8000/api/tasks/list/
```

3. **Update the task:**
```bash
curl -X PUT http://localhost:8000/api/tasks/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

4. **Get specific task:**
```bash
curl http://localhost:8000/api/tasks/1/
```

5. **Delete the task:**
```bash
curl -X DELETE http://localhost:8000/api/tasks/1/delete/
```

### Filtering Tasks

```bash
# Get only completed tasks
curl http://localhost:8000/api/tasks/list/?status=completed

# Get tasks in progress
curl http://localhost:8000/api/tasks/list/?status=in_progress
```

## Web Interface

The application also provides a web interface accessible at:
- Task List: `http://localhost:8000/`
- Add Task: `http://localhost:8000/add/`

The web interface uses the same API endpoints and provides a user-friendly interface for managing tasks.

## Testing

The API includes comprehensive tests. Run tests using:

```bash
# Using Django's test runner
python manage.py test

# Using pytest
pytest
```

## Logging

The application logs all API requests and responses. Logs are stored in the `logs/` directory and also displayed in the console during development.

## Database

The application uses SQLite by default. The database file is created automatically at `db.sqlite3` in the project root. The database schema is created automatically when the application starts.

## Security Considerations

- Input validation is implemented for all endpoints
- SQL injection protection through parameterized queries
- XSS protection through proper HTML escaping in templates
- CSRF protection is disabled for API endpoints (as they are stateless)

For production deployment, consider:
- Implementing authentication and authorization
- Using HTTPS
- Adding rate limiting
- Implementing proper CORS configuration
- Using environment variables for sensitive configuration
