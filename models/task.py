from typing import Dict, Any, Optional
from .project import Project
from .user import User

class Task:
    """Represents a task within a project."""
    data_key = "tasks"
    id_counter_key = "next_task_id"

    def __init__(self, id: int, title: str, status: str = "pending",
                 assigned_to: Optional[int] = None):
        self.id = id
        self.title = title
        self.status = status  # "pending" or "completed"
        self.assigned_to = assigned_to

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create a Task instance from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            status=data["status"],
            assigned_to=data.get("assigned_to")
        )

    @classmethod
    def create(cls, project_title: str, title: str, assigned_to_name: Optional[str],
               data: Dict) -> "Task":
        """Create a new task. project_title must exist; assigned_to_name optional."""
        project = Project.find_by_title(project_title, data)
        if not project:
            raise ValueError(f"Project '{project_title}' not found")
        assigned_user = None
        if assigned_to_name:
            assigned_user = User.find_by_name(assigned_to_name, data)
            if not assigned_user:
                raise ValueError(f"User '{assigned_to_name}' not found")
        tasks = data.setdefault(cls.data_key, [])
        task_id = data.get(cls.id_counter_key, 1)
        task = cls(task_id, title, assigned_to=assigned_user.id if assigned_user else None)
        tasks.append(task.to_dict())
        data[cls.id_counter_key] = task_id + 1

        # Update project's task_ids
        project.task_ids.append(task_id)
        for idx, p in enumerate(data[Project.data_key]):
            if p["id"] == project.id:
                data[Project.data_key][idx] = project.to_dict()
                break
        return task

    @classmethod
    def complete(cls, task_id: int, data: Dict) -> "Task":
        """Mark a task as completed by its ID."""
        for t in data.get(cls.data_key, []):
            if t["id"] == task_id:
                t["status"] = "completed"
                return cls.from_dict(t)
        raise ValueError(f"Task with ID {task_id} not found")

    @classmethod
    def find_by_id(cls, task_id: int, data: Dict) -> Optional["Task"]:
        """Find a task by ID."""
        for t in data.get(cls.data_key, []):
            if t["id"] == task_id:
                return cls.from_dict(t)
        return None

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"