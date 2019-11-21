import csv, re

def extract_data():
    # Ignore the first two lines of the source file.
    # Transform header labels into prettier format by removing underscores and
    #   using title case.
    # Transpose the data format from wide format to tall, skinny table.
    # End goal: 1 row per state per data point type per time period
    population_change_input_file_path = './input/pop_change.csv'
    label_row_number = 3
    ignore_lines_start = 4
    ignore_lines_end = 8
    ignore_lines = range(ignore_lines_start, ignore_lines_end + 1)
    label_dict = {}
    output_data = []

    with open(population_change_input_file_path, newline='') as csv_file:
        file_reader = csv.reader(csv_file, delimiter=',')
        current_row_number = 1

        for row in file_reader:
            current_field_number = 1

            # Create a dictionary out of the labels in the header row
            if(current_row_number == label_row_number):
                for field in row:
                    label_dict[current_field_number] = transform_label(field)
                    current_field_number += 1

            # Process the data rows
            if(current_row_number > label_row_number and current_row_number not in ignore_lines):
                current_field_number = 1
                current_state_name = row[0]

                # Process the data points
                for field in row:
                    if(current_field_number > 1):
                        current_label = label_dict[current_field_number]
                        current_data_point_type = extract_data_point_type_from_label(current_label)
                        current_data_point_year = extract_year_from_label(current_label)
                        current_data_point_dict = {}
                        current_data_point_dict['State Name'] = current_state_name
                        current_data_point_dict['Data Point Type'] = current_data_point_type
                        current_data_point_dict['Data Point Time Period'] = current_data_point_year
                        current_data_point_dict['Data Point Value'] = field
                        output_data.append(current_data_point_dict)

                    current_field_number += 1

            current_row_number += 1

    headers = [
        'State Name',
        'Data Point Type',
        'Data Point Time Period',
        'Data Point Value'
    ]
    write_data_to_csv(headers, output_data, './output/usa-states-population-change.csv')

def extract_year_from_label(label):
    match = re.search('^\d+', label)
    year = match.group(0)
    year = int(year)

    return year

def extract_data_point_type_from_label(label):
    year_text_length = len(str(extract_year_from_label(label)))
    data_point_type = label[year_text_length + 1:]

    return data_point_type

def transform_label(text):
    new_label = text.replace('_', ' ')
    new_label = new_label.title()
    new_label = new_label.replace('Change', 'Population Change')

    return new_label

def write_data_to_csv(header_list, data_list_of_dicts, output_file_path):
    with open(output_file_path, 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=header_list)
        writer.writeheader()
        writer.writerows(data_list_of_dicts)

extract_data()
