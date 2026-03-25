# Function to calculate grade
def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "Fail"


# Main program
students = []

n = int(input("Enter number of students: "))

for i in range(n):
    name = input(f"Enter name of student {i+1}: ")
    marks = float(input(f"Enter marks of {name}: "))
    
    student = {
        "name": name,
        "marks": marks,
        "grade": calculate_grade(marks)
    }
    
    students.append(student)

# Calculate average
total_marks = sum(student["marks"] for student in students)
average = total_marks / n

# Find topper
topper = max(students, key=lambda x: x["marks"])

# Display results
print("\n📊 Student Report")
for student in students:
    print(f"{student['name']} - Marks: {student['marks']} - Grade: {student['grade']}")

print(f"\n📈 Average Marks: {average:.2f}")
print(f"🏆 Topper: {topper['name']} with {topper['marks']} marks")