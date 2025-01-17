import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def create_csv(filename, headers):
    #Create a CSV file with the specified headers if it doesn't exist.
    if not os.path.exists(filename):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
        print(f"CSV file '{filename}' created successfully.")

def log_expense(filename):
    #Log a new expense into the CSV file.
    print("\nLog Expense ")
    category = input("Enter the category: ")
    amount = float(input("Enter the amount: "))
    date = input("Enter the date (YYYY-MM-DD): ")

    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format! Please use YYYY-MM-DD.")
        return

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([category, amount, date])
    print("Expense logged successfully!")

def analyze_expenses(filename):
    #Analyze and display the expenses from the CSV file.
    print("\nAnalyze Expenses")
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print("No data found. Please log some expenses first.")
        return

    # Ensure the "Expenses" column is treated as numeric
    df["Expenses"] = pd.to_numeric(df["Expenses"], errors='coerce')

    total_spent = df["Expenses"].sum()
    print(f"\nTotal Spending: ${total_spent:.2f}")

    category_breakdown = df.groupby("Category")["Expenses"].sum().sort_values(ascending=False)
    print("\nCategory-wise Breakdown:")
    print(category_breakdown)

    df['Date'] = pd.to_datetime(df['Date'])
    daily_spending = df.groupby(df['Date'].dt.date)["Expenses"].sum()
    print("\nDaily Spending Trends:")
    print(daily_spending)

    print(f"\nGrand Total Expense: ${total_spent:.2f}")

def visualize_expenses(filename):
    #Visualize the expenses using bar and line graphs.
    print("\nVisualize Expenses")
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print("No data found. Please log some expenses first.")
        return

    df['Date'] = pd.to_datetime(df['Date'])

    while True:
        print("\n1. Visualize expenses by category")
        print("2. Visualize expenses by date")
        print("3. Back to main menu")
        
        sub_choice = input("Enter your choice: ")

        if sub_choice == "1":
            # Bar graph for category-wise spending
            category_breakdown = df.groupby("Category")["Expenses"].sum()
            category_breakdown.plot(kind='bar', title="Category-wise Spending", color=["orange", "green", "yellow", "red","blue","pink"])
            plt.xlabel("Category")
            plt.ylabel("Amount")
            plt.show()

        elif sub_choice == "2":
            # Line graph for daily spending trends
            daily_spending = df.groupby(df['Date'].dt.date)["Expenses"].sum()
            daily_spending.plot(kind='line', title="Daily Spending Trends",marker = 'o', ms = 8, mfc = 'r')
            plt.xlabel("Date")
            plt.ylabel("Amount")
            plt.xticks(rotation=45)
            plt.show()

        elif sub_choice == "3":
            break
        else:
            print("Invalid choice! Please try again.")

def view_csv(filename):
    #View the contents of the CSV file.
    print("\n ----EXPENSE TRACKING------")
    try:
        df = pd.read_csv(filename)
        print(df)
    except FileNotFoundError:
        print("No data found. Please log some expenses first.")

def main_menu():
    """Display the main menu and handle user choices."""
    filename = "Expenses.csv"
    headers = ["Category", "Expenses", "Date"]
    
    create_csv(filename, headers)

    while True:
        print("\n Expense Tracker ")
        print("1. Log Expense")
        print("2. View CSV")
        print("3. Analyze Expenses")
        print("4. Visualize Expenses")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            log_expense(filename)
        elif choice == "2":
            view_csv(filename)
           
        elif choice == "3":
            analyze_expenses(filename)
            
        elif choice == "4":
            visualize_expenses(filename)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()
