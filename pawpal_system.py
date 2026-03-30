from dataclasses import dataclass, field
from datetime import date, timedelta
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
		if task not in self.tasks:
			self.tasks.append(task)


@dataclass
class Task:
	title: str
	duration: int
	priority: int
	pet: Optional[Pet] = None
	optional_time_window: Optional[str] = None
	due_date: date = field(default_factory=date.today)
	recurrence: Optional[str] = None
	is_done: bool = False
	status: str = "pending"

	def mark_complete(self) -> Optional["Task"]:
		"""Mark complete and return the next recurring task if applicable."""
		self.is_done = True
		self.status = "complete"

		if self.recurrence == "daily":
			return self._next_occurrence(days=1)
		if self.recurrence == "weekly":
			return self._next_occurrence(days=7)
		return None

	def markDone(self) -> None:
		"""Provide camelCase compatibility for completion behavior."""
		self.mark_complete()

	def reschedule(self, new_time_window: Optional[str]) -> None:
		"""Set or clear the optional time window for this task."""
		self.optional_time_window = new_time_window

	def _next_occurrence(self, days: int) -> "Task":
		"""Create the next recurring task occurrence after a date offset."""
		return Task(
			title=self.title,
			duration=self.duration,
			priority=self.priority,
			pet=self.pet,
			optional_time_window=self.optional_time_window,
			due_date=self.due_date + timedelta(days=days),
			recurrence=self.recurrence,
		)


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
		if pet not in self.pets:
			self.pets.append(pet)

	def addTask(self, task: Task) -> None:
		"""Add a task to this owner."""
		self.tasks.append(task)
		if task.pet is not None:
			task.pet.add_task(task)

	def getTasks(self) -> list[Task]:
		"""Return a shallow copy of the owner's task list."""
		return list(self.tasks)


class Scheduler:
	def buildPlan(self, owner: Owner) -> list[Task]:
		"""Return pending tasks sorted by time, priority, and shorter duration."""
		if not owner.pets:
			raise ValueError("Owner must have at least one pet.")
		if not owner.tasks:
			raise ValueError("Owner must have at least one task.")

		pending_tasks = [task for task in owner.tasks if not task.is_done]
		time_sorted = self.sort_by_time(pending_tasks)
		return sorted(time_sorted, key=lambda task: (-task.priority, task.duration))

	def getDueTasks(self, owner: Owner) -> list[Task]:
		"""Return pending tasks due today."""
		if not owner.pets:
			raise ValueError("Owner must have at least one pet.")
		if not owner.tasks:
			raise ValueError("Owner must have at least one task.")

		today = date.today()
		return [task for task in owner.tasks if (not task.is_done) and task.due_date == today]

	def sort_by_time(self, tasks: list[Task]) -> list[Task]:
		"""Sort tasks by HH:MM time strings using a lambda key."""
		return sorted(tasks, key=lambda task: self._time_to_minutes(task.optional_time_window))

	def filter_tasks(
		self,
		tasks: list[Task],
		pet_name: Optional[str] = None,
		is_done: Optional[bool] = None,
	) -> list[Task]:
		"""Filter tasks by pet name and/or completion state."""
		filtered = tasks
		if pet_name:
			filtered = [task for task in filtered if task.pet is not None and task.pet.name == pet_name]
		if is_done is not None:
			filtered = [task for task in filtered if task.is_done == is_done]
		return filtered

	def complete_task(self, owner: Owner, task: Task) -> Optional[Task]:
		"""Complete a task and append its next recurring occurrence if created."""
		next_task = task.mark_complete()
		if next_task is not None:
			owner.addTask(next_task)
		return next_task

	def detect_conflicts(self, tasks: list[Task]) -> list[str]:
		"""Return warning strings for tasks that share the same date and time."""
		buckets: dict[tuple[date, str], list[Task]] = {}
		for task in tasks:
			time_label = task.optional_time_window or "unscheduled"
			if time_label == "unscheduled":
				continue
			key = (task.due_date, time_label)
			buckets.setdefault(key, []).append(task)

		warnings: list[str] = []
		for (due, time_label), grouped in buckets.items():
			if len(grouped) > 1:
				titles = ", ".join(task.title for task in grouped)
				warnings.append(f"Conflict at {time_label} on {due.isoformat()}: {titles}")
		return warnings

	def _time_to_minutes(self, hhmm: Optional[str]) -> int:
		"""Convert HH:MM to minutes, placing missing/invalid values at the end."""
		if not hhmm:
			return 24 * 60 + 1
		parts = hhmm.split(":")
		if len(parts) != 2:
			return 24 * 60 + 1
		try:
			hours = int(parts[0])
			minutes = int(parts[1])
		except ValueError:
			return 24 * 60 + 1
		if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
			return 24 * 60 + 1
		return hours * 60 + minutes
