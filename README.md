# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built. 
    

 ## Features

 - Owner and pet management with session-persistent owner state in Streamlit.
 - Task creation with duration, priority, due date/time, and optional recurrence.
 - Smart scheduling helpers for sorting and filtering task lists.
 - Lightweight conflict warnings when tasks share the same date/time.
 - Recurring task support that auto-creates the next daily/weekly occurrence on completion.

 ## Smarter Scheduling

 PawPal+ includes a few simple scheduling upgrades:

 - Sorting: tasks are ordered by time (`HH:MM`) so the day plan is easier to follow.
 - Filtering: tasks can be filtered by pet name and by status (pending or complete).
 - Recurring tasks: daily and weekly tasks automatically create the next occurrence when completed.
 - Conflict warnings: if two tasks land on the same date/time, the app shows a warning instead of failing.

 ## Testing PawPal+

 The pytest suite covers core scheduling behavior:

 - Task completion status updates.
 - Pet task assignment and task-count changes.
 - Time sorting ("HH:MM") behavior.
 - Filtering by pet and completion status.
 - Recurring task generation for daily tasks.
 - Conflict warning detection for overlapping task times.

 Run tests with:

 ```bash
 python -m pytest
 ```

## 📸 Demo

<a href="/course_images/ai110/Screenshot1_30-3-2026_134138_localhost.jpeg" target="_blank"><img src='/course_images/ai110/Screenshot1_30-3-2026_134138_localhost.jpeg' title='PawPal App' width='900' alt='PawPal App' class='center-block' /></a>

<a href="/course_images/ai110/Screenshot2_30-3-2026_134223_localhost.jpeg" target="_blank"><img src='/course_images/ai110/Screenshot2_30-3-2026_134223_localhost.jpeg' title='PawPal App' width='900' alt='PawPal App' class='center-block' /></a>

<a href="/course_images/ai110/Screenshot3_30-3-2026_13439_localhost.jpeg" target="_blank"><img src='/course_images/ai110/Screenshot3_30-3-2026_13439_localhost.jpeg' title='PawPal App' width='900' alt='PawPal App' class='center-block' /></a>

<a href="/course_images/ai110/Screenshot4_30-3-2026_134338_localhost.jpeg" target="_blank"><img src='/course_images/ai110/Screenshot4_30-3-2026_134338_localhost.jpeg' title='PawPal App' width='900' alt='PawPal App' class='center-block' /></a>

<a href="/course_images/ai110/Screenshot5_30-3-2026_13447_localhost.jpeg" target="_blank"><img src='/course_images/ai110/Screenshot5_30-3-2026_13447_localhost.jpeg' title='PawPal App' width='900' alt='PawPal App' class='center-block' /></a>

<a href="/course_images/ai110/PawPal+ Demo.pdf" target="_blank">Open PawPal+ Demo PDF</a>
  
