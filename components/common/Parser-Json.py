import json
import re
import csv

def extract_large_numbers_after_string_corrected(data, search_string, min_digits=2, case_insensitive=True):
    """
    Extracts Room Size
    Extracts all numbers with a minimum number of digits that immediately follow a specific string in a nested JSON structure.
    The search is not case-sensitive.
    """
    numbers = []

    def extract_from_string(s):
        flags = re.IGNORECASE if case_insensitive else 0
        pattern = rf"{re.escape(search_string)}\s+(\d{{{min_digits},}})"
        return re.findall(pattern, s, flags)

    if isinstance(data, dict):
        for value in data.values():
            numbers.extend(extract_large_numbers_after_string_corrected(value, search_string, min_digits, case_insensitive))

    elif isinstance(data, list):
        for item in data:
            numbers.extend(extract_large_numbers_after_string_corrected(item, search_string, min_digits, case_insensitive))

    elif isinstance(data, str):
        found_numbers = extract_from_string(data)
        numbers.extend([int(num) for num in found_numbers])
    
    return numbers

def extract_large_numbers_between_strings(data, start_string, end_string, min_digits=3, case_insensitive=True):
    """
    Extracts Rent Price
    Extracts all numbers with a minimum number of digits that are found between two specified strings in a nested JSON structure.
    The search is not case-sensitive.
    """
    numbers = []

    def extract_from_string(s):
        flags = re.IGNORECASE if case_insensitive else 0
        pattern = rf"{re.escape(start_string)}\s+(.*?)\s+{re.escape(end_string)}"
        matches = re.findall(pattern, s, flags)
        return [num for match in matches for num in re.findall(r'\b\d{3,}\b', match)]

    if isinstance(data, dict):
        for value in data.values():
            numbers.extend(extract_large_numbers_between_strings(value, start_string, end_string, min_digits, case_insensitive))

    elif isinstance(data, list):
        for item in data:
            numbers.extend(extract_large_numbers_between_strings(item, start_string, end_string, min_digits, case_insensitive))

    elif isinstance(data, str):
        found_numbers = extract_from_string(data)
        numbers.extend([int(num) for num in found_numbers])
    
    return numbers

def extract_room_size_and_final_price(json_files, room_size_string, start_string, end_string, min_digits=2):
    """
    For a list of JSON files, extracts the room size and final price information and writes it to a CSV file.
    """
    csv_data = []

    for file_path in json_files:
        with open(file_path, 'r') as file:
            data = json.load(file)

            # Extract room size (case insensitive)
            room_size = extract_large_numbers_after_string_corrected(data, room_size_string, min_digits, case_insensitive=True)
            room_size_value = room_size[-1] if room_size else None

            # Extract final price (case insensitive)
            final_price = extract_large_numbers_between_strings(data, start_string, end_string, min_digits, case_insensitive=True)
            final_price_value = final_price[-1] if final_price else None

            # Append to CSV data
            csv_data.append([room_size_value, final_price_value])

    # Writing data to CSV
    csv_file_path = 'extracted_data.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Room Size', 'Final Price'])
        writer.writerows(csv_data)

    return csv_file_path

# file paths 
json_files_example = ['conversation1.json', 'conversation2.json','conversation3.json']

# usage
csv_file_path = extract_room_size_and_final_price(json_files_example, "room size is", "I believe a price of", "euros per month is fair")
csv_file_path
