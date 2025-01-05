from fastapi import HTTPException, Depends
from app.models import Project
from app.auth import get_current_user

def create_project(name: str, description: str, user=Depends(get_current_user)):
    if user['role'] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    project = Project(name=name, description=description)
    project.save()
    return project

def get_projects():
    return list(Project.objects.all())
