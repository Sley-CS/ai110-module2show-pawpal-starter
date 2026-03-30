from pawpal_system import Owner, Pet, Scheduler, Task


def print_todays_schedule() -> None:
	owner = Owner(
		name="Wes",
		daily_time_available=180,
		preferences={"preferred_window": "morning"},
	)

	buddy = Pet(name="Buddy", species="Dog", age=4)
	whiskers = Pet(name="Whiskers", species="Cat", age=2)
	owner.addPet(buddy)
	owner.addPet(whiskers)

	# Added out of time order on purpose to verify sorting.
	owner.addTask(Task(title="Evening Play", duration=20, priority=2, pet=buddy, optional_time_window="18:00"))
	owner.addTask(Task(title="Morning Walk", duration=30, priority=3, pet=buddy, optional_time_window="08:00"))
	owner.addTask(Task(title="Feed Breakfast", duration=10, priority=5, pet=whiskers, optional_time_window="07:30"))
	owner.addTask(
		Task(
			title="Daily Medication",
			duration=5,
			priority=5,
			pet=whiskers,
			optional_time_window="08:00",
			recurrence="daily",
		)
	)

	scheduler = Scheduler()
	sorted_tasks = scheduler.sort_by_time(owner.getTasks())
	buddy_tasks = scheduler.filter_tasks(sorted_tasks, pet_name="Buddy", is_done=False)
	conflicts = scheduler.detect_conflicts(sorted_tasks)

	print("Today's Schedule")
	print("-" * 24)
	for index, task in enumerate(sorted_tasks, start=1):
		pet_name = task.pet.name if task.pet else "General"
		time_slot = task.optional_time_window or "Anytime"
		print(f"{index}. {time_slot} | {task.title} ({pet_name}) - {task.duration} min")

	print("\nBuddy's Pending Tasks")
	print("-" * 24)
	for task in buddy_tasks:
		time_slot = task.optional_time_window or "Anytime"
		print(f"- {time_slot} | {task.title}")

	if conflicts:
		print("\nConflict Warnings")
		print("-" * 24)
		for warning in conflicts:
			print(f"WARNING: {warning}")

	# Recurrence demo: complete a daily task and show the next instance.
	daily_task = next(task for task in owner.getTasks() if task.recurrence == "daily")
	next_task = scheduler.complete_task(owner, daily_task)
	if next_task is not None:
		print("\nRecurring Task Created")
		print("-" * 24)
		print(f"{next_task.title} scheduled for {next_task.due_date.isoformat()}")


if __name__ == "__main__":
	print_todays_schedule()
