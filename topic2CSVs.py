# This code used BagFileParser to get messages from a topic, flatten the objects and create CSV files 

import csv
import os
from BagFileParser import BagFileParser

def flatten_message(message, prefix='', flat_data=None):
    if flat_data is None:
        flat_data = {}
    
    fields = message.get_fields_and_field_types()
    
    for field, value in fields.items():
        full_field_name = f"{prefix}.{field}" if prefix else field
        sub_object = getattr(message, field)
        
        if hasattr(sub_object, 'get_fields_and_field_types'):
            # If it's a message with subfields, flatten it recursively
            flatten_message(sub_object, prefix=full_field_name, flat_data=flat_data)
        else:
            # If it's a simple value, add it to the flat data
            flat_data[full_field_name] = getattr(message, field)
            
    return flat_data

def accumulate_data(messages):
    accumulated_data = {}

    for timestamp, message in messages:
        flat_data = flatten_message(message)
        
        for field, value in flat_data.items():
            if field not in accumulated_data:
                accumulated_data[field] = []
            accumulated_data[field].append((timestamp, value))
    
    return accumulated_data

def topic2CSVs(bag_file, topic_name, output_dir = 'output_csv'):
    
    parser = BagFileParser(bag_file)
    msgs = parser.get_messages(topic_name)

    # Accumulate flattened data for each field across all messages
    accumulated_data = accumulate_data(msgs)

    # Create a directory to store CSV files
    os.makedirs(output_dir, exist_ok=True)

    # Write accumulated data to CSV files
    for field, values in accumulated_data.items():
        csv_file_path = os.path.join(output_dir, f"{field}.csv")
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', field])  # Write header

            for timestamp, value in values:
                writer.writerow([timestamp, value])

if __name__ == "__main__":
    
    bag_file = 'bag_files/2024_04_02__15_38_08_bag_test/2024_04_02__15_38_08_bag_test_0.db3'
    if os.path.isfile(bag_file):
        topic_name = '/emg_armband/emg'
        # topic_name = '/experiment_labels'
        topic2CSVs(bag_file, topic_name)
    else:
        print(f'File "{bag_file}" not found!')