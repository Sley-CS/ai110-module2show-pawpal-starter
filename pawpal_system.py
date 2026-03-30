from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Pet:
	name: str
	species: str
	age: int
	tasks: list["Task"] = field(default_factory=list)

	def updateProfile(
		self,
		name: Optional[str] = None,
		species: Optional[str] = None,
		age: Optional[int] = None,
	) -> None:
		"""Update pet profile fields when new values are provided."""
		if name is not None:
			self.name = name
		if species is not None:
			self.species = species
		if age is not None:
			self.age = age

	def add_task(self, task: "Task") -> None:
		"""Attach a task to this pet and set the back-reference."""
		task.pet = self
		self.tasks.append(task)


@dataclass
class Task:
	title: str
	duration: int
	priority: int
	pet: Optional[Pet] = None
	optional_time_window: Optional[str] = None
	is_done: bool = False
	status: str = "pending"

	def mark_complete(self) -> None:
		"""Mark this task as complete and update its status label."""
		self.is_done = True
		self.status = "complete"

	def markDone(self) -> None:
		"""Provide camelCase compatibility for completion behavior."""
		self.mark_complete()

	def reschedule(self, new_time_window: Optional[str]) -> None:
		"""Set or clear the optional time window for this task."""
		self.optional_time_window = new_time_window


class Owner:
	def __init__(self, name: str, daily_time_available: int, preferences: dict[str, Any]) -> None:
		"""Initialize an owner with preferences and empty pet/task lists."""
		self.name = name
		self.daily_time_available = daily_time_available
		self.preferences = preferences
		self.pets: list[Pet] = []
		self.tasks: list[Task] = []

	def addPet(self, pet: Pet) -> None:
		"""Add a pet to this owner."""
		self.pets.append(pet)

	def addTask(self, task: Task) -> None:
		"""Add a task to this owner."""
		self.tasks.append(task)

	def getTasks(self) -> list[Task]:
		"""Return a shallow copy of the owner's task list."""
		return list(self.tasks)


class Scheduler:
	def buildPlan(self, owner: Owner) -> list[Task]:
		"""Return pending tasks sorted by priority and shorter duration."""
		if not owner.pets:
			raise ValueError("Owner must have at least one pet.")
		if not owner.tasks:
			raise ValueError("Owner must have at least one task.")

		# Read-only planning view: prioritize high-priority, shorter tasks first.
		pending_tasks = [task for task in owner.tasks if not task.is_done]
		return sorted(pending_tasks, key=lambda task: (-task.priority, task.duration))

	def getDueTasks(self, owner: Owner) -> list[Task]:
		"""Return all tasks that are not yet marked complete."""
		if not owner.pets:
			raise ValueError("Owner must have at least one pet.")
		if not owner.tasks:
			raise ValueError("Owner must have at least one task.")

		return [task for task in owner.tasks if not task.is_done]
