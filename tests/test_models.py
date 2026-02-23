import pytest
import json
from models.user import User
from models.project import Project
from models.task import Task

@pytest.fixture
def sample_data():
    """Provide a fresh data structure for each test."""
    return {
        "users": [],
        "projects": [],
        "tasks": [],
        "next_user_id": 1,
        "next_project_id": 1,
        "next_task_id": 1
    }

def test_create_user(sample_data):
    user = User.create("Alex", "alex@example.com", sample_data)
    assert user.id == 1
    assert user.name == "Alex"
    assert user.email == "alex@example.com"
    assert user.project_ids == []
    assert sample_data["next_user_id"] == 2
    assert len(sample_data["users"]) == 1

def test_find_user_by_name(sample_data):
    User.create("Alex", "a@b.com", sample_data)
    found = User.find_by_name("Alex", sample_data)
    assert found is not None
    assert found.email == "a@b.com"
    assert found.id == 1

def test_create_project(sample_data):
    User.create("Alex", "a@b.com", sample_data)
    project = Project.create("New Project", "Description", "2025-06-01", "Alex", sample_data)
    assert project.id == 1
    assert project.title == "New Project"
    assert project.owner_id == 1
    assert project.due_date == "2025-06-01"
    # Check owner's project list updated
    owner = User.find_by_id(1, sample_data)
    assert 1 in owner.project_ids

def test_find_project_by_title(sample_data):
    User.create("Alex", "a@b.com", sample_data)
    Project.create("P1", "desc", "2025-06-01", "Alex", sample_data)
    found = Project.find_by_title("P1", sample_data)
    assert found is not None
    assert found.id == 1

def test_create_task(sample_data):
    User.create("Alex", "a@b.com", sample_data)
    Project.create("P1", "desc", "2025-06-01", "Alex", sample_data)
    task = Task.create("P1", "Do something", "Alex", sample_data)
    assert task.id == 1
    assert task.title == "Do something"
    assert task.status == "pending"
    assert task.assigned_to == 1
    # Check project's task list
    proj = Project.find_by_id(1, sample_data)
    assert 1 in proj.task_ids

def test_complete_task(sample_data):
    User.create("Alex", "a@b.com", sample_data)
    Project.create("P1", "desc", "2025-06-01", "Alex", sample_data)
    Task.create("P1", "Do something", None, sample_data)
    task = Task.complete(1, sample_data)
    assert task.status == "completed"
    # Verify in data
    task_from_data = Task.find_by_id(1, sample_data)
    assert task_from_data.status == "completed"