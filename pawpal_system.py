from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Pet:
	name: str
	species: str
	age: int

	def updateProfile(self) -> None:
		pass


@dataclass
class Task:
	title: str
	duration: int
	priority: int
	optional_time_window: Optional[str] = None

	def markDone(self) -> None:
		pass

	def reschedule(self) -> None:
		pass


class Owner:
	def __init__(self, name: str, daily_time_available: int, preferences: dict[str, Any]) -> None:
		self.name = name
		self.daily_time_available = daily_time_available
		self.preferences = preferences
		self.pets: list[Pet] = []
		self.tasks: list[Task] = []

	def addPet(self, pet: Pet) -> None:
		pass

	def addTask(self, task: Task) -> None:
		pass

	def getTasks(self) -> list[Task]:
		pass


class Scheduler:
	def buildPlan(self, owner: Owner) -> list[Task]:
		pass

	def getDueTasks(self, owner: Owner) -> list[Task]:
		pass
