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

	owner.addTask(Task(title="Morning Walk", duration=30, priority=3, pet=buddy, optional_time_window="08:00"))
	owner.addTask(Task(title="Feed Breakfast", duration=10, priority=5, pet=whiskers, optional_time_window="07:30"))
	owner.addTask(Task(title="Evening Play", duration=20, priority=2, pet=buddy, optional_time_window="18:00"))

	scheduler = Scheduler()
	planned_tasks = scheduler.buildPlan(owner)

	print("Today's Schedule")
	print("-" * 24)
	for index, task in enumerate(planned_tasks, start=1):
		pet_name = task.pet.name if task.pet else "General"
		time_slot = task.optional_time_window or "Anytime"
		print(f"{index}. {time_slot} | {task.title} ({pet_name}) - {task.duration} min")


if __name__ == "__main__":
	print_todays_schedule()
