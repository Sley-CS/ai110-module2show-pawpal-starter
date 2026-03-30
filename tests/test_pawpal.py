from pawpal_system import Pet, Task


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
