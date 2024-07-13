## Views

This application is organized into five main sections, referred to as Layers:

1. **Start**: Includes the landing view, and forms needed to log in and sign up.
2. **User**: Includes a dashboard and forms needed to join / create workspaces.
3. **Work**: Includes a members view, an exams view for viewing all exams, and settings necessary for class administration.
4. **Manage**: Includes a view for students to enter an exam, and management views for teachers to oversee and manage exam settings and sessions.
5. **Exam**: This is where students actually complete questions, and teachers view that in real-time.

Each layer has it's very own sidebar layout. You can read about that in the [neighboring README](../layouts/README.md) over at ../layouts.

### Naming convention

The following naming convention applies to all views:

```text
(Layer) (Action) View.vue
```

- **Layer** is the layer the view is on
- **Action** is a single word that defines the function of the view

**Note that the `Layer` and `Action` values are not necessarily connected. For example, `WorkCreateView.vue` might suggest it creates a workspace, but it actually allows for the creation of an exam within the work layer.**

### Directory stucture

Make sure to update this as things get added and renamed!

```py
client/src/views
│   README.md # This file
│
├───exam
│       ExamAccessView.vue # Wiew exam in real-time (work_admins only)
│       ExamWriteView.vue # Complete an exam (students only)
│
├───manage
│       ManageQuestionsView.vue # Manage an exam's questions (work_admins only)
│       ManageSessionsView.vue # Manage an exam's sessions (work_admins only)
│       ManageSettingsView.vue # Manage & configure an exam's settings (work_admins only)
│       ManageStartView.vue # Start an exam session (students only)
│
├───start
│       StartHomeView.vue # Landing view. Sells users the product.
│       StartLoginView.vue # Allows for login.
│       StartSignupView.vue # Allows for signup (access code required)
│
├───user
│       UserCreateView.vue # Allows to create a workspace (access code required)
│       UserDashboardView.vue # View the dashboard with all your classes!
│       UserJoinView.vue # Allows to join a workspace.
│
└───work
        WorkCreateView.vue # Allows to create an exam (work_admins only)
        WorkExamsView.vue # Allows to view exams
        WorkMembersView.vue # Allows to view members
        WorkSettingsView.vue # Allows to configure a workspace's settings. (work_admins only)
```
