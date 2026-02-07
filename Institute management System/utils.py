from datetime import datetime

def format_date(value):
    if not value:
        return ""
    if isinstance(value, str):
        return value
    return value.strftime("%Y-%m-%d")
def sort_students_by_name(students):
    return sorted(students, key=lambda x: x["name"].lower())


def binary_search_student_by_id(students, target_id):
    low = 0
    high = len(students) - 1

    while low <= high:
        mid = (low + high) // 2
        if students[mid]["id"] == target_id:
            return students[mid]
        elif students[mid]["id"] < target_id:
            low = mid + 1
        else:
            high = mid - 1

    return None
