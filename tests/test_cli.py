import pytest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO
from main import add_user, add_project, add_task, complete_task, list_projects, list_users

# We'll mock load_data, save_data, and console.print for isolation.

@pytest.fixture
def mock_data():
    return {
        "users": [],
        "projects": [],
        "tasks": [],
        "next_user_id": 1,
        "next_project_id": 1,
        "next_task_id": 1
    }

@patch("main.save_data")
@patch("main.load_data")
def test_add_user(mock_load, mock_save, mock_data):
    mock_load.return_value = mock_data
    mock_save.return_value = None

    args = MagicMock()
    args.name = "Alice"
    args.email = "alice@example.com"

    with patch("main.console.print") as mock_print:
        add_user(args)

    mock_load.assert_called_once()
    mock_save.assert_called_once()
    mock_print.assert_called_with("[green]User 'Alice' added with ID 1.[/green]")
    assert len(mock_data["users"]) == 1
    assert mock_data["users"][0]["name"] == "Alice"

@patch("main.save_data")
@patch("main.load_data")
def test_add_project(mock_load, mock_save, mock_data):
    # Pre-create a user
    from models.user import User
    User.create("Bob", "bob@example.com", mock_data)

    mock_load.return_value = mock_data
    mock_save.return_value = None

    args = MagicMock()
    args.user = "Bob"
    args.title = "Test Project"
    args.description = "Some desc"
    args.due_date = "2025-07-01"

    with patch("main.console.print") as mock_print:
        add_project(args)

    mock_save.assert_called_once()
    mock_print.assert_called_with("[green]Project 'Test Project' added with ID 1 for user 'Bob'.[/green]")
    assert len(mock_data["projects"]) == 1
    assert mock_data["projects"][0]["owner_id"] == 1

@patch("main.save_data")
@patch("main.load_data")
def test_add_task(mock_load, mock_save, mock_data):
    # Pre-create user and project
    from models.user import User
    from models.project import Project
    User.create("Charlie", "c@example.com", mock_data)
    Project.create("P1", "desc", "2025-07-01", "Charlie", mock_data)

    mock_load.return_value = mock_data
    mock_save.return_value = None

    args = MagicMock()
    args.project = "P1"
    args.title = "New Task"
    args.assigned_to = "Charlie"

    with patch("main.console.print") as mock_print:
        add_task(args)

    mock_save.assert_called_once()
    assert "Task 'New Task' added to project 'P1' with ID 1. Assigned to 'Charlie'." in mock_print.call_args[0][0]
    assert len(mock_data["tasks"]) == 1
    assert mock_data["tasks"][0]["assigned_to"] == 1

@patch("main.save_data")
@patch("main.load_data")
def test_complete_task(mock_load, mock_save, mock_data):
    # Pre-create user, project, task
    from models.user import User
    from models.project import Project
    from models.task import Task
    User.create("Dave", "d@example.com", mock_data)
    Project.create("P1", "desc", "2025-07-01", "Dave", mock_data)
    Task.create("P1", "Task 1", None, mock_data)

    mock_load.return_value = mock_data
    mock_save.return_value = None

    args = MagicMock()
    args.task_id = 1

    with patch("main.console.print") as mock_print:
        complete_task(args)

    mock_save.assert_called_once()
    mock_print.assert_called_with("[green]Task 'Task 1' (ID 1) marked as completed.[/green]")
    assert mock_data["tasks"][0]["status"] == "completed"