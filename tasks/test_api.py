"""
API tests for the tasks application
"""
import json
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
import os
import tempfile
from .database import TaskDatabase

class TaskDatabaseTest(TestCase):
    """Test the database module"""
    def setUp(self):
        """Set up test database"""
        self.db = TaskDatabase()
    
    def test_create_task(self):
        """Test creating a task"""
        task = self.db.create_task("Test Task", "Test Description", "2024-12-31")
        
        self.assertIsNotNone(task)
        self.assertEqual(task['title'], "Test Task")
        self.assertEqual(task['description'], "Test Description")
        self.assertEqual(task['due_date'], "2024-12-31")
        self.assertEqual(task['status'], "pending")
        self.assertIsNotNone(task['id'])
    
    def test_get_all_tasks(self):
        """Test getting all tasks"""
        # Create some test tasks
        self.db.create_task("Task 1", "Description 1")
        self.db.create_task("Task 2", "Description 2")
        
        tasks = self.db.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['title'], "Task 2")  # Most recent first
        self.assertEqual(tasks[1]['title'], "Task 1")
    
    def test_get_task_by_id(self):
        """Test getting a task by ID"""
        task = self.db.create_task("Test Task", "Test Description")
        task_id = task['id']
        
        retrieved_task = self.db.get_task_by_id(task_id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task['title'], "Test Task")
        
        # Test non-existent task
        non_existent = self.db.get_task_by_id(999)
        self.assertIsNone(non_existent)
    
    def test_update_task(self):
        """Test updating a task"""
        task = self.db.create_task("Original Title", "Original Description")
        task_id = task['id']
        
        # Update task
        updated_task = self.db.update_task(
            task_id, 
            title="Updated Title", 
            status="completed"
        )
        
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task['title'], "Updated Title")
        self.assertEqual(updated_task['status'], "completed")
        self.assertEqual(updated_task['description'], "Original Description")  # Should remain unchanged
    
    def test_delete_task(self):
        """Test deleting a task"""
        task = self.db.create_task("Task to Delete")
        task_id = task['id']
        
        # Delete task
        success = self.db.delete_task(task_id)
        self.assertTrue(success)
        
        # Verify task is deleted
        deleted_task = self.db.get_task_by_id(task_id)
        self.assertIsNone(deleted_task)
        
        # Test deleting non-existent task
        success = self.db.delete_task(999)
        self.assertFalse(success)
    
    def test_get_tasks_by_status(self):
        """Test getting tasks by status"""
        # Create tasks with different statuses
        task1 = self.db.create_task("Pending Task")
        task2 = self.db.create_task("In Progress Task")
        task3 = self.db.create_task("Completed Task")
        
        # Update statuses
        self.db.update_task(task1['id'], status="pending")
        self.db.update_task(task2['id'], status="in_progress")
        self.db.update_task(task3['id'], status="completed")
        
        # Test filtering
        pending_tasks = self.db.get_tasks_by_status("pending")
        in_progress_tasks = self.db.get_tasks_by_status("in_progress")
        completed_tasks = self.db.get_tasks_by_status("completed")
        
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(len(in_progress_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
        
        self.assertEqual(pending_tasks[0]['title'], "Pending Task")
        self.assertEqual(in_progress_tasks[0]['title'], "In Progress Task")
        self.assertEqual(completed_tasks[0]['title'], "Completed Task")


class TaskAPITest(TestCase):
    """Test the API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_create_task_api(self):
        """Test creating a task via API"""
        data = {
            "title": "API Test Task",
            "description": "Test Description",
            "due_date": "2024-12-31"
        }
        
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data']['title'], "API Test Task")
        self.assertEqual(response_data['data']['status'], "pending")
    
    def test_create_task_validation(self):
        """Test task creation validation"""
        # Test missing title
        data = {"description": "No title"}
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['error'], 'MISSING_TITLE')
        
        # Test empty title
        data = {"title": ""}
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        # Test title too long
        data = {"title": "x" * 201}
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'TITLE_TOO_LONG')
        
        # Test invalid date format
        data = {"title": "Test", "due_date": "invalid-date"}
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'INVALID_DATE_FORMAT')
    
    def test_get_tasks_api(self):
        """Test getting tasks via API"""
        # Create some test tasks first
        self.client.post(
            '/api/tasks/',
            data=json.dumps({"title": "Task 1"}),
            content_type='application/json'
        )
        self.client.post(
            '/api/tasks/',
            data=json.dumps({"title": "Task 2"}),
            content_type='application/json'
        )
        
        # Get all tasks
        response = self.client.get('/api/tasks/list/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(len(response_data['data']), 2)
    
    def test_get_task_by_id_api(self):
        """Test getting a specific task via API"""
        # Create a task
        create_response = self.client.post(
            '/api/tasks/',
            data=json.dumps({"title": "Specific Task"}),
            content_type='application/json'
        )
        task_id = json.loads(create_response.content)['data']['id']
        
        # Get the task
        response = self.client.get(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data']['title'], "Specific Task")
        
        # Test non-existent task
        response = self.client.get('/api/tasks/999/')
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'TASK_NOT_FOUND')
    
    def test_update_task_api(self):
        """Test updating a task via API"""
        # Create a task
        create_response = self.client.post(
            '/api/tasks/',
            data=json.dumps({"title": "Original Title"}),
            content_type='application/json'
        )
        task_id = json.loads(create_response.content)['data']['id']
        
        # Update the task
        update_data = {
            "title": "Updated Title",
            "status": "completed"
        }
        response = self.client.put(
            f'/api/tasks/{task_id}/update/',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data']['title'], "Updated Title")
        self.assertEqual(response_data['data']['status'], "completed")
    
    def test_delete_task_api(self):
        """Test deleting a task via API"""
        # Create a task
        create_response = self.client.post(
            '/api/tasks/',
            data=json.dumps({"title": "Task to Delete"}),
            content_type='application/json'
        )
        task_id = json.loads(create_response.content)['data']['id']
        
        # Delete the task
        response = self.client.delete(f'/api/tasks/{task_id}/delete/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        
        # Verify task is deleted
        get_response = self.client.get(f'/api/tasks/{task_id}/')
        self.assertEqual(get_response.status_code, 404)
    
    def test_invalid_json(self):
        """Test handling of invalid JSON"""
        response = self.client.post(
            '/api/tasks/',
            data="invalid json",
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'JSON_DECODE_ERROR')
    
    def test_invalid_task_id(self):
        """Test handling of invalid task IDs"""
        response = self.client.get('/api/tasks/invalid/')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'INVALID_TASK_ID')
    
    def test_filter_tasks_by_status(self):
        """Test filtering tasks by status"""
        # Create tasks with different statuses
        task1_response = self.client.post(
            '/api/tasks/',
            data=json.dumps({"title": "Pending Task"}),
            content_type='application/json'
        )
        task1_id = json.loads(task1_response.content)['data']['id']
        
        task2_response = self.client.post(
            '/api/tasks/',
            data=json.dumps({"title": "Completed Task"}),
            content_type='application/json'
        )
        task2_id = json.loads(task2_response.content)['data']['id']
        
        # Update statuses
        self.client.put(
            f'/api/tasks/{task1_id}/update/',
            data=json.dumps({"status": "pending"}),
            content_type='application/json'
        )
        self.client.put(
            f'/api/tasks/{task2_id}/update/',
            data=json.dumps({"status": "completed"}),
            content_type='application/json'
        )
        
        # Test filtering
        response = self.client.get('/api/tasks/list/?status=pending')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['data']), 1)
        self.assertEqual(response_data['data'][0]['title'], "Pending Task")
        
        response = self.client.get('/api/tasks/list/?status=completed')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['data']), 1)
        self.assertEqual(response_data['data'][0]['title'], "Completed Task")
        
        # Test invalid status
        response = self.client.get('/api/tasks/list/?status=invalid')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'INVALID_STATUS')


class TemplateViewTest(TestCase):
    """Test template views"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_task_list_view(self):
        """Test task list template view"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'To-Do List')
        self.assertContains(response, 'My Tasks')
    
    def test_add_task_view(self):
        """Test add task template view"""
        response = self.client.get('/add/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Task')
        self.assertContains(response, 'Title')
        self.assertContains(response, 'Description')
