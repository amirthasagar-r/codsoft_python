import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
from datetime import datetime

# File to store the to-do list
FILE_NAME = 'todo_list.json'

class Task:
    def __init__(self, description, priority='Low', due_date=None):
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date
        }

    @staticmethod
    def from_dict(task_dict):
        return Task(
            description=task_dict['description'],
            priority=task_dict['priority'],
            due_date=task_dict.get('due_date')
        )

    def __str__(self):
        return f"{self.description} (Priority: {self.priority}, Due Date: {self.due_date})"

def load_todo_list():
    try:
        with open(FILE_NAME, 'r') as file:
            tasks_dict = json.load(file)
            return [Task.from_dict(task) for task in tasks_dict]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_todo_list(todo_list):
    with open(FILE_NAME, 'w') as file:
        json.dump([task.to_dict() for task in todo_list], file, indent=4)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")

        self.todo_list = load_todo_list()

        # Create the UI components
        self.create_widgets()

        # Populate the listbox with tasks
        self.update_listbox()

    def create_widgets(self):
        # Frame for the listbox and scrollbar
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        self.listbox = tk.Listbox(frame, width=50, height=15)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.add_button = tk.Button(button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(button_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(button_frame, text="Update Task", command=self.update_task)
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_app)
        self.exit_button.pack(side=tk.LEFT, padx=5)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.todo_list:
            self.listbox.insert(tk.END, str(task))

    def add_task(self):
        description = simpledialog.askstring("Input", "Enter the task description:")
        if not description:
            return
        
        priority = simpledialog.askstring("Input", "Enter priority (Low, Medium, High):").capitalize()
        if priority not in ['Low', 'Medium', 'High']:
            messagebox.showerror("Error", "Invalid priority. Task not added.")
            return

        due_date = simpledialog.askstring("Input", "Enter due date (YYYY-MM-DD) or leave empty:")
        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Task not added.")
                return
        
        task = Task(description, priority, due_date)
        self.todo_list.append(task)
        self.update_listbox()
        save_todo_list(self.todo_list)

    def remove_task(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No task selected.")
            return

        task = self.todo_list[selected_index[0]]
        self.todo_list.pop(selected_index[0])
        self.update_listbox()
        save_todo_list(self.todo_list)

    def update_task(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No task selected.")
            return

        task = self.todo_list[selected_index[0]]

        new_description = simpledialog.askstring("Input", f"New description (leave empty to keep '{task.description}'):") or task.description
        new_priority = simpledialog.askstring("Input", f"New priority (leave empty to keep '{task.priority}'):").capitalize() or task.priority
        if new_priority not in ['Low', 'Medium', 'High']:
            messagebox.showerror("Error", "Invalid priority. Task not updated.")
            return

        new_due_date = simpledialog.askstring("Input", f"New due date (leave empty to keep '{task.due_date}'):") or task.due_date
        if new_due_date:
            try:
                datetime.strptime(new_due_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Due date not updated.")
                return

        task.description = new_description
        task.priority = new_priority
        task.due_date = new_due_date

        self.update_listbox()
        save_todo_list(self.todo_list)

    def exit_app(self):
        save_todo_list(self.todo_list)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
