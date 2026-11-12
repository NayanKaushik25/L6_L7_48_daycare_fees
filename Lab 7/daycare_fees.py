import math
def parse_enrolment(text):
    if not isinstance(text, str):
        return "", 0.0
    try:
        parts = text.split(':')
        if len(parts) != 2:
            return "", 0.0
        age_group, hours = parts
        age_group = age_group.strip()
        hours = float(hours)
        if not age_group or not math.isfinite(hours) or hours < 0:
            return "", 0.0
        return age_group.title(), hours
    except (ValueError, TypeError):
        return "", 0.0

def hours_average(hours_csv):
    if not isinstance(hours_csv, str):
        return 0
    try:
        values = [int(r.strip()) for r in hours_csv.split(',')]
        if not values:
            return 0
        return sum(values) // len(values)
    except (ValueError, TypeError):
        return 0

def payable_fee(text):
    if not isinstance(text, str):
        return 0.0
    try:
        parts = text.split('|')
        if len(parts) != 2:
            return 0.0
        fee, discount = parts
        fee = float(fee)
        discount = float(discount)
        if not math.isfinite(fee) or not math.isfinite(discount):
            return 0.0
        return max(fee * 1.18 - discount, 0)
    except (ValueError, TypeError):
        return 0.0


def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    print("Age Group and Hours:", result)

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    print("Average Hours:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
