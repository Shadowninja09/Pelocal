"""
API views for task management
"""
import json
import logging
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from .database import TaskDatabase

logger = logging.getLogger(__name__)

# Initialize database handler
db = TaskDatabase()

def api_response(data=None, message="", status=200, error=None):
    """Helper function to create consistent API responses"""
    response_data = {
        "status": "success" if status < 400 else "error",
        "message": message,
        "data": data
    }
    
    if error:
        response_data["error"] = error
    
    return JsonResponse(response_data, status=status)

@csrf_exempt
@require_http_methods(["POST"])
def create_task(request):
    """Create a new task"""
    try:
        # Parse JSON data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return api_response(
                message="Invalid JSON data",
                status=400,
                error="JSON_DECODE_ERROR"
            )
        
        # Validate required fields
        title = data.get('title', '').strip()
        if not title:
            return api_response(
                message="Title is required",
                status=400,
                error="MISSING_TITLE"
            )
        
        if len(title) > 200:
            return api_response(
                message="Title must be less than 200 characters",
                status=400,
                error="TITLE_TOO_LONG"
            )
        
        # Extract optional fields
        description = data.get('description', '').strip() or None
        due_date = data.get('due_date', '').strip() or None
        
        # Validate due_date format if provided
        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                return api_response(
                    message="Invalid date format. Use YYYY-MM-DD",
                    status=400,
                    error="INVALID_DATE_FORMAT"
                )
        
        # Create task
        task = db.create_task(title, description, due_date)
        
        if task:
            logger.info(f"Task created successfully: {task['id']}")
            return api_response(
                data=task,
                message="Task created successfully",
                status=201
            )
        else:
            return api_response(
                message="Failed to create task",
                status=500,
                error="CREATION_FAILED"
            )
            
    except Exception as e:
        logger.error(f"Error in create_task: {str(e)}")
        return api_response(
            message="Internal server error",
            status=500,
            error="INTERNAL_ERROR"
        )

@require_http_methods(["GET"])
def get_tasks(request):
    """Get all tasks or filter by status"""
    try:
        status = request.GET.get('status', '').strip()
        
        if status:
            # Validate status
            valid_statuses = ['pending', 'in_progress', 'completed']
            if status not in valid_statuses:
                return api_response(
                    message=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
                    status=400,
                    error="INVALID_STATUS"
                )
            tasks = db.get_tasks_by_status(status)
        else:
            tasks = db.get_all_tasks()
        
        logger.info(f"Retrieved {len(tasks)} tasks")
        return api_response(
            data=tasks,
            message=f"Retrieved {len(tasks)} tasks successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in get_tasks: {str(e)}")
        return api_response(
            message="Internal server error",
            status=500,
            error="INTERNAL_ERROR"
        )

@require_http_methods(["GET"])
def get_task(request, task_id):
    """Get a specific task by ID"""
    try:
        # Validate task_id
        try:
            task_id = int(task_id)
        except ValueError:
            return api_response(
                message="Invalid task ID",
                status=400,
                error="INVALID_TASK_ID"
            )
        
        task = db.get_task_by_id(task_id)
        
        if task:
            logger.info(f"Task {task_id} retrieved successfully")
            return api_response(
                data=task,
                message="Task retrieved successfully"
            )
        else:
            return api_response(
                message="Task not found",
                status=404,
                error="TASK_NOT_FOUND"
            )
            
    except Exception as e:
        logger.error(f"Error in get_task: {str(e)}")
        return api_response(
            message="Internal server error",
            status=500,
            error="INTERNAL_ERROR"
        )

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_task(request, task_id):
    """Update a task"""
    try:
        # Validate task_id
        try:
            task_id = int(task_id)
        except ValueError:
            return api_response(
                message="Invalid task ID",
                status=400,
                error="INVALID_TASK_ID"
            )
        
        # Parse JSON data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return api_response(
                message="Invalid JSON data",
                status=400,
                error="JSON_DECODE_ERROR"
            )
        
        # Extract and validate fields
        title = data.get('title', '').strip() or None
        description = data.get('description', '').strip() or None
        due_date = data.get('due_date', '').strip() or None
        status = data.get('status', '').strip() or None
        
        # Validate title length if provided
        if title and len(title) > 200:
            return api_response(
                message="Title must be less than 200 characters",
                status=400,
                error="TITLE_TOO_LONG"
            )
        
        # Validate due_date format if provided
        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                return api_response(
                    message="Invalid date format. Use YYYY-MM-DD",
                    status=400,
                    error="INVALID_DATE_FORMAT"
                )
        
        # Validate status if provided
        if status:
            valid_statuses = ['pending', 'in_progress', 'completed']
            if status not in valid_statuses:
                return api_response(
                    message=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
                    status=400,
                    error="INVALID_STATUS"
                )
        
        # Update task
        task = db.update_task(task_id, title, description, due_date, status)
        
        if task:
            logger.info(f"Task {task_id} updated successfully")
            return api_response(
                data=task,
                message="Task updated successfully"
            )
        else:
            return api_response(
                message="Task not found",
                status=404,
                error="TASK_NOT_FOUND"
            )
            
    except Exception as e:
        logger.error(f"Error in update_task: {str(e)}")
        return api_response(
            message="Internal server error",
            status=500,
            error="INTERNAL_ERROR"
        )

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_task(request, task_id):
    """Delete a task"""
    try:
        # Validate task_id
        try:
            task_id = int(task_id)
        except ValueError:
            return api_response(
                message="Invalid task ID",
                status=400,
                error="INVALID_TASK_ID"
            )
        
        success = db.delete_task(task_id)
        
        if success:
            logger.info(f"Task {task_id} deleted successfully")
            return api_response(
                message="Task deleted successfully"
            )
        else:
            return api_response(
                message="Task not found",
                status=404,
                error="TASK_NOT_FOUND"
            )
            
    except Exception as e:
        logger.error(f"Error in delete_task: {str(e)}")
        return api_response(
            message="Internal server error",
            status=500,
            error="INTERNAL_ERROR"
        )

# Template views
def task_list_view(request):
    """Render task list template"""
    try:
        return render(request, 'tasks/task_list.html')
    except Exception as e:
        logger.error(f"Error in task_list_view: {str(e)}")
        return HttpResponse("Error loading page", status=500)

def add_task_view(request):
    """Render add task template"""
    try:
        return render(request, 'tasks/add_task.html')
    except Exception as e:
        logger.error(f"Error in add_task_view: {str(e)}")
        return HttpResponse("Error loading page", status=500)