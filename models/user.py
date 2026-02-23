import json
from typing import List, Dict, Any, Optional

class User:
    """Represents a user in the system."""
    data_key = "users"
    id_counter_key = "next_user_id"

    def __init__(self, id: int, name: str, email: str, project_ids: Optional[List[int]] = None):
        self.id = id
        self.name = name
        self.email = email
        self.project_ids = project_ids or []

    def to_dict(self) -> Dict[str, Any]:
        """Convert user instance to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "project_ids": self.project_ids
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create a User instance from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            project_ids=data.get("project_ids", [])
        )

    @classmethod
    def create(cls, name: str, email: str, data: Dict) -> "User":
        """Create a new user, add to data dictionary, and return the user."""
        users = data.setdefault(cls.data_key, [])
        user_id = data.get(cls.id_counter_key, 1)
        user = cls(user_id, name, email)
        users.append(user.to_dict())
        data[cls.id_counter_key] = user_id + 1
        return user

    @classmethod
    def find_by_name(cls, name: str, data: Dict) -> Optional["User"]:
        """Find a user by name. Returns User object or None."""
        for u in data.get(cls.data_key, []):
            if u["name"] == name:
                return cls.from_dict(u)
        return None

    @classmethod
    def find_by_id(cls, user_id: int, data: Dict) -> Optional["User"]:
        """Find a user by ID. Returns User object or None."""
        for u in data.get(cls.data_key, []):
            if u["id"] == user_id:
                return cls.from_dict(u)
        return None

    def __repr__(self) -> str:
        return f"User(id={self.id}, name='{self.name}')"