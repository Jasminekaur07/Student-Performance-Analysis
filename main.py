import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File and subject details
FILE = Path(__file__).with_name("students.csv")

SUBJECTS = ["English", "Maths", "Computer", "Science", "Accounts"]

COLUMNS = ["Roll_No", "Name", "Class"] + SUBJECTS


# 1. Load student data
def load_data():
    if not FILE.exists():
        pd.DataFrame(columns=COLUMNS).to_csv(FILE, index=False)

    data = pd.read_csv(FILE)

    for col in COLUMNS:
        if col not in data.columns:
            data[col] = "" if col in ["Name", "Class"] else 0

    return data[COLUMNS]


# 2. Save student data
def save_data(data):
    data.to_csv(FILE, index=False)


# 3. Input marks
def get_marks():
    marks = {}

    for subject in SUBJECTS:
        while True:
            try:
                mark = float(
                    input(f"Enter marks in {subject} (0-100): ")
                )

                if 0 <= mark <= 100:
                    marks[subject] = mark
                    break

                print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid number.")

    return marks


# 4. Add a new student
def add_student():
    data = load_data()

    try:
        roll = int(input("Enter roll number: "))
    except ValueError:
        print("Invalid roll number.")
        return

    existing_rolls = pd.to_numeric(
        data["Roll_No"], errors="coerce"
    )

    if roll in existing_rolls.values:
        print("Roll number already exists.")
        return

    name = input("Enter student name: ").strip()
    student_class = input("Enter class (e.g. BCA-1): ").strip()

    if not name or not student_class:
        print("Name and class cannot be empty.")
        return

    record = {
        "Roll_No": roll,
        "Name": name,
        "Class": student_class
    }

    record.update(get_marks())

    new_row = pd.DataFrame([record])
    data = pd.concat([data, new_row], ignore_index=True)

    save_data(data)
    print("Student added successfully!")


# 5. View all students
def view_students():
    data = load_data()

    if data.empty:
        print("No student records found.")
    else:
        print("\n========== STUDENT RECORDS ==========")
        print(data.to_string(index=False))


# 6. Search student by roll number
def search_student():
    data = load_data()

    roll = input("Enter roll number to search: ").strip()

    result = data[
        data["Roll_No"].astype(str) == roll
    ]

    if result.empty:
        print("Student not found.")
    else:
        print("\nStudent Details:")
        print(result.to_string(index=False))


# 7. Update student marks
def update_student():
    data = load_data()

    roll = input("Enter roll number to update: ").strip()

    matches = data.index[
        data["Roll_No"].astype(str) == roll
    ].tolist()

    if not matches:
        print("Student not found.")
        return

    index = matches[0]

    print("Enter the updated marks:")

    marks = get_marks()

    for subject, mark in marks.items():
        data.loc[index, subject] = mark

    save_data(data)

    print("Marks updated successfully!")


# 8. Delete a student
def delete_student():
    data = load_data()

    roll = input("Enter roll number to delete: ").strip()

    result = data[
        data["Roll_No"].astype(str) != roll
    ]

    if len(result) == len(data):
        print("Student not found.")
    else:
        save_data(result)
        print("Student deleted successfully!")


# 9. Calculate grade
def grade_for(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 33:
        return "E"
    else:
        return "F"


# 10. Generate an individual student report
def student_report():
    data = load_data()

    roll = input("Enter roll number: ").strip()

    result = data[
        data["Roll_No"].astype(str) == roll
    ]

    if result.empty:
        print("Student not found.")
        return

    student = result.iloc[0]

    marks = pd.to_numeric(student[SUBJECTS])

    total = marks.sum()
    percentage = total / len(SUBJECTS)

    passed = all(marks >= 33)

    print("\n========== STUDENT REPORT ==========")
    print("Roll Number :", student["Roll_No"])
    print("Name        :", student["Name"])
    print("Class       :", student["Class"])

    print("\nSubject-wise Marks:")

    for subject in SUBJECTS:
        print(f"{subject}: {marks[subject]:.0f}/100")

    print("\nTotal       :", f"{total:.0f}/500")
    print("Percentage  :", f"{percentage:.2f}%")
    print("Grade       :", grade_for(percentage))
    print("Result      :", "PASS" if passed else "FAIL")


# 11. Class analysis and ranking
def class_analysis():
    data = load_data()

    if data.empty:
        print("No student records to analyse.")
        return

    marks = data[SUBJECTS].apply(
        pd.to_numeric, errors="coerce"
    ).fillna(0)

    data["Total"] = marks.sum(axis=1)
    data["Percentage"] = data["Total"] / len(SUBJECTS)

    data["Result"] = marks.ge(33).all(axis=1).map({
        True: "PASS",
        False: "FAIL"
    })

    data["Grade"] = data["Percentage"].apply(grade_for)

    topper = data.loc[data["Percentage"].idxmax()]

    print("\n========== CLASS ANALYSIS ==========")
    print("Total Students :", len(data))
    print(f"Class Average  : {data['Percentage'].mean():.2f}%")
    print(
        f"Class Topper   : {topper['Name']} "
        f"({topper['Percentage']:.2f}%)"
    )
    print("Students Passed:", (data["Result"] == "PASS").sum())
    print("Students Failed:", (data["Result"] == "FAIL").sum())

    print("\n========== STUDENT RANKING ==========")

    ranking = data.sort_values(
        "Percentage", ascending=False
    )

    ranking = ranking[
        [
            "Roll_No", "Name", "Total",
            "Percentage", "Grade", "Result"
        ]
    ]

    ranking = ranking.reset_index(drop=True)
    ranking.index = ranking.index + 1
    ranking.index.name = "Rank"

    print(ranking.to_string())


# 12. Subject-wise analysis
def subject_analysis():
    data = load_data()

    if data.empty:
        print("No student records to analyse.")
        return

    marks = data[SUBJECTS].apply(
        pd.to_numeric, errors="coerce"
    )

    print("\n========== SUBJECT-WISE ANALYSIS ==========")

    print(
        f"{'Subject':<12}"
        f"{'Average':>10}"
        f"{'Highest':>10}"
        f"{'Lowest':>10}"
    )

    for subject in SUBJECTS:
        print(
            f"{subject:<12}"
            f"{marks[subject].mean():>10.2f}"
            f"{marks[subject].max():>10.2f}"
            f"{marks[subject].min():>10.2f}"
        )


# 13. Display performance graphs
def show_graphs():
    data = load_data()

    if data.empty:
        print("No student records to display.")
        return

    marks = data[SUBJECTS].apply(
        pd.to_numeric, errors="coerce"
    ).fillna(0)

    # Graph 1: Average marks in each subject
    average_marks = marks.mean()

    plt.figure(figsize=(8, 5))
    average_marks.plot(kind="bar")

    plt.title("Average Marks by Subject")
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

    # Graph 2: Student percentage comparison
    percentages = marks.mean(axis=1)

    plt.figure(figsize=(8, 5))
    plt.bar(data["Name"].astype(str), percentages)

    plt.title("Student Performance Comparison")
    plt.xlabel("Students")
    plt.ylabel("Percentage")
    plt.ylim(0, 100)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()


# 14. Export performance report to CSV
def export_report():
    data = load_data()

    if data.empty:
        print("No student records to export.")
        return

    marks = data[SUBJECTS].apply(
        pd.to_numeric, errors="coerce"
    ).fillna(0)

    report = data[
        ["Roll_No", "Name", "Class"]
    ].copy()

    report["Total"] = marks.sum(axis=1)
    report["Percentage"] = report["Total"] / len(SUBJECTS)
    report["Grade"] = report["Percentage"].apply(grade_for)

    report["Result"] = marks.ge(33).all(axis=1).map({
        True: "PASS",
        False: "FAIL"
    })

    output = FILE.with_name("student_report.csv")

    report.to_csv(output, index=False)

    print("Report exported successfully!")
    print("File name:", output.name)


# 15. Main menu
def main():
    while True:
        print("\n============================================")
        print("  STUDENT PERFORMANCE ANALYSIS SYSTEM")
        print("============================================")

        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Marks")
        print("5. Delete Student")
        print("6. Generate Individual Report")
        print("7. Class Analysis and Ranking")
        print("8. Subject-wise Analysis")
        print("9. Show Performance Graphs")
        print("10. Export Report to CSV")
        print("11. Exit")

        choice = input("\nEnter your choice (1-11): ").strip()

        actions = {
            "1": add_student,
            "2": view_students,
            "3": search_student,
            "4": update_student,
            "5": delete_student,
            "6": student_report,
            "7": class_analysis,
            "8": subject_analysis,
            "9": show_graphs,
            "10": export_report
        }

        if choice == "11":
            print("Thank you for using the system!")
            break

        action = actions.get(choice)

        if action:
            try:
                action()
            except (ValueError, KeyError, TypeError) as error:
                print("Could not complete this action.")
                print("Please check the data and try again.")
                print("Details:", error)
        else:
            print("Invalid choice. Please select 1-11.")


if __name__ == "__main__":
    main()
