# I used ChatGPT for guidance, debugging help, and explanations while developing this project.
# The final implementation, testing, and design decisions are my own.

from cs50 import SQL
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///studyflow.db")


@app.route("/")
def index():

    selected_filter = request.args.get("selected_filter")
    search = request.args.get("search")

    if search:
        pattern = "%" + search + "%"
        tasks = db.execute(
            "SELECT * FROM tasks WHERE course LIKE ? OR title LIKE ? ORDER BY deadline ASC",
            pattern,
            pattern,
        )

    elif selected_filter == "pending" or selected_filter == "completed":
        tasks = db.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY deadline ASC",
            selected_filter,
        )

    else:
        tasks = db.execute("SELECT * FROM tasks ORDER BY deadline ASC")

    total_tasks = db.execute("SELECT COUNT(*) as total_tasks FROM tasks")
    pending_tasks = db.execute(
        "SELECT COUNT(*) as pending_tasks FROM tasks WHERE status = 'pending'"
    )
    completed_tasks = db.execute(
        "SELECT COUNT(*) as completed_tasks FROM tasks WHERE status = 'completed'"
    )

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks[0],
        pending_tasks=pending_tasks[0],
        completed_tasks=completed_tasks[0],
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")

    else:
        course = request.form.get("course")
        title = request.form.get("title")
        deadline = request.form.get("deadline")
        priority = request.form.get("priority")

        if (
            not course
            or not title
            or not deadline
            or not priority
            or priority == "none"
        ):
            return render_template("add.html", message="Please fill all fields.")

        db.execute(
            "INSERT INTO tasks(course, title, deadline, priority) VALUES (?, ?, ?, ?)",
            course,
            title,
            deadline,
            priority,
        )

        return redirect("/")


@app.route("/mark_completed", methods=["POST"])
def mark_complete():
    task_id = request.form.get("id")

    db.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", task_id)

    return redirect("/")


@app.route("/delete_task", methods=["POST"])
def delete_task():
    task_id = request.form.get("id")

    db.execute("DELETE FROM tasks WHERE id = ?", task_id)

    return redirect("/")
