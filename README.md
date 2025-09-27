# To-Do List Application

A comprehensive web application built with Django for managing tasks with RESTful APIs and a modern web interface.

## Features

- ✅ **RESTful API**: Complete CRUD operations for tasks
- ✅ **Web Interface**: Modern, responsive UI with Bootstrap
- ✅ **Database**: SQLite database with raw SQL (no ORM)
- ✅ **Task Management**: Create, read, update, delete tasks
- ✅ **Status Tracking**: Track task status (pending, in_progress, completed)
- ✅ **Due Dates**: Set and track task due dates
- ✅ **Filtering**: Filter tasks by status
- ✅ **Real-time Updates**: Dynamic web interface with JavaScript
- ✅ **Logging**: Comprehensive logging and exception handling
- ✅ **Testing**: Full test coverage with pytest
- ✅ **Documentation**: Complete API documentation

## Project Structure

```
todolist_project/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── pytest.ini              # Pytest configuration
├── README.md               # This file
├── API_DOCUMENTATION.md    # API documentation
├── todolist_project/       # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── tasks/                  # Tasks application
│   ├── __init__.py
│   ├── admin.py           # Django admin configuration
│   ├── apps.py            # App configuration
│   ├── models.py          # Database models (empty - using raw SQL)
│   ├── views.py           # API and template views
│   ├── urls.py            # URL routing
│   ├── database.py        # Database operations with raw SQL
│   ├── middleware.py      # Custom middleware
│   ├── tests.py           # Basic tests
│   └── test_api.py        # Comprehensive API tests
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── tasks/             # Task-specific templates
│       ├── task_list.html # Task list page
│       └── add_task.html  # Add task page
├── logs/                   # Application logs
└── db.sqlite3             # SQLite database (created automatically)
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd assignment
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Usage

### Web Interface

1. **View Tasks**: Visit `http://localhost:8000/` to see all tasks
2. **Add Task**: Click "Add Task" or visit `http://localhost:8000/add/`
3. **Edit Task**: Click the edit button on any task card
4. **Delete Task**: Click the delete button on any task card
5. **Filter Tasks**: Use the filter buttons to view tasks by status

### API Usage

The API provides RESTful endpoints for all operations:

#### Create Task
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Task", "description": "Task description", "due_date": "2024-12-31"}'
```

#### Get All Tasks
```bash
curl http://localhost:8000/api/tasks/list/
```

#### Get Task by ID
```bash
curl http://localhost:8000/api/tasks/1/
```

#### Update Task
```bash
curl -X PUT http://localhost:8000/api/tasks/1/update/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "status": "completed"}'
```

#### Delete Task
```bash
curl -X DELETE http://localhost:8000/api/tasks/1/delete/
```

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

## Testing

### Run All Tests

```bash
# Using Django's test runner
python manage.py test

# Using pytest
pytest

# Run specific test file
pytest tasks/test_api.py

# Run with verbose output
pytest -v
```

### Test Coverage

The application includes comprehensive tests covering:
- Database operations
- API endpoints
- Input validation
- Error handling
- Template rendering

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/list/` | Get all tasks (with optional status filter) |
| GET | `/api/tasks/{id}/` | Get a specific task |
| PUT | `/api/tasks/{id}/update/` | Update a task |
| DELETE | `/api/tasks/{id}/delete/` | Delete a task |

## Database Schema

The application uses a single `tasks` table with the following structure:

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    due_date DATE,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Configuration

### Environment Variables

The application uses Django's settings system. Key configurations:

- `DEBUG`: Set to `True` for development, `False` for production
- `SECRET_KEY`: Django secret key for security
- `DATABASES`: Database configuration (SQLite by default)

### Logging

Logs are written to:
- Console output (development)
- `logs/django.log` file

Log levels:
- `INFO`: General information
- `DEBUG`: Detailed debugging information
- `ERROR`: Error messages

## Deployment

### Production Considerations

1. **Environment Variables**: Use environment variables for sensitive settings
2. **Database**: Consider using PostgreSQL or MySQL for production
3. **Static Files**: Configure static file serving
4. **Security**: Set `DEBUG=False` and configure `ALLOWED_HOSTS`
5. **HTTPS**: Use HTTPS in production
6. **Authentication**: Implement user authentication if needed

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Development

### Adding New Features

1. **Database Changes**: Modify `tasks/database.py` for new database operations
2. **API Endpoints**: Add new views in `tasks/views.py`
3. **URL Routing**: Update `tasks/urls.py` for new endpoints
4. **Templates**: Add new templates in `templates/` directory
5. **Tests**: Add tests in `tasks/test_api.py`

### Code Style

The project follows Python best practices:
- PEP 8 style guide
- Type hints where appropriate
- Comprehensive error handling
- Detailed logging
- Clear documentation

## Troubleshooting

### Common Issues

1. **Database Errors**: Ensure the database file is writable
2. **Port Already in Use**: Change the port with `python manage.py runserver 8001`
3. **Import Errors**: Ensure virtual environment is activated
4. **Permission Errors**: Check file permissions for logs directory

### Debug Mode

Enable debug mode by setting `DEBUG=True` in `settings.py` for detailed error messages.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is created for educational purposes as part of an assignment.

## Support

For issues or questions:
1. Check the API documentation
2. Review the test files for usage examples
3. Check the logs for error details
4. Ensure all dependencies are installed correctly

## Future Enhancements

Potential improvements for future versions:
- User authentication and authorization
- Task categories and tags
- File attachments
- Email notifications
- Task sharing and collaboration
- Advanced filtering and search
- Export/import functionality
- Mobile app
- Real-time updates with WebSockets
