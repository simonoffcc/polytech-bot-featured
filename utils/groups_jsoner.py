import json
import os

mock_groups_path = os.path.join(os.path.dirname(__file__), "../mock_data/groups.json")
mock_groups_path = os.path.abspath(mock_groups_path)

mock_teachers_path = os.path.join(os.path.dirname(__file__), "../mock_data/teachers.json")
mock_teachers_path = os.path.abspath(mock_teachers_path)


def find_group_by_id(faculty: int, group_num: int) -> dict | None:
    with open(mock_groups_path, 'r') as groups_file:
        groups = json.load(groups_file)

    result = list(
        filter(lambda group: faculty == group['faculty'] and group_num == group['group'], groups['mock_data']))

    if not result:
        return None

    return result[0]


def find_group_by_name(group_name: str) -> list | None:
    with open(mock_groups_path, 'r') as groups_file:
        groups = json.load(groups_file)

    result = list(filter(lambda group: group_name in group['name'], groups['mock_data']))

    if not result:
        return None

    return result


def find_teacher_by_name(teacher_name: str) -> list | None:
    with open(mock_teachers_path, 'r', encoding='utf-8') as groups_file:
        teachers = json.load(groups_file)

    partial_input = teacher_name.lower().split()
    result = []

    for teacher_data in teachers['mock_data']:
        teacher_parts = teacher_data['name'].lower().split()  # Разделяем ФИО учителя

        match = True
        for part in partial_input:
            if not any(part == teacher_parts[i] for i in range(len(teacher_parts))):
                match = False
                break

        if match:
            result.append(teacher_data)

    if not result:
        return None

    return result



if __name__ == '__main__':
    res = find_teacher_by_name("Александр Гончаров")
    print(res)
