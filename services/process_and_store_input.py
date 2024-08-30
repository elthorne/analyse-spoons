import json
import re

from datetime import datetime
from collections import defaultdict


def import_json(filename):
    with open(filename) as file:
        return json.load(file)


def get_valid_data_object(input):
    if isinstance(input, str):
        return json.loads(input)
    return input


def convert_name_to_date(input_str):
    date_match = re.search(r'---\w+\s(\d{1,2})[A-Z]{2}\s(\w+)\s*(\d{4})?---', input_str)
    if date_match:
        # Parse the extracted date into a datetime object
        day = date_match.group(1)
        month = date_match.group(2)
        year = "2023"  # Assuming the year is 2023, adjust if necessary

        # Construct the date string and convert it to a datetime object
        date_str = f"{day} {month} {year}"
        date_obj = f'{datetime.strptime(date_str, "%d %B %Y").date()}'
        return date_obj


def extract_card_data(data):
    cards = {}
    current_key = None
    total = 0

    for card in data['cards']:
        name = card.get('name')
        labels = card.get('labels', [])

        # If the card's name starts with "---", set it as the current key and reset the total
        if name.startswith("---"):
            # If there was a previous key, add the total before moving to the next one
            if current_key is not None:
                cards[current_key].append({'Total': total})

            current_key = convert_name_to_date(name)
            cards[current_key] = []
            total = 0  # Reset total for the new key

        elif current_key:
            # Append the card's name to the current key's list
            card_entry = {'name': name}

            # If labels are not empty, extract colors
            if labels:
                card_entry['colors'] = [label.get('color') for label in labels]

            cards[current_key].append(card_entry)

            # Update the total based on the current card's name
            total += extract_integers(name)

    # Add the total for the last key after the loop completes
    if current_key is not None:
        cards[current_key].append({'Total': total})

    return cards


def process_cards(input_file):
    raw_json_input = import_json(input_file)
    data = get_valid_data_object(raw_json_input)
    cards = extract_card_data(data)

    return cards


def extract_integers(text):
    match = re.search(r'\((\d+)\)', text)
    if match:
        return int(match.group(1))
    else:
        return 0


def save_dict_to_json(data, filename):
    """
    Converts a dictionary to a JSON string and saves it to a file.

    Parameters:
    encrypted_data (dict): The dictionary to convert to JSON.
    filename (str): The filename (with path) where the JSON file will be saved.
    """
    try:
        # Convert dictionary to JSON string
        json_string = json.dumps(data, indent=4, default=str)

        # Write the JSON string to a file
        with open(filename, 'w') as json_file:
            json_file.write(json_string)

        print(f"Dictionary successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the dictionary to JSON: {e}")
        raise


def extract_and_save_data_by_month(data):
    """
    Extracts encrypted_data by month from the given dictionary and saves it to JSON files.

    Parameters:
    encrypted_data (dict): The dictionary containing date keys and associated encrypted_data.
    """
    # Dictionary to hold encrypted_data grouped by month
    monthly_data = defaultdict(dict)

    for date, items in data.items():
        # Skip invalid keys such as None
        if date is None:
            continue

        # Extract year and month
        year, month, _ = date.split('-')
        month_key = f"{year}-{month}"

        # Add the encrypted_data to the corresponding month in the monthly_data dictionary
        monthly_data[month_key][date] = items

    # Save each month's encrypted_data to a JSON file
    for month, month_data in monthly_data.items():
        filename = f"encrypted_data/{month}-encrypted_data.json"
        save_dict_to_json(month_data, filename)