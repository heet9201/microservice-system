from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import engine, Base, get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse, ValidatedUser
from dependencies import validate_token_with_auth_service, require_admin
from middleware import CustomHeaderMiddleware, SecurityMiddleware
from notification_client import send_notification
from config import settings

Base.metadata.create_all(bind=engine)

# MVC pattern
app = FastAPI(title="Task Service")

app.add_middleware(SecurityMiddleware)
app.add_middleware(CustomHeaderMiddleware)


@app.get("/")
def root():
    """Root endpoint"""
    return {"service": "Task Service", "status": "running"}


@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: ValidatedUser = Depends(validate_token_with_auth_service)
):
    """Create new task"""
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user.user_id,
        status=task_data.status
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # Send notification to Notification Service
    send_notification(
        user_id=current_user.user_id,
        message=f"New task created: {new_task.title}"
    )
    
    return new_task


@app.get("/tasks/", response_model=List[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: ValidatedUser = Depends(validate_token_with_auth_service)
):
    """Get all tasks or user tasks"""
    if current_user.role == "admin":
        # Admin can see all tasks
        tasks = db.query(Task).all()
    else:
        # User can only see their own tasks
        tasks = db.query(Task).filter(Task.user_id == current_user.user_id).all()
    
    return tasks


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: ValidatedUser = Depends(validate_token_with_auth_service)
):
    """Update task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # User can only update their own tasks
    if current_user.role != "admin" and task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own tasks"
        )
    
    task.status = task_update.status
    db.commit()
    db.refresh(task)
    
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: ValidatedUser = Depends(validate_token_with_auth_service),
    _: ValidatedUser = Depends(require_admin)
):
    """
    Delete task (Admin only)
    Design Pattern: Dependency Injection with chained dependencies for admin check
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(task)
    db.commit()
    
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.TASK_SERVICE_PORT)
