import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

# Data storage (in-memory dictionaries)
users = {}
workouts = {}
meals = {}
goals = {}

# Helper to generate unique IDs
def generate_id(data_dict):
    return max(data_dict.keys(), default=0) + 1

class SFMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Fitness Management System (SFMS)")
        self.root.geometry("600x400")

        ttk.Label(root, text="Welcome to SFMS", font=("Arial", 20)).pack(pady=10)

        ttk.Button(root, text="User Management", width=25, command=self.user_management).pack(pady=5)
        ttk.Button(root, text="Workout Tracking", width=25, command=self.workout_tracking).pack(pady=5)
        ttk.Button(root, text="Goal Tracking & Progress", width=25, command=self.goal_tracking).pack(pady=5)
        ttk.Button(root, text="Nutrition Tracking", width=25, command=self.nutrition_tracking).pack(pady=5)
        ttk.Button(root, text="Reports & Analytics", width=25, command=self.reports).pack(pady=5)

        ttk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=20)

    def workout_tracking(self):
        print("Workout Tracking started")
    
        # Select a user for workout tracking
        user_id = self.select_user(self.root)
        if user_id is None:
            print("No user selected, aborting workout tracking")
            return

        win = tk.Toplevel(self.root)
        win.title("Workout Tracking")
        win.geometry("700x450")

        try:
            print(f"Selected user ID: {user_id}")

            if user_id not in workouts:
                workouts[user_id] = []

            # Create workout listbox
            workout_list = tk.Listbox(win, width=40)
            workout_list.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

            details = ScrolledText(win, width=40, height=15)
            details.grid(row=0, column=1, padx=10, pady=10, rowspan=4)

            def refresh_workouts():
                workout_list.delete(0, tk.END)
                # Check if there are any workouts for the selected user
                if not workouts[user_id]:
                    workout_list.insert(tk.END, "No workouts logged yet.")
                    print("No workouts logged yet.")
                else:
                    # Populate the list with workouts
                    for idx, w in enumerate(workouts[user_id]):
                        workout_list.insert(tk.END, f"{idx + 1}: {w['type']} - {w['duration']} mins")
                    print(f"Workouts for user {user_id}: {workouts[user_id]}")

            # Call to refresh workouts
            refresh_workouts()

            def show_workout_details(event=None):
                selection = workout_list.curselection()
                if not selection:
                    return
                idx = selection[0]
                w = workouts[user_id][idx]
                text = (f"Exercise Type: {w['type']}\nDuration: {w['duration']} mins\n"
                        f"Calories Burned: {w['calories']}\nNotes: {w['notes']}")
                details.delete(1.0, tk.END)
                details.insert(tk.END, text)

            workout_list.bind('<<ListboxSelect>>', show_workout_details)

            # Add workout
            def add_workout():
                dialog = WorkoutDialog(win, "Log Workout")
                self.root.wait_window(dialog.top)
                if dialog.result:
                    workouts[user_id].append(dialog.result)
                    refresh_workouts()
                    messagebox.showinfo("Success", "Workout logged.")

            # Edit workout
            def edit_workout():
                selection = workout_list.curselection()
                if not selection:
                    messagebox.showwarning("Warning", "Select a workout to edit.")
                    return
                idx = selection[0]
                dialog = WorkoutDialog(win, "Edit Workout", workouts[user_id][idx])
                self.root.wait_window(dialog.top)
                if dialog.result:
                    workouts[user_id][idx] = dialog.result
                    refresh_workouts()
                    messagebox.showinfo("Success", "Workout updated.")

            # Delete workout
            def delete_workout():
                selection = workout_list.curselection()
                if not selection:
                    messagebox.showwarning("Warning", "Select a workout to delete.")
                    return
                idx = selection[0]
                confirm = messagebox.askyesno("Confirm Delete", "Delete this workout?")
                if confirm:
                    workouts[user_id].pop(idx)
                    refresh_workouts()
                    messagebox.showinfo("Deleted", "Workout deleted.")

            # Buttons for adding, editing, and deleting workouts
            ttk.Button(win, text="Log New Workout", command=add_workout).grid(row=5, column=1, sticky="ew", pady=5)
            ttk.Button(win, text="Edit Selected Workout", command=edit_workout).grid(row=6, column=0, sticky="ew", padx=10)
            ttk.Button(win, text="Delete Selected Workout", command=delete_workout).grid(row=6, column=1, sticky="ew", pady=5)

        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "An error occurred while creating the workout tracking window.")
    def user_management(self):
        win = tk.Toplevel(self.root)
        win.title("User Management")
        win.geometry("700x400")

        self.user_list = tk.Listbox(win, width=30)  # Store user_list as an instance variable
        self.user_list.grid(row=0, column=0, rowspan=6, padx=10, pady=10, sticky="ns")

        def refresh_user_list():
            self.user_list.delete(0, tk.END)  # Use self.user_list here
            for uid, data in users.items():
                self.user_list.insert(tk.END, f"{uid}: {data['name']}")
        refresh_user_list()

        details = ScrolledText(win, width=40, height=15)
        details.grid(row=0, column=1, padx=10, pady=10, rowspan=4)

        def show_details(event=None):
            selection = self.user_list.curselection()  # Use self.user_list here
            if not selection:
                return
            index = selection[0]
            key = list(users.keys())[index]
            data = users[key]
            text = (f"Name: {data['name']}\nAge: {data['age']}\nGender: {data['gender']}\n"
                    f"Fitness Goals: {data['goals']}")
            details.delete(1.0, tk.END)
            details.insert(tk.END, text)

        self.user_list.bind('<<ListboxSelect>>', show_details)

        ttk.Button(win, text="Create New User", command=self.create_user).grid(row=5, column=1, sticky="ew", pady=5)
        ttk.Button(win, text="Update Selected User", command=self.update_user).grid(row=6, column=0, sticky="ew", padx=10)
        ttk.Button(win, text="Delete Selected User", command=self.delete_user).grid(row=6, column=1, sticky="ew", pady=5)

    def create_user(self):
        print("Create User button clicked")  # Debugging line
        dialog = UserDialog(self.root, "Create New User")  # Pass the root window and title
        self.root.wait_window(dialog.top)  # Wait until the dialog is closed
        if dialog.result:
            uid = generate_id(users)
            users[uid] = dialog.result  # Store the new user data
            messagebox.showinfo("Success", "User profile created.")
        print(f"User created: {dialog.result}")  # Debugging line

    def update_user(self):
        selection = self.user_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a user to update.")
            return
        index = selection[0]
        key = list(users.keys())[index]
        dialog = UserDialog(self.root, "Update User", users[key])
        self.root.wait_window(dialog.top)  # Wait for the dialog window to close
        if dialog.result:
            users[key] = dialog.result  # Update the user data
            refresh_user_list()  # Refresh the list of users
            messagebox.showinfo("Success", "User profile updated.")

    def delete_user(self):
        selection = self.user_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a user to delete.")
            return
        index = selection[0]
        key = list(users.keys())[index]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete user {users[key]['name']}?")
        if confirm:
            del users[key]  # Delete the user from the dictionary
            refresh_user_list()  # Refresh the user list to show the changes
            messagebox.showinfo("Deleted", "User profile deleted.")
    
    def select_user(self, parent):
        select_win = tk.Toplevel(self.root)
        select_win.title("Select User")
        select_win.geometry("300x300")

        user_list = tk.Listbox(select_win, width=40)
        user_list.pack(padx=10, pady=10, fill='both', expand=True)

        for uid, data in users.items():
            user_list.insert(tk.END, f"{uid}: {data['name']}")

        selected_user_id = {'id': None}  # Use dict to modify from nested function

        def on_select():
            selection = user_list.curselection()
            if selection:
                selected_user_id['id'] = list(users.keys())[selection[0]]
                print(f"User selected: {selected_user_id['id']}")
                select_win.destroy()
            else:
                messagebox.showwarning("Warning", "Please select a user.")

        ttk.Button(select_win, text="Select User", command=on_select).pack(pady=5)

        select_win.grab_set()  # Prevent interacting with other windows
        select_win.wait_window(select_win)  # Wait until this window is closed

        return selected_user_id['id']

    def goal_tracking(self):
        print("Goal Tracking started")  # Debugging line
        win = tk.Toplevel(self.root)
        win.title("Goal Tracking")
        win.geometry("700x450")

        user_id = self.select_user(win)  # Select user
        if user_id is None:
            print("No user selected, closing goal tracking window")  # Debugging line
            win.destroy()
            return

        if user_id not in goals:
            goals[user_id] = []

        goal_list = tk.Listbox(win, width=40)
        goal_list.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

        details = ScrolledText(win, width=40, height=15)
        details.grid(row=0, column=1, padx=10, pady=10, rowspan=4)

        def refresh_goals():
            goal_list.delete(0, tk.END)
            for idx, g in enumerate(goals[user_id]):
                goal_list.insert(tk.END, f"{idx + 1}: {g['name']} - {g['progress']}")

        refresh_goals()

        def show_goal_details(event=None):
            selection = goal_list.curselection()
            if not selection:
                return
            idx = selection[0]
            g = goals[user_id][idx]
            text = (f"Goal: {g['name']}\nProgress: {g['progress']}\nTarget: {g['target']}")
            details.delete(1.0, tk.END)
            details.insert(tk.END, text)

        goal_list.bind('<<ListboxSelect>>', show_goal_details)

        # Add goal
        def add_goal():
            dialog = GoalDialog(win, "Set New Goal")
            self.root.wait_window(dialog.top)
            if dialog.result:
                goals[user_id].append(dialog.result)
                refresh_goals()
                messagebox.showinfo("Success", "Goal set.")

        # Edit goal
        def edit_goal():
            selection = goal_list.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Select a goal to edit.")
                return
            idx = selection[0]
            dialog = GoalDialog(win, "Edit Goal", goals[user_id][idx])
            self.root.wait_window(dialog.top)
            if dialog.result:
                goals[user_id][idx] = dialog.result
                refresh_goals()
                messagebox.showinfo("Success", "Goal updated.")

        # Delete goal
        def delete_goal():
            selection = goal_list.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Select a goal to delete.")
                return
            idx = selection[0]
            confirm = messagebox.askyesno("Confirm Delete", "Delete this goal?")
            if confirm:
                goals[user_id].pop(idx)
                refresh_goals()
                messagebox.showinfo("Deleted", "Goal deleted.")

        # Buttons for adding, editing, and deleting goals
        ttk.Button(win, text="Set New Goal", command=add_goal).grid(row=5, column=1, sticky="ew", pady=5)
        ttk.Button(win, text="Edit Selected Goal", command=edit_goal).grid(row=6, column=0, sticky="ew", padx=10)
        ttk.Button(win, text="Delete Selected Goal", command=delete_goal).grid(row=6, column=1, sticky="ew", pady=5)

    def nutrition_tracking(self):
        print("Nutrition Tracking started")  # Debugging line
        win = tk.Toplevel(self.root)
        win.title("Nutrition Tracking")
        win.geometry("700x450")

        user_id = self.select_user(win)  # Select user
        if user_id is None:
            print("No user selected, closing nutrition tracking window")  # Debugging line
            win.destroy()
            return

        if user_id not in meals:
            meals[user_id] = []

        meal_list = tk.Listbox(win, width=40)
        meal_list.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

        details = ScrolledText(win, width=40, height=15)
        details.grid(row=0, column=1, padx=10, pady=10, rowspan=4)

        def refresh_meals():
            meal_list.delete(0, tk.END)
            for idx, m in enumerate(meals[user_id]):
                meal_list.insert(tk.END, f"{idx + 1}: {m['name']} - {m['calories']} calories")
        refresh_meals()

        def show_meal_details(event=None):
            selection = meal_list.curselection()
            if not selection:
                return
            idx = selection[0]
            m = meals[user_id][idx]
            text = (f"Meal: {m['name']}\nCalories: {m['calories']}\nProtein: {m['protein']}g\n"
                    f"Carbs: {m['carbs']}g\nFats: {m['fats']}g\nNotes: {m['notes']}")
            details.delete(1.0, tk.END)
            details.insert(tk.END, text)

        meal_list.bind('<<ListboxSelect>>', show_meal_details)

        # Add meal
        def add_meal():
            dialog = MealDialog(win, "Log Meal")
            self.root.wait_window(dialog.top)
            if dialog.result:
                meals[user_id].append(dialog.result)
                refresh_meals()
                messagebox.showinfo("Success", "Meal logged.")

        # Edit meal
        def edit_meal():
            selection = meal_list.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Select a meal to edit.")
                return
            idx = selection[0]
            dialog = MealDialog(win, "Edit Meal", meals[user_id][idx])
            self.root.wait_window(dialog.top)
            if dialog.result:
                meals[user_id][idx] = dialog.result
                refresh_meals()
                messagebox.showinfo("Success", "Meal updated.")

        # Delete meal
        def delete_meal():
            selection = meal_list.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Select a meal to delete.")
                return
            idx = selection[0]
            confirm = messagebox.askyesno("Confirm Delete", "Delete this meal?")
            if confirm:
                meals[user_id].pop(idx)
                refresh_meals()
                messagebox.showinfo("Deleted", "Meal deleted.")

        # Buttons for adding, editing, and deleting meals
        ttk.Button(win, text="Log New Meal", command=add_meal).grid(row=5, column=1, sticky="ew", pady=5)
        ttk.Button(win, text="Edit Selected Meal", command=edit_meal).grid(row=6, column=0, sticky="ew", padx=10)
        ttk.Button(win, text="Delete Selected Meal", command=delete_meal).grid(row=6, column=1, sticky="ew", pady=5)

    def reports(self):
        print("Reports generation started")  # Debugging line
        win = tk.Toplevel(self.root)
        win.title("Reports")
        win.geometry("700x450")

        user_id = self.select_user(win)  # Select user
        if user_id is None:
            print("No user selected, closing report window")  # Debugging line
            win.destroy()
            return

        # Gather data for the report
        total_calories_burned = sum([w['calories'] for w in workouts.get(user_id, [])])
        total_meals = meals.get(user_id, [])
        total_calories_consumed = sum([m['calories'] for m in total_meals])
        total_protein = sum([m['protein'] for m in total_meals])
        total_carbs = sum([m['carbs'] for m in total_meals])
        total_fats = sum([m['fats'] for m in total_meals])

        # Create the report content
        report_text = f"User ID: {user_id}\n\n"
        report_text += f"Total Workouts: {len(workouts.get(user_id, []))}\n"
        report_text += f"Total Calories Burned: {total_calories_burned}\n\n"
        report_text += f"Total Meals: {len(total_meals)}\n"
        report_text += f"Total Calories Consumed: {total_calories_consumed}\n"
        report_text += f"Total Protein: {total_protein}g\n"
        report_text += f"Total Carbs: {total_carbs}g\n"
        report_text += f"Total Fats: {total_fats}g\n"

        # Display the report in a ScrolledText widget
        report_display = ScrolledText(win, width=70, height=15)
        report_display.grid(row=0, column=0, padx=10, pady=10)
        report_display.insert(tk.END, report_text)
        report_display.config(state=tk.DISABLED)  # Make the report text non-editable

        # Option to generate charts (if needed)
        def generate_chart():
            # You can use matplotlib to generate charts here, for example:
            import matplotlib.pyplot as plt

            # Data for the chart
            labels = ['Calories Burned', 'Calories Consumed']
            values = [total_calories_burned, total_calories_consumed]

            plt.bar(labels, values)
            plt.title("Calories Burned vs Calories Consumed")
            plt.show()

        # Button to generate a chart
        ttk.Button(win, text="Generate Chart", command=generate_chart).grid(row=1, column=0, pady=5)

        # Button to close the report window
        ttk.Button(win, text="Close", command=win.destroy).grid(row=2, column=0, pady=10)

# Define your UserDialog class here if needed (I assume it is defined somewhere else in your code)
class UserDialog:
    def __init__(self, parent, title, data=None):
        self.top = tk.Toplevel(parent)  # Create a new top-level window (a new dialog)
        self.top.title(title)  # Set the title of the dialog window

        tk.Label(self.top, text="Name:").grid(row=0, column=0, sticky="e")
        tk.Label(self.top, text="Age:").grid(row=1, column=0, sticky="e")
        tk.Label(self.top, text="Gender:").grid(row=2, column=0, sticky="e")
        tk.Label(self.top, text="Fitness Goals:").grid(row=3, column=0, sticky="e")

        self.name_var = tk.StringVar(value=data['name'] if data else "")
        self.age_var = tk.StringVar(value=str(data['age']) if data else "")
        self.gender_var = tk.StringVar(value=data['gender'] if data else "")
        self.goals_var = tk.StringVar(value=data['goals'] if data else "")

        tk.Entry(self.top, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(self.top, textvariable=self.age_var).grid(row=1, column=1)
        tk.Entry(self.top, textvariable=self.gender_var).grid(row=2, column=1)
        tk.Entry(self.top, textvariable=self.goals_var).grid(row=3, column=1)

        tk.Button(self.top, text="Save", command=self.save).grid(row=4, column=0, columnspan=2, pady=10)

        self.result = None  # This will hold the result after saving

    def save(self):
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        gender = self.gender_var.get().strip()
        goals = self.goals_var.get().strip()

        if not name or not age or not gender or not goals:
            messagebox.showerror("Error", "All fields are required.")
            return
        if not age.isdigit():
            messagebox.showerror("Error", "Age must be a number.")
            return

        self.result = {"name": name, "age": int(age), "gender": gender, "goals": goals}
        self.top.destroy()  # Close the dialog window after saving the data

class WorkoutDialog:
    def __init__(self, parent, title, workout=None):
        self.top = tk.Toplevel(parent)
        self.top.title(title)

        tk.Label(self.top, text="Exercise Type:").grid(row=0, column=0, sticky="e")
        tk.Label(self.top, text="Duration (minutes):").grid(row=1, column=0, sticky="e")
        tk.Label(self.top, text="Calories Burned:").grid(row=2, column=0, sticky="e")
        tk.Label(self.top, text="Notes:").grid(row=3, column=0, sticky="e")

        self.type_var = tk.StringVar(value=workout['type'] if workout else "")
        self.duration_var = tk.StringVar(value=str(workout['duration']) if workout else "")
        self.calories_var = tk.StringVar(value=str(workout['calories']) if workout else "")
        self.notes_var = tk.StringVar(value=workout['notes'] if workout else "")

        tk.Entry(self.top, textvariable=self.type_var).grid(row=0, column=1)
        tk.Entry(self.top, textvariable=self.duration_var).grid(row=1, column=1)
        tk.Entry(self.top, textvariable=self.calories_var).grid(row=2, column=1)
        tk.Entry(self.top, textvariable=self.notes_var).grid(row=3, column=1)

        tk.Button(self.top, text="Save", command=self.save).grid(row=4, column=0, columnspan=2, pady=10)

        self.result = None  # This will hold the workout data after saving

    def save(self):
        workout_type = self.type_var.get().strip()
        duration = self.duration_var.get().strip()
        calories = self.calories_var.get().strip()
        notes = self.notes_var.get().strip()

        if not workout_type or not duration or not calories or not notes:
            messagebox.showerror("Error", "All fields are required.")
            return
        if not duration.isdigit() or not calories.isdigit():
            messagebox.showerror("Error", "Duration and Calories must be numbers.")
            return

        self.result = {
            "type": workout_type,
            "duration": int(duration),
            "calories": int(calories),
            "notes": notes
        }
        self.top.destroy()

class GoalDialog:
    def __init__(self, parent, title, goal=None):
        self.top = tk.Toplevel(parent)
        self.top.title(title)

        tk.Label(self.top, text="Goal Name:").grid(row=0, column=0, sticky="e")
        tk.Label(self.top, text="Progress:").grid(row=1, column=0, sticky="e")
        tk.Label(self.top, text="Target:").grid(row=2, column=0, sticky="e")

        self.name_var = tk.StringVar(value=goal['name'] if goal else "")
        self.progress_var = tk.StringVar(value=str(goal['progress']) if goal else "")
        self.target_var = tk.StringVar(value=str(goal['target']) if goal else "")

        tk.Entry(self.top, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(self.top, textvariable=self.progress_var).grid(row=1, column=1)
        tk.Entry(self.top, textvariable=self.target_var).grid(row=2, column=1)

        tk.Button(self.top, text="Save", command=self.save).grid(row=3, column=0, columnspan=2, pady=10)

        self.result = None

    def save(self):
        name = self.name_var.get().strip()
        progress = self.progress_var.get().strip()
        target = self.target_var.get().strip()

        if not name or not progress or not target:
            messagebox.showerror("Error", "All fields are required.")
            return
        if not progress.isdigit() or not target.isdigit():
            messagebox.showerror("Error", "Progress and Target must be numbers.")
            return

        self.result = {"name": name, "progress": int(progress), "target": int(target)}
        self.top.destroy()

class MealDialog:
    def __init__(self, parent, title, meal=None):
        self.top = tk.Toplevel(parent)
        self.top.title(title)

        tk.Label(self.top, text="Meal Name:").grid(row=0, column=0, sticky="e")
        tk.Label(self.top, text="Calories:").grid(row=1, column=0, sticky="e")
        tk.Label(self.top, text="Protein (g):").grid(row=2, column=0, sticky="e")
        tk.Label(self.top, text="Carbs (g):").grid(row=3, column=0, sticky="e")
        tk.Label(self.top, text="Fats (g):").grid(row=4, column=0, sticky="e")
        tk.Label(self.top, text="Notes:").grid(row=5, column=0, sticky="e")

        self.name_var = tk.StringVar(value=meal['name'] if meal else "")
        self.calories_var = tk.StringVar(value=str(meal['calories']) if meal else "")
        self.protein_var = tk.StringVar(value=str(meal['protein']) if meal else "")
        self.carbs_var = tk.StringVar(value=str(meal['carbs']) if meal else "")
        self.fats_var = tk.StringVar(value=str(meal['fats']) if meal else "")
        self.notes_var = tk.StringVar(value=meal['notes'] if meal else "")

        tk.Entry(self.top, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(self.top, textvariable=self.calories_var).grid(row=1, column=1)
        tk.Entry(self.top, textvariable=self.protein_var).grid(row=2, column=1)
        tk.Entry(self.top, textvariable=self.carbs_var).grid(row=3, column=1)
        tk.Entry(self.top, textvariable=self.fats_var).grid(row=4, column=1)
        tk.Entry(self.top, textvariable=self.notes_var).grid(row=5, column=1)

        tk.Button(self.top, text="Save", command=self.save).grid(row=6, column=0, columnspan=2, pady=10)

        self.result = None  # This will hold the result after saving

    def save(self):
        name = self.name_var.get().strip()
        calories = self.calories_var.get().strip()
        protein = self.protein_var.get().strip()
        carbs = self.carbs_var.get().strip()
        fats = self.fats_var.get().strip()
        notes = self.notes_var.get().strip()

        if not name or not calories or not protein or not carbs or not fats or not notes:
            messagebox.showerror("Error", "All fields are required.")
            return
        if not calories.isdigit() or not protein.isdigit() or not carbs.isdigit() or not fats.isdigit():
            messagebox.showerror("Error", "Calories, Protein, Carbs, and Fats must be numbers.")
            return

        self.result = {
            "name": name,
            "calories": int(calories),
            "protein": int(protein),
            "carbs": int(carbs),
            "fats": int(fats),
            "notes": notes
        }
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SFMSApp(root)
    root.mainloop()
