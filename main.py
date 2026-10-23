import csv
from datetime import datetime
import os

CSV_FILE = "parking_records.csv"


def initialize_csv():
    """Creates the CSV file with headers if it does not exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Plate",
                    "Entry_Time",
                    "Exit_Time",
                    "Duration_Hours",
                    "Fee_TL",
                    "Status",
                ]
            )


def calculate_fee(hours):
    """Calculates fee based on duration in hours."""
    if hours <= 1:
        return 50.0
    elif hours <= 3:
        return 90.0
    elif hours <= 6:
        return 150.0
    elif hours <= 12:
        return 220.0
    else:
        # Daily rate / 12+ hours
        days = (hours // 24) + 1
        return days * 350.0


def vehicle_entry():
    """Registers a new vehicle entering the parking lot."""
    plate = input("Enter vehicle plate (e.g., 34ABC123): ").strip().upper()
    if not plate:
        print("Plate cannot be empty!")
        return

    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([plate, entry_time, "N/A", 0, 0.0, "PARKED"])

    print(
        f"Vehicle {plate} successfully registered at entry time: {entry_time}"
    )


def vehicle_exit():
    """Processes vehicle exit, calculates fee, and updates CSV."""
    plate = input("Enter vehicle plate for exit: ").strip().upper()
    records = []
    found = False

    if not os.path.exists(CSV_FILE):
        print("No parking records found!")
        return

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = list(csv.reader(file))
        if not reader:
            print("Records file is empty.")
            return
        header = reader[0]
        data = reader[1:]

    for row in data:
        # Check if plate matches and status is PARKED
        if len(row) >= 6 and row[0] == plate and row[5] == "PARKED" and not found:
            entry_time_str = row[1]
            entry_dt = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
            exit_dt = datetime.now()
            exit_time_str = exit_dt.strftime("%Y-%m-%d %H:%M:%S")

            # Calculate stay duration in hours (minimum 1 hour rounding for demo)
            duration_seconds = (exit_dt - entry_dt).total_seconds()
            duration_hours = max(1.0, round(duration_seconds / 3600, 2))

            fee = calculate_fee(duration_hours)

            # Update row: Exit_Time, Duration_Hours, Fee_TL, Status
            row[2] = exit_time_str
            row[3] = str(duration_hours)
            row[4] = f"{fee:.2f}"
            row[5] = "COMPLETED"

            found = True
            print(f"\n--- EXIT SUMMARY FOR {plate} ---")
            print(f"Entry Time:     {entry_time_str}")
            print(f"Exit Time:      {exit_time_str}")
            print(f"Duration:       {duration_hours} Hour(s)")
            print(f"Total Fee:      {fee:.2f} TL")

        records.append(row)

    if found:
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(records)
    else:
        print(f"No active parked vehicle found with plate: {plate}")


def daily_income_report():
    """Reads CSV and prints total revenue and vehicle counts."""
    if not os.path.exists(CSV_FILE):
        print("No parking records available.")
        return

    total_revenue = 0.0
    total_vehicles = 0
    currently_parked = 0

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader, None)

        for row in reader:
            if len(row) >= 6:
                if row[5] == "COMPLETED":
                    total_revenue += float(row[4])
                    total_vehicles += 1
                elif row[5] == "PARKED":
                    currently_parked += 1

    print("\n================ DAILY REPORT ================")
    print(f"Completed Transactions:  {total_vehicles}")
    print(f"Currently Parked:        {currently_parked}")
    print(f"Total Earnings:          {total_revenue:.2f} TL")
    print("==============================================")


def main_menu():
    initialize_csv()
    while True:
        print("\n=== PARKING LOT FEE SYSTEM ===")
        print("1. Vehicle Entry")
        print("2. Vehicle Exit & Calculate Fee")
        print("3. Daily Income Report")
        print("4. Exit")

        choice = input("Please select an option (1-4): ").strip()

        if choice == "1":
            vehicle_entry()
        elif choice == "2":
            vehicle_exit()
        elif choice == "3":
            daily_income_report()
        elif choice == "4":
            print("Exiting system. Have a good day!")
            break
        else:
            print("Invalid choice, please select between 1 and 4.")


if __name__ == "__main__":
    main_menu()