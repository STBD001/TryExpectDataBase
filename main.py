import tkinter as tk
from tkinter import messagebox
from exceptions import UserNotFoundError, UserAlreadyExistsError, InvalidUserDataError
from user_database import UserDatabase

class UserApp:
    def __init__(self, root):
        self.db = UserDatabase()
        self.root = root
        self.root.title("User Management App")

        # Add User Section
        self.add_user_frame = tk.Frame(root)
        self.add_user_frame.pack(pady=10)

        self.user_id_label = tk.Label(self.add_user_frame, text="User ID")
        self.user_id_label.grid(row=0, column=0, padx=5)
        self.user_id_entry = tk.Entry(self.add_user_frame)
        self.user_id_entry.grid(row=0, column=1, padx=5)

        self.user_name_label = tk.Label(self.add_user_frame, text="Name")
        self.user_name_label.grid(row=1, column=0, padx=5)
        self.user_name_entry = tk.Entry(self.add_user_frame)
        self.user_name_entry.grid(row=1, column=1, padx=5)

        self.user_email_label = tk.Label(self.add_user_frame, text="Email")
        self.user_email_label.grid(row=2, column=0, padx=5)
        self.user_email_entry = tk.Entry(self.add_user_frame)
        self.user_email_entry.grid(row=2, column=1, padx=5)

        self.add_user_button = tk.Button(self.add_user_frame, text="Add User", command=self.add_user)
        self.add_user_button.grid(row=3, columnspan=2, pady=5)

        # User List Section
        self.user_list_frame = tk.Frame(root)
        self.user_list_frame.pack(pady=10)

        self.user_list_label = tk.Label(self.user_list_frame, text="User List")
        self.user_list_label.grid(row=0, column=0)

        self.user_listbox = tk.Listbox(self.user_list_frame, width=50)
        self.user_listbox.grid(row=1, column=0)
        self.user_listbox.bind('<<ListboxSelect>>', self.on_user_select)

        # Update/Delete Section
        self.update_user_button = tk.Button(root, text="Update User", command=self.update_user)
        self.update_user_button.pack(pady=5)

        self.delete_user_button = tk.Button(root, text="Delete User", command=self.delete_user)
        self.delete_user_button.pack(pady=5)

        # Initialize the user list
        self.refresh_user_list()

    def add_user(self):
        user_id = self.user_id_entry.get()
        name = self.user_name_entry.get()
        email = self.user_email_entry.get()
        if not user_id or not name or not email:
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            self.db.add_user(user_id, {"name": name, "email": email})
            messagebox.showinfo("Success", "User added successfully")
            self.refresh_user_list()
        except UserAlreadyExistsError as e:
            messagebox.showerror("Error", str(e))
        except InvalidUserDataError as e:
            messagebox.showerror("Error", str(e))

    def delete_user(self):
        selected_user = self.user_listbox.curselection()
        if not selected_user:
            messagebox.showerror("Error", "No user selected")
            return
        user_id = self.user_listbox.get(selected_user)
        try:
            self.db.remove_user(user_id)
            messagebox.showinfo("Success", "User deleted successfully")
            self.refresh_user_list()
        except UserNotFoundError as e:
            messagebox.showerror("Error", str(e))

    def update_user(self):
        selected_user = self.user_listbox.curselection()
        if not selected_user:
            messagebox.showerror("Error", "No user selected")
            return
        user_id = self.user_listbox.get(selected_user)
        name = self.user_name_entry.get()
        email = self.user_email_entry.get()
        if not name or not email:
            messagebox.showerror("Error", "Name and email are required for update")
            return
        try:
            self.db.update_user(user_id, {"name": name, "email": email})
            messagebox.showinfo("Success", "User updated successfully")
            self.refresh_user_list()
        except UserNotFoundError as e:
            messagebox.showerror("Error", str(e))
        except InvalidUserDataError as e:
            messagebox.showerror("Error", str(e))

    def refresh_user_list(self):
        self.user_listbox.delete(0, tk.END)
        for user_id in self.db.get_all_users():
            self.user_listbox.insert(tk.END, user_id)

    def on_user_select(self, event):
        selected_user = self.user_listbox.curselection()
        if selected_user:
            user_id = self.user_listbox.get(selected_user)
            user_data = self.db.get_user(user_id)
            self.user_id_entry.delete(0, tk.END)
            self.user_id_entry.insert(0, user_id)
            self.user_name_entry.delete(0, tk.END)
            self.user_name_entry.insert(0, user_data['name'])
            self.user_email_entry.delete(0, tk.END)
            self.user_email_entry.insert(0, user_data['email'])

if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()
