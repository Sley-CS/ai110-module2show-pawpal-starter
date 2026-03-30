from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_changes_status() -> None:
	task = Task(title="Feed", duration=10, priority=2)

	assert task.status == "pending"
	assert task.is_done is False

	task.mark_complete()

	assert task.status == "complete"
	assert task.is_done is True


def test_add_task_to_pet_increases_task_count() -> None:
	pet = Pet(name="Buddy", species="Dog", age=4)
	task = Task(title="Walk", duration=30, priority=3)

	starting_count = len(pet.tasks)
	pet.add_task(task)

	assert len(pet.tasks) == starting_count + 1
	assert pet.tasks[-1] is task
	assert task.pet is pet


def test_sort_by_time_orders_hhmm_values() -> None:
	scheduler = Scheduler()
	tasks = [
		Task(title="Play", duration=20, priority=1, optional_time_window="14:30"),
		Task(title="Feed", duration=10, priority=3, optional_time_window="07:00"),
		Task(title="Walk", duration=30, priority=2, optional_time_window="08:15"),
	]

	sorted_tasks = scheduler.sort_by_time(tasks)

	assert [task.title for task in sorted_tasks] == ["Feed", "Walk", "Play"]


def test_filter_tasks_by_pet_name_and_status() -> None:
	scheduler = Scheduler()
	buddy = Pet(name="Buddy", species="Dog", age=4)
	mochi = Pet(name="Mochi", species="Cat", age=2)
	t1 = Task(title="Walk", duration=30, priority=2, pet=buddy)
	t2 = Task(title="Feed", duration=10, priority=3, pet=mochi)
	t2.mark_complete()

	by_pet = scheduler.filter_tasks([t1, t2], pet_name="Buddy")
	completed = scheduler.filter_tasks([t1, t2], is_done=True)

	assert by_pet == [t1]
	assert completed == [t2]


def test_complete_task_creates_next_daily_occurrence() -> None:
	owner = Owner(name="Jordan", daily_time_available=120, preferences={})
	buddy = Pet(name="Buddy", species="Dog", age=4)
	owner.addPet(buddy)
	original = Task(
		title="Daily Walk",
		duration=25,
		priority=2,
		pet=buddy,
		optional_time_window="09:00",
		due_date=date.today(),
		recurrence="daily",
	)
	owner.addTask(original)
	scheduler = Scheduler()

	next_task = scheduler.complete_task(owner, original)

	assert original.is_done is True
	assert next_task is not None
	assert next_task.due_date == date.today() + timedelta(days=1)
	assert next_task.recurrence == "daily"
	assert next_task.is_done is False


def test_detect_conflicts_returns_warning_messages() -> None:
	scheduler = Scheduler()
	buddy = Pet(name="Buddy", species="Dog", age=4)
	tasks = [
		Task(title="Walk", duration=30, priority=2, pet=buddy, optional_time_window="08:00"),
		Task(title="Breakfast", duration=10, priority=3, pet=buddy, optional_time_window="08:00"),
	]

	warnings = scheduler.detect_conflicts(tasks)

	assert len(warnings) == 1
	assert "Conflict at 08:00" in warnings[0]
