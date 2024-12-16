import tkinter as tk
from tkinter import messagebox, simpledialog
import os


NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)

def get_note_filepath(title):
    return os.path.join(NOTES_DIR, f"{title}.txt")

def load_notes():
    notes = {}
    for filename in os.listdir(NOTES_DIR):
        if filename.endswith(".txt"):
            title = filename[:-4]
            with open(get_note_filepath(title), "r") as file:
                lines = file.readlines()
                password = lines[0].strip()
                content = "".join(lines[1:]).strip()
                notes[title] = {"content": content, "password": password}
    return notes

def save_note_to_file(title, content, password):
    with open(get_note_filepath(title), "w") as file:
        file.write(password + "\n")
        file.write(content)

def delete_note_file(title):
    os.remove(get_note_filepath(title))

def add_note():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END).strip()
    password = password_entry.get()

    if not title or not content or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    if title in notes:
        messagebox.showerror("Error", "A note with this title already exists!")
        return

    notes[title] = {"content": content, "password": password}
    save_note_to_file(title, content, password)
    messagebox.showinfo("Success", "Note added successfully!")
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)
    password_entry.delete(0, tk.END)

def view_note():
    title = title_entry.get()
    if title not in notes:
        messagebox.showerror("Error", "Note not found!")
        return

    password = simpledialog.askstring("Password", "Enter the password for this note:", show="*")
    if password == notes[title]["password"]:
        content_text.delete("1.0", tk.END)
        content_text.insert(tk.END, notes[title]["content"])
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Incorrect password!")

def delete_note():
    title = title_entry.get()
    if title not in notes:
        messagebox.showerror("Error", "Note not found!")
        return

    password = simpledialog.askstring("Password", "Enter the password to delete this note:", show="*")
    if password == notes[title]["password"]:
        del notes[title]
        delete_note_file(title)
        messagebox.showinfo("Success", "Note deleted successfully!")
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Incorrect password!")


notes = load_notes()

root = tk.Tk()
root.title("Secure Note App")

frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

tk.Label(frame, text="Title:").grid(row=0, column=0, sticky="w")
title_entry = tk.Entry(frame, width=40)
title_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Password:").grid(row=1, column=0, sticky="w")
password_entry = tk.Entry(frame, width=40, show="*")
password_entry.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Content:").grid(row=2, column=0, sticky="nw")
content_text = tk.Text(frame, width=40, height=10)
content_text.grid(row=2, column=1, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Note", command=add_note).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="View Note", command=view_note).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Note", command=delete_note).grid(row=0, column=2, padx=5)

root.mainloop()
