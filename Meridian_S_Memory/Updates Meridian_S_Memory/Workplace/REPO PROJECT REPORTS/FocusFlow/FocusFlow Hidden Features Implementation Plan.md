---
modified: 2026-04-15T16:57:11+03:00
---
                                      
                                                                                     
 Context                                                

 The application has several business logic features implemented in taskService and
 the Task data model that are not yet exposed in the UI. This plan aims to surface
 these "hidden features" to improve the user experience and make the app a more
 complete productivity tool.

 Recommended Approach

 1. Due Date & Category Support

 - UI Additions:
   - Add an <input type="date"> for dueDate in the "Add New Task" form
 (pages/index.tsx) and in the TaskCard edit mode (components/TaskCard.tsx).
   - Implement simple text-based categories by adding a "Category" text input to the
  task form and edit mode.
 - State Updates:
   - Update the newTask state in Home to include dueDate and categoryId.

 2. Focus Metrics Visibility

 - TaskCard Enhancements:
   - Add a "Focus Stats" section to the card-meta area of components/TaskCard.tsx.
   - Display pomodorosCompleted (with a 🍅 icon) and totalFocusTime (with a ⏱️ 
 icon), formatted as HH:mm.
 - TaskList Update:
   - Ensure the TaskItem in the list view also displays these metrics for
 consistency.

 3. Data Portability (Export/Import)

 - Header Controls:
   - Add "Export" and "Export" buttons (Wait, let me fix that: "Export" and
 "Import") to the header in pages/index.tsx.
   - Use a hidden file input for imports.
 - Implementation:
   - Export: Call taskService.exportTasks(tasks) and trigger a browser download of
 the resulting JSON.
   - Import: Read the JSON file, call taskService.importTasks(data), and update the
 application state.

 4. Advanced Sorting

 - Filter Updates:
   - Add a "Sort By" dropdown in the filters section of pages/index.tsx with options
  for "Created Date", "Priority", and "Status".
 - Logic Integration:
   - Update the task rendering pipeline in Home to: tasks $\rightarrow$ filterTasks
 $\rightarrow$ sortTasks $\rightarrow$ TaskList.

 Critical Files

 - pages/index.tsx
 - components/TaskCard.tsx
 - components/TaskList.tsx
 - utils/tasks.ts

 Verification Plan

 1. Due Date & Category: Create a task with a due date and category $\ category
 $\rightarrow$ Verify display on card $\rightarrow$ Edit and verify update.
 2. Focus Metrics: Complete a Pomodoro session $\rightarrow$ Verify
 pomodorosCompleted and totalFocusTime increment on the TaskCard.
 3. Sorting: Create tasks with mixed priorities $\rightarrow$ Sort by "Priority"
 $\rightarrow$ Verify the order changes.
 4. Portability: Export current tasks $\rightarrow$ Clear local storage
 $\rightarrow$ Import the JSON file $\rightarrow$ Verify tasks are restored.