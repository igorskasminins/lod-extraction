import os
import csv

# Path to the directory containing the output files
output_directory = "./responses"

# Path to your CSV file
csv_file = "./extraction_statistics_output.csv"

def find_extra_files(csv_file, output_directory):
    csv_files_set = set()

    # Extracting filenames from CSV
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            output_file = row['Output File']
            csv_files_set.add(output_file + '.json')

    # Finding extra files in the directory
    extra_files = []
    for filename in os.listdir(output_directory):
        if filename not in csv_files_set:
            extra_files.append(filename)

    return extra_files

extra_files = find_extra_files(csv_file, output_directory)

if extra_files:
    print("Extra files found in the directory:")
    for file in extra_files:
        print(file)
else:
    print("No extra files found in the directory.")
