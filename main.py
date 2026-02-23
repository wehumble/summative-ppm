#!/usr/bin/env python3
"""
Project Management CLI Tool
Entry point for the command-line interface.
"""
import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from models import User, Project, Task
from utils import load_data, save_data, parse_date, validate_email

console = Console()


# Command Handlers

def add_user(args):
    """Handle add-user command."""
    data = load_data()
    try:
        validate_email(args.email)
        user = User.create(args.name, args.email, data)
        save_data(data)
        console.print(f"[green]User '{user.name}' added with ID {user.id}.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

def add_project(args):
    """Handle add-project command."""
    data = load_data()
    try:
        due_date = parse_date(args.due_date)
        project = Project.create(args.title, args.description, due_date, args.user, data)
        save_data(data)
        console.print(f"[green]Project '{project.title}' added with ID {project.id} for user '{args.user}'.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

def add_task(args):
    """Handle add-task command."""
    data = load_data()
    try:
        task = Task.create(args.project, args.title, args.assigned_to, data)
        save_data(data)
        msg = f"Task '{task.title}' added to project '{args.project}' with ID {task.id}."
        if args.assigned_to:
            msg += f" Assigned to '{args.assigned_to}'."
        console.print(f"[green]{msg}[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

def complete_task(args):
    """Handle complete-task command."""
    data = load_data()
    try:
        task = Task.complete(args.task_id, data)
        save_data(data)
        console.print(f"[green]Task '{task.title}' (ID {task.id}) marked as completed.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

def list_projects(args):
    """Handle list-projects command."""
    data = load_data()
    if args.user:
        projects = Project.find_by_user(args.user, data)
        if not projects:
            console.print(f"[yellow]No projects found for user '{args.user}'.[/yellow]")
            return
        title = f"Projects for {args.user}"
    else:
        projects = [Project.from_dict(p) for p in data.get(Project.data_key, [])]
        if not projects:
            console.print("[yellow]No projects found.[/yellow]")
            return
        title = "All Projects"

    table = Table(title=title)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Description")
    table.add_column("Due Date", justify="center")
    table.add_column("Tasks", justify="right")

    for proj in projects:
        task_count = len(proj.task_ids)
        table.add_row(
            str(proj.id),
            proj.title,
            proj.description[:30] + "..." if len(proj.description) > 30 else proj.description,
            proj.due_date,
            str(task_count)
        )
    console.print(table)

def list_users(args):
    """Handle list-users command."""
    data = load_data()
    users = [User.from_dict(u) for u in data.get(User.data_key, [])]
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Users")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Projects", justify="right")

    for user in users:
        table.add_row(str(user.id), user.name, user.email, str(len(user.project_ids)))
    console.print(table)


# Main CLI setup

def main():
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  add-user --name "Alex" --email "alex@example.com"
  add-project --user "Alex" --title "CLI Tool" --due-date "2025-06-01"
  add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alex"
  complete-task --task-id 1
  list-projects --user "Alex"
  list-users
        """
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")

    # add-user
    pu = subparsers.add_parser("add-user", help="Add a new user")
    pu.add_argument("--name", required=True, help="User's full name")
    pu.add_argument("--email", required=True, help="User's email address")

    # add-project
    pp = subparsers.add_parser("add-project", help="Add a new project")
    pp.add_argument("--user", required=True, help="Name of the project owner")
    pp.add_argument("--title", required=True, help="Project title")
    pp.add_argument("--description", default="", help="Project description")
    pp.add_argument("--due-date", required=True, help="Due date (e.g., 2025-06-01)")

    # add-task
    pt = subparsers.add_parser("add-task", help="Add a task to a project")
    pt.add_argument("--project", required=True, help="Project title")
    pt.add_argument("--title", required=True, help="Task title")
    pt.add_argument("--assigned-to", help="Name of user to assign (optional)")

    # complete-task
    pc = subparsers.add_parser("complete-task", help="Mark a task as complete")
    pc.add_argument("--task-id", type=int, required=True, help="ID of the task")

    # list-projects
    pl = subparsers.add_parser("list-projects", help="List projects (optionally filtered by user)")
    pl.add_argument("--user", help="Filter by user name")

    # list-users
    subparsers.add_parser("list-users", help="List all users")

    args = parser.parse_args()

    # Dispatch to appropriate handler
    if args.command == "add-user":
        add_user(args)
    elif args.command == "add-project":
        add_project(args)
    elif args.command == "add-task":
        add_task(args)
    elif args.command == "complete-task":
        complete_task(args)
    elif args.command == "list-projects":
        list_projects(args)
    elif args.command == "list-users":
        list_users(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()