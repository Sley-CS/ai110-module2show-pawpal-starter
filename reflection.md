# PawPal+ Project Reflection

## 1. System Design
PawPal+ is a Streamlit app that helps a pet owner plan care tasks for their pet.

-User should be able to:
    1. Add their pet and set up basic info. Things like the pet’s name, type, and the 
        owner’s preferences.
 	2. Create or update care tasks. For example, adding a walk, changing feeding duration, 
        or adjusting a task’s priority.
 	3. Generate and view today’s care plan. A clear schedule that fits the owner’s time and  
        explains why each task was chosen.

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design started with four basic classes that match how a real pet‑care app works. The OWNER class holds the person’s info along with their pets and tasks. The PET class is just a simple record of each animal. The TASK class represents things the pet needs—like walks or feeding—and can update its own status. Finally, the SCHEDULER looks at everything the owner has going on and puts together a daily plan. Overall, the design keeps each class focused on one clear job, which makes the system easy to understand and build on.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing my initial class skeleton, I made several improvements based on AI feedback to better match my UML design and avoid future logic problems. I added real relationships between the classes so an Owner can actually store Pets and Tasks, and I introduced a Pet reference inside each Task to support multi‑pet scheduling. I also gave my method stubs minimal behavior like updating profiles, marking tasks done, and rescheduling so the classes behave more realistically. The Scheduler now validates that an owner has pets and tasks before generating a plan, keeping it read‑only as intended. These changes made my design cleaner, more consistent, and easier to extend, and the AI feedback helped me catch gaps I hadn’t noticed and strengthen the overall structure. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler only checks exact same-time matches for conflicts (for example, two tasks both at 08:00). It does not yet calculate overlap by duration. I accepted that tradeoff because it keeps the code easy to understand, and simple conflict warnings are enough for this project stage.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project

The Copilot features that helped most were iterative code generation for class methods, targeted test generation, and quick review feedback on relationship gaps. The most useful pattern was giving narrow prompts (for example, one scheduler feature at a time), then immediately running tests to validate behavior.

One suggestion I rejected was adding heavy optimization and complex validation layers too early. I chose to keep the scheduler lightweight and readable first, then add focused improvements like sorting, filtering, recurrence, and conflict warnings.

Using separate chat sessions helped me stay organized by phase. One session focused on UML and class structure, another on algorithm features, and another on testing and docs. That separation reduced context noise and made decisions clearer.

My biggest lesson was that I need to act as the lead architect, not just accept generated code. AI accelerated implementation, but I still had to define constraints, choose tradeoffs, and keep the design coherent across UI, domain logic, tests, and documentation.

