"""
Database module for handling task operations using raw SQL
"""
import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any
from django.conf import settings

logger = logging.getLogger(__name__)

class TaskDatabase:
    """Database handler for tasks using raw SQL"""
    
    def __init__(self):
        self.db_path = settings.DATABASES['default']['NAME']
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def init_database(self):
        """Initialize database and create tasks table if not exists"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        due_date DATE,
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
                logger.info("Database initialized successfully")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def create_task(self, title: str, description: str = None, due_date: str = None) -> Dict[str, Any]:
        """Create a new task"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO tasks (title, description, due_date, status)
                    VALUES (?, ?, ?, 'pending')
                ''', (title, description, due_date))
                
                task_id = cursor.lastrowid
                conn.commit()
                
                # Fetch the created task
                cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
                task = cursor.fetchone()
                
                logger.info(f"Task created successfully with ID: {task_id}")
                return dict(task) if task else {}
                
        except sqlite3.Error as e:
            logger.error(f"Error creating task: {e}")
            raise
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
                tasks = cursor.fetchall()
                
                logger.info(f"Retrieved {len(tasks)} tasks")
                return [dict(task) for task in tasks]
                
        except sqlite3.Error as e:
            logger.error(f"Error retrieving tasks: {e}")
            raise
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
                task = cursor.fetchone()
                
                if task:
                    logger.info(f"Task {task_id} retrieved successfully")
                    return dict(task)
                else:
                    logger.warning(f"Task {task_id} not found")
                    return None
                    
        except sqlite3.Error as e:
            logger.error(f"Error retrieving task {task_id}: {e}")
            raise
    
    def update_task(self, task_id: int, title: str = None, description: str = None, 
                   due_date: str = None, status: str = None) -> Optional[Dict[str, Any]]:
        """Update a task"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Build dynamic update query
                update_fields = []
                params = []
                
                if title is not None:
                    update_fields.append("title = ?")
                    params.append(title)
                if description is not None:
                    update_fields.append("description = ?")
                    params.append(description)
                if due_date is not None:
                    update_fields.append("due_date = ?")
                    params.append(due_date)
                if status is not None:
                    update_fields.append("status = ?")
                    params.append(status)
                
                if not update_fields:
                    logger.warning("No fields to update")
                    return None
                
                update_fields.append("updated_at = CURRENT_TIMESTAMP")
                params.append(task_id)
                
                query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, params)
                
                if cursor.rowcount == 0:
                    logger.warning(f"Task {task_id} not found for update")
                    return None
                
                conn.commit()
                
                # Fetch the updated task
                cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
                task = cursor.fetchone()
                
                logger.info(f"Task {task_id} updated successfully")
                return dict(task) if task else None
                
        except sqlite3.Error as e:
            logger.error(f"Error updating task {task_id}: {e}")
            raise
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
                
                if cursor.rowcount == 0:
                    logger.warning(f"Task {task_id} not found for deletion")
                    return False
                
                conn.commit()
                logger.info(f"Task {task_id} deleted successfully")
                return True
                
        except sqlite3.Error as e:
            logger.error(f"Error deleting task {task_id}: {e}")
            raise
    
    def get_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get tasks by status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status,))
                tasks = cursor.fetchall()
                
                logger.info(f"Retrieved {len(tasks)} tasks with status: {status}")
                return [dict(task) for task in tasks]
                
        except sqlite3.Error as e:
            logger.error(f"Error retrieving tasks by status {status}: {e}")
            raise
