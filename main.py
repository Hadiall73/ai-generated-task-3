Below is a production-quality implementation of a relational database for storing tasks data using SQLAlchemy ORM. SQLAlchemy is a powerful Python library for working with databases, and we'll use it to define a schema, handle database connections, and perform CRUD operations.

---

### Explanation:
1. **Database Choice**: We'll use a relational database (e.g., SQLite for simplicity, but it can be replaced with PostgreSQL, MySQL, etc.).
2. **Schema Design**: A `Task` table will store task-related information such as `id`, `title`, `description`, `status`, `priority`, and `due_date`.
3. **SQLAlchemy ORM**: We'll define the `Task` model using SQLAlchemy's declarative base.
4. **Input Validation**: We'll validate inputs before inserting them into the database.
5. **Error Handling**: We'll handle database connection errors and other exceptions gracefully.
6. **Security Best Practices**: We'll use parameterized queries to prevent SQL injection.

---

### Code Implementation

```python
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import enum

# Define the base class for ORM models
Base = declarative_base()

# Enum for task status
class TaskStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

# Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Integer, nullable=False, default=1)  # 1 = Low, 2 = Medium, 3 = High
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}', priority={self.priority})>"

# Database setup
DATABASE_URL = "sqlite:///tasks.db"  # Replace with your database URL (e.g., PostgreSQL, MySQL)

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Database utility functions
def get_db_session():
    """Create a new database session."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# CRUD Operations
def create_task(db, title: str, description: str = None, status: TaskStatus = TaskStatus.PENDING, priority: int = 1, due_date: datetime = None):
    """Create a new task."""
    if not title or len(title) > 255:
        raise ValueError("Title is required and must be less than 255 characters.")
    if priority not in [1, 2, 3]:
        raise ValueError("Priority must be 1 (Low), 2 (Medium), or 3 (High).")
    
    new_task = Task(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date
    )
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error creating task: {str(e)}")

def get_task_by_id(db, task_id: int):
    """Retrieve a task by its ID."""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        return task
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error retrieving task: {str(e)}")

def update_task_status(db, task_id: int, new_status: TaskStatus):
    """Update the status of a task."""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        task.status = new_status
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error updating task status: {str(e)}")

def delete_task(db, task_id: int):
    """Delete a task by its ID."""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        db.delete(task)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Error deleting task: {str(e)}")

# Example Usage
if __name__ == "__main__":
    # Create a new database session
    db_session = next(get_db_session())

    # Create a new task
    try:
        task = create_task(db_session, title="Finish project", description="Complete the project by the end of the week", priority=2)
        print(f"Created Task: {task}")
    except Exception as e:
        print(f"Error: {e}")

    # Retrieve the task
    try:
        retrieved_task = get_task_by_id(db_session, task.id)
        print(f"Retrieved Task: {retrieved_task}")
    except Exception as e:
        print(f"Error: {e}")

    # Update the task status
    try:
        updated_task = update_task_status(db_session, task.id, TaskStatus.COMPLETED)
        print(f"Updated Task: {updated_task}")
    except Exception as e:
        print(f"Error: {e}")

    # Delete the task
    try:
        delete_task(db_session, task.id)
        print(f"Task with ID {task.id} deleted.")
    except Exception as e:
        print(f"Error: {e}")
```

---

### Key Features:
1. **Task Model**: Defines the schema for the `tasks` table with fields for `id`, `title`, `description`, `status`, `priority`, `due_date`, `created_at`, and `updated_at`.
2. **CRUD Operations**: Includes functions to create, read, update, and delete tasks.
3. **Input Validation**: Ensures that inputs are valid before performing database operations.
4. **Error Handling**: Catches and handles SQLAlchemy errors and other exceptions.
5. **Database Connection Management**: Uses a session factory to manage database connections.

### How to Run:
1. Install SQLAlchemy: `pip install sqlalchemy`.
2. Save the code to a file (e.g., `task_manager.py`).
3. Run the script to see the example usage in action.
4. Replace `sqlite:///tasks.db` with your preferred database URL (e.g., PostgreSQL or MySQL) if needed.

This implementation is modular and can be extended to include more features such as user authentication, task filtering, or integration with a web framework like Flask or FastAPI.