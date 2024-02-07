import csv
import re
import json


def csv_to_json(csv_file, json_file):
    try:
        with open(csv_file, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            json_data = json.dumps(list(csv_reader), indent=4)
            with open(json_file, "w") as json_file:
                json_file.write(json_data)
        print(f"CSV file '{csv_file}' converted to JSON successfully: '{json_file}'")
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")


def extract_emails(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails = re.findall(pattern, text)
    return emails


def extract_phone_numbers(text):
    pattern = r"\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b"
    phone_numbers = re.findall(pattern, text)
    formatted_numbers = ["".join(groups) for groups in phone_numbers]
    return formatted_numbers


if __name__ == "__main__":
    text = """
    Contact us at support@example.com or call +123-456-7890. 
    You can also reach us at info@example.org.
    """
    emails = extract_emails(text)
    phone_numbers = extract_phone_numbers(text)
    print("Emails:", emails)
    print("Phone Numbers:", phone_numbers)

    csv_file = "data.csv"
    json_file = "data.json"
    csv_to_json(csv_file, json_file)
