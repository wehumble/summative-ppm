from typing import List, Dict, Any, Optional
from .user import User

class Project:
    """Represents a project owned by a user."""
    data_key = "projects"
    id_counter_key = "next_project_id"

    def __init__(self, id: int, title: str, description: str, due_date: str,
                 owner_id: int, task_ids: Optional[List[int]] = None):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner_id = owner_id
        self.task_ids = task_ids or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner_id": self.owner_id,
            "task_ids": self.task_ids
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Create a Project instance from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            owner_id=data["owner_id"],
            task_ids=data.get("task_ids", [])
        )

    @classmethod
    def create(cls, title: str, description: str, due_date: str,
               owner_name: str, data: Dict) -> "Project":
        """Create a new project. owner_name must exist. Returns created project."""
        owner = User.find_by_name(owner_name, data)
        if not owner:
            raise ValueError(f"User '{owner_name}' not found")
        projects = data.setdefault(cls.data_key, [])
        proj_id = data.get(cls.id_counter_key, 1)
        project = cls(proj_id, title, description, due_date, owner.id)
        projects.append(project.to_dict())
        data[cls.id_counter_key] = proj_id + 1

        # Update owner's project_ids
        owner.project_ids.append(proj_id)
        # Update the user in data
        for idx, u in enumerate(data[User.data_key]):
            if u["id"] == owner.id:
                data[User.data_key][idx] = owner.to_dict()
                break
        return project

    @classmethod
    def find_by_user(cls, user_name: str, data: Dict) -> List["Project"]:
        """Return all projects belonging to a user by name."""
        user = User.find_by_name(user_name, data)
        if not user:
            return []
        projects = []
        for p in data.get(cls.data_key, []):
            if p["owner_id"] == user.id:
                projects.append(cls.from_dict(p))
        return projects

    @classmethod
    def find_by_title(cls, title: str, data: Dict) -> Optional["Project"]:
        """Find a project by its title (assumes title is unique)."""
        for p in data.get(cls.data_key, []):
            if p["title"] == title:
                return cls.from_dict(p)
        return None

    @classmethod
    def find_by_id(cls, proj_id: int, data: Dict) -> Optional["Project"]:
        """Find a project by ID."""
        for p in data.get(cls.data_key, []):
            if p["id"] == proj_id:
                return cls.from_dict(p)
        return None

    def __repr__(self) -> str:
        return f"Project(id={self.id}, title='{self.title}')"