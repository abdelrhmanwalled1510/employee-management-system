import csv
import re
from pathlib import Path

class EmployeeManager:
    FIELDNAMES = ["id", "name", "position", "salary", "email"]
    def __init__(self, filename="employees.csv"):
        self.filename = Path(filename)
        self.employees = {}
        self.load_employees()

    def load_employees(self):
        if not self.filename.exists():
            return

        try:
            with self.filename.open("r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames != self.FIELDNAMES:
                    print("Warning: CSV columns are invalid. Starting with no records.")
                    return
                for row in reader:
                    employee_id = row["id"].strip()
                    if employee_id:
                        self.employees[employee_id] = {
                            field: row[field].strip() for field in self.FIELDNAMES
                        }
        except (OSError, csv.Error) as error:
            print(f"Could not load employee data: {error}")

    def save_employees(self):
        try:
            with self.filename.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                writer.writerows(self.employees.values())
        except OSError as error:
            print(f"Could not save employee data: {error}")

    @staticmethod
    def valid_salary(salary):
        try:
            return float(salary) >= 0
        except ValueError:
            return False

    @staticmethod
    def valid_email(email):
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))

    def add_employee(self):
        employee_id = input("Employee ID: ").strip()
        if not employee_id:
            print("ID cannot be empty.")
            return
        if employee_id in self.employees:
            print("An employee with this ID already exists.")
            return

        name = input("Name: ").strip()
        position = input("Position: ").strip()
        salary = input("Salary: ").strip()
        email = input("Email: ").strip()

        if not name or not position:
            print("Name and position cannot be empty.")
            return
        if not self.valid_salary(salary):
            print("Salary must be a non-negative number.")
            return
        if not self.valid_email(email):
            print("Please enter a valid email address.")
            return

        self.employees[employee_id] = {
            "id": employee_id,
            "name": name,
            "position": position,
            "salary": salary,
            "email": email,
        }
        self.save_employees()
        print("Employee added successfully.")

    def view_employees(self):
        """Display all employees currently stored in memory."""
        if not self.employees:
            print("No employees found.")
            return

        print("\n" + "=" * 62)
        print(f"{'ID':<10} {'Name':<18} {'Position':<16} {'Salary':<10} Email")
        print("-" * 62)
        for employee in self.employees.values():
            print(
                f"{employee['id']:<10} {employee['name']:<18} "
                f"{employee['position']:<16} {employee['salary']:<10} "
                f"{employee['email']}"
            )
        print("=" * 62)

    def search_employee(self):
        employee_id = input("Enter employee ID to search: ").strip()
        employee = self.employees.get(employee_id)
        if not employee:
            print("Employee not found.")
            return
        self.display_employee(employee)

    def update_employee(self):
        employee_id = input("Enter employee ID to update: ").strip()
        employee = self.employees.get(employee_id)
        if not employee:
            print("Employee not found.")
            return

        print("Leave a field empty to keep its current value.")
        name = input(f"Name [{employee['name']}]: ").strip()
        position = input(f"Position [{employee['position']}]: ").strip()
        salary = input(f"Salary [{employee['salary']}]: ").strip()
        email = input(f"Email [{employee['email']}]: ").strip()

        if salary and not self.valid_salary(salary):
            print("Salary must be a non-negative number. No changes were saved.")
            return
        if email and not self.valid_email(email):
            print("Please enter a valid email address. No changes were saved.")
            return

        if name:
            employee["name"] = name
        if position:
            employee["position"] = position
        if salary:
            employee["salary"] = salary
        if email:
            employee["email"] = email

        self.save_employees()
        print("Employee updated successfully.")

    def delete_employee(self):
        employee_id = input("Enter employee ID to delete: ").strip()
        employee = self.employees.get(employee_id)
        if not employee:
            print("Employee not found.")
            return

        self.display_employee(employee)
        confirmation = input("Delete this employee? (y/n): ").strip().lower()
        if confirmation == "y":
            del self.employees[employee_id]
            self.save_employees()
            print("Employee deleted successfully.")
        else:
            print("Delete cancelled.")

    @staticmethod
    def display_employee(employee):
        print("\nEmployee details")
        print("-" * 20)
        for field in ("id", "name", "position", "salary", "email"):
            print(f"{field.capitalize()}: {employee[field]}")

    def run(self):
        actions = {
            "1": self.add_employee,
            "2": self.view_employees,
            "3": self.update_employee,
            "4": self.delete_employee,
            "5": self.search_employee,
        }

        while True:
            print("\n--- Employee Data Management System ---")
            print("1. Add Employee")
            print("2. View All Employees")
            print("3. Update Employee")
            print("4. Delete Employee")
            print("5. Search Employee")
            print("6. Exit")
            choice = input("Choose an option (1-6): ").strip()

            if choice == "6":
                print("Goodbye!")
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":
    csv_path = Path(__file__).with_name("employees.csv")
    EmployeeManager(csv_path).run()
