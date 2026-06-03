import csv
import os
from datetime import datetime

TRACKER_FILE = "job_applications.csv"
FIELDS = ["id", "date_applied", "company", "role", "platform", "status", "notes"]
STATUSES = ["Applied", "Interview", "Rejected", "Offer", "Ghosted"]


def load_applications():
    if not os.path.isfile(TRACKER_FILE):
        return []
    with open(TRACKER_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_applications(apps):
    with open(TRACKER_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(apps)


def next_id(apps):
    if not apps:
        return 1
    return max(int(a["id"]) for a in apps) + 1


def add_application():
    print("\n--- Add New Application ---")
    company = input("Company name: ").strip()
    role = input("Role/Position: ").strip()
    platform = input("Where did you apply? (LinkedIn / Email / Website / etc): ").strip()
    notes = input("Notes (optional): ").strip()

    apps = load_applications()
    apps.append({
        "id": next_id(apps),
        "date_applied": datetime.now().strftime("%Y-%m-%d"),
        "company": company,
        "role": role,
        "platform": platform,
        "status": "Applied",
        "notes": notes,
    })
    save_applications(apps)
    print(f"\nSaved! {role} at {company} added to your tracker.")


def view_all():
    apps = load_applications()
    if not apps:
        print("\nNo applications yet. Start applying!")
        return

    print(f"\n{'ID':<4} {'Date':<12} {'Company':<20} {'Role':<25} {'Status':<12} {'Platform'}")
    print("-" * 85)
    for a in apps:
        print(f"{a['id']:<4} {a['date_applied']:<12} {a['company']:<20} {a['role']:<25} {a['status']:<12} {a['platform']}")


def update_status():
    apps = load_applications()
    if not apps:
        print("\nNo applications to update.")
        return

    view_all()
    try:
        app_id = int(input("\nEnter ID to update: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    app = next((a for a in apps if int(a["id"]) == app_id), None)
    if not app:
        print("Application not found.")
        return

    print(f"\nCurrent status: {app['status']}")
    print("Choose new status:")
    for i, s in enumerate(STATUSES, 1):
        print(f"  {i}. {s}")

    try:
        choice = int(input("Enter number: ").strip())
        app["status"] = STATUSES[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    notes = input(f"Update notes (current: '{app['notes']}'): ").strip()
    if notes:
        app["notes"] = notes

    save_applications(apps)
    print(f"\nUpdated! {app['company']} is now marked as: {app['status']}")


def show_summary():
    apps = load_applications()
    if not apps:
        print("\nNo applications yet.")
        return

    total = len(apps)
    by_status = {}
    for a in apps:
        by_status[a["status"]] = by_status.get(a["status"], 0) + 1

    print(f"\n--- Your Job Search Summary ---")
    print(f"Total applications: {total}")
    for status, count in sorted(by_status.items()):
        bar = "#" * count
        print(f"  {status:<12} {bar} ({count})")

    interviews = by_status.get("Interview", 0)
    if total > 0:
        rate = round((interviews / total) * 100)
        print(f"\nInterview rate: {rate}%")


def main():
    print("=" * 40)
    print("   JOB APPLICATION TRACKER")
    print("=" * 40)

    while True:
        print("\nWhat do you want to do?")
        print("  1. Add new application")
        print("  2. View all applications")
        print("  3. Update application status")
        print("  4. Show summary")
        print("  5. Exit")

        choice = input("\nEnter number: ").strip()

        if choice == "1":
            add_application()
        elif choice == "2":
            view_all()
        elif choice == "3":
            update_status()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("\nGood luck with your applications!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
