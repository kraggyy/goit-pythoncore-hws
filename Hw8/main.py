from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):
    birthdays = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
    days_name = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Monday",
        6: "Monday",
    }

    current_date = date.today()
    # print(f"Початкова дата перевірки {current_date}")
    delta = timedelta(days=6)
    end_of_week = current_date + delta
    # print(f"Кінцева дата перевірки {end_of_week}")

    current_year = current_date.year
    current_month = current_date.month

    for user in users:
        birthday = user["birthday"]
        if current_month == 12 and birthday.month == 1:
            birthday_to_check = birthday.replace(year=current_year + 1)
        else:
            birthday_to_check = birthday.replace(year=current_year)

        if current_date <= birthday_to_check <= end_of_week:
            name_of_the_day = days_name[birthday_to_check.weekday()]
            birthdays[name_of_the_day].append(user["name"])
        else:
            continue

    clean_list_of_birthdays = {}
    for key, value in birthdays.items():
        if len(value) > 0:
            clean_list_of_birthdays[key] = value

    return clean_list_of_birthdays


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")