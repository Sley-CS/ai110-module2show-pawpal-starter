import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value="Jordan")
daily_time = st.number_input("Daily time available (minutes)", min_value=30, max_value=600, value=120)

# Session-state vault pattern: create once, then reuse on every rerun.
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(
        name=owner_name,
        daily_time_available=int(daily_time),
        preferences={},
    )
if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = Scheduler()

owner = st.session_state["owner"]
scheduler = st.session_state["scheduler"]
owner.name = owner_name
owner.daily_time_available = int(daily_time)

st.caption(f"Active owner in session: {owner.name}")

st.markdown("### Add Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=2)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    existing_names = {pet.name for pet in owner.pets}
    if pet_name in existing_names:
        st.warning(f"Pet '{pet_name}' already exists.")
    else:
        owner.addPet(Pet(name=pet_name, species=species, age=int(pet_age)))
        st.success(f"Added pet: {pet_name}")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": pet.name, "species": pet.species, "age": pet.age} for pet in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Add Task")
priority_map = {"low": 1, "medium": 2, "high": 3}
recurrence_options = ["none", "daily", "weekly"]

with st.form("add_task_form", clear_on_submit=True):
    task_title = st.text_input("Task title", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    time_window = st.text_input("Time (HH:MM)", value="08:00")
    recurrence = st.selectbox("Recurrence", recurrence_options)
    pet_options = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Assign to pet", pet_options) if pet_options else None
    add_task_submitted = st.form_submit_button("Add task")

if add_task_submitted:
    selected_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), None)
    new_task = Task(
        title=task_title,
        duration=int(duration),
        priority=priority_map[priority_label],
        pet=selected_pet,
        optional_time_window=time_window,
        due_date=date.today(),
        recurrence=None if recurrence == "none" else recurrence,
    )
    owner.addTask(new_task)
    st.success(f"Added task: {task_title}")

st.divider()

st.subheader("Task Views")
pet_filter_options = ["all"] + [pet.name for pet in owner.pets]
selected_pet_filter = st.selectbox("Filter by pet", pet_filter_options)
status_filter = st.selectbox("Filter by status", ["all", "pending", "complete"])

all_tasks = owner.getTasks()
sorted_tasks = scheduler.sort_by_time(all_tasks)
filtered_tasks = scheduler.filter_tasks(
    sorted_tasks,
    pet_name=None if selected_pet_filter == "all" else selected_pet_filter,
    is_done=None if status_filter == "all" else (status_filter == "complete"),
)

if filtered_tasks:
    rows = []
    for task in filtered_tasks:
        rows.append(
            {
                "title": task.title,
                "pet": task.pet.name if task.pet else "General",
                "time": task.optional_time_window or "Anytime",
                "duration": task.duration,
                "priority": task.priority,
                "status": task.status,
                "recurrence": task.recurrence or "none",
                "due_date": task.due_date.isoformat(),
            }
        )
    st.table(rows)
else:
    st.info("No tasks match your current filters.")

conflicts = scheduler.detect_conflicts(filtered_tasks)
if conflicts:
    for warning_msg in conflicts:
        st.warning(warning_msg)
else:
    st.success("No schedule conflicts detected for this view.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate today's plan from your owner data.")

if st.button("Generate schedule"):
    try:
        today_plan = scheduler.sort_by_time(scheduler.getDueTasks(owner))
        if today_plan:
            st.success("Today's schedule generated.")
            st.table(
                [
                    {
                        "time": task.optional_time_window or "Anytime",
                        "task": task.title,
                        "pet": task.pet.name if task.pet else "General",
                        "duration": task.duration,
                        "priority": task.priority,
                    }
                    for task in today_plan
                ]
            )
        else:
            st.info("No tasks due today.")
    except ValueError as err:
        st.warning(str(err))

st.subheader("Complete a Task")
pending_tasks = [task for task in owner.getTasks() if not task.is_done]
if pending_tasks:
    pending_labels = [
        f"{task.title} ({task.optional_time_window or 'Anytime'})"
        for task in scheduler.sort_by_time(pending_tasks)
    ]
    selected_label = st.selectbox("Pending tasks", pending_labels)
    if st.button("Mark selected task complete"):
        selected_task = next(task for task in pending_tasks if f"{task.title} ({task.optional_time_window or 'Anytime'})" == selected_label)
        next_task = scheduler.complete_task(owner, selected_task)
        if next_task is not None:
            st.success(
                f"Marked complete and created next {next_task.recurrence} occurrence for {next_task.due_date.isoformat()}."
            )
        else:
            st.success("Task marked complete.")
else:
    st.info("No pending tasks to complete.")
