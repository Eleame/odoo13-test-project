Project Management — Odoo 13

Requirements:

- Odoo 13.0 (Community or Enterprise)
- PostgreSQL 10+
- Python 3.6+
- Core modules: base, web, mail, hr

Installation:

1. **Clone the module into your Odoo addons path**

    ```bash
    git clone https://github.com/Eleame/odoo13-test-project.git /path/to/your/addons/project_management
    ```
    - For **Windows Installer**, use:
      ```
      ..\Odoo 13.0\server\addons\project_management
      ```
    - For Docker or custom setups, use your actual Odoo addons path.

2. **Ensure your `odoo.conf` includes the correct `addons_path`**

    Edit your `odoo.conf` and make sure the `addons_path` includes the folder where you placed `project_management`:
    ```
    addons_path = <other_paths>,/path/to/your/addons
    ```
    - Double-check for typos or duplicate paths!

3. **Install or update the module in your Odoo database**

    - For **Linux/Mac**:
      ```bash
      ./odoo-bin -d <your_db_name> -i project_management
      ```
    - For **Windows** (from the server folder):
      ```bash
      odoo-bin -d <your_db_name> -i project_management --stop-after-init
      ```
    - If you see a “Module not found” error, check the module path and spelling.
    - For permission errors, run the terminal as administrator.
    - If your database is empty, create a new database first via the Odoo web UI.

4. **Configure outgoing mail** (for e-mail notifications):

    Go to **Settings → Technical → Outgoing Mail Servers**. Add your SMTP server and credentials, then click *Test Connection*.


Features:

| Area        | What you get |
|-------------|-------------------------------------------------------------|
| **Data**    | Projects, workflow stages (Created → In Progress → Done), tasks with assigned employees, deadlines, and priorities |
| **UI**      | Menus for Projects/Tasks, tree, form, and **Kanban** views with drag & drop |
| **E-mail**  | Two templates: on stage change (or new task) and on overdue |
| **Reports** | Printable PDF Task Status (QWeb report) |
| **Cron**    | Daily reminder for overdue tasks (activity scheduled) |
| **ACL**     | Two groups: *Project User* (see own only), *Project Manager* (see all, can manage views) |
| **Tests**   | Unit-test for e-mail template rendering and cron job |


Usage:

- Go to **Projects → Projects → Create** — Create a project.
- Inside a project, go to **Tasks → Create** — fill in all required fields.
- **Drag & drop tasks** between Kanban columns: green = done, red = overdue.
- For reports — use **Print → Task Status (PDF)** inside any project.
- Use the filter wizard: **Reporting ▸ Task Filter Wizard** for advanced search/export.
