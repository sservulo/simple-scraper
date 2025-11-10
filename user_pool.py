import csv
import random
from dataclasses import dataclass
from typing import List


@dataclass
class User:
    name: str
    email: str
    mobile: str
    address: str
    zipCode: str


class UserPool:
    def __init__(self, filepath: str = "data/mock_users.csv"):
        self.filepath = filepath
        self.users: List[User] = self._load_users()

    def _load_users(self) -> List[User]:
        """Load user data from a CSV file."""
        users = []
        with open(self.filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(
                    User(
                        name=row["name"],
                        email=row["email"],
                        mobile=row["mobile"],
                        address=row["address"],
                        zipCode=row["zipCode"],
                    )
                )
        return users

    def random_user(self) -> User:
        """Return a random User object."""
        return random.choice(self.users)
