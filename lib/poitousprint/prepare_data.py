import csv

with open('data/toflit18_all_flows.csv', newline='') as csv_reader_file:
    reader = csv.DictReader(csv_reader_file, quotechar='"')
    
    with open('data/toflit18_flows_sprint.csv', 'w', newline='') as csv_writer_file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csv_writer_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['year'] == '1789' and row['customs_region'] == 'La Rochelle':
                writer.writerow(row)


with open('data/navigo_all_flows_1789.csv', newline='') as csv_reader_file:
    reader = csv.DictReader(csv_reader_file, quotechar='"')
    
    with open('data/navigo_flows_sprint.csv', 'w', newline='') as csv_writer_file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csv_writer_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['source_subset'] == 'Poitou_1789':
                writer.writerow(row)
    
with open('data/navigo_all_pointcalls_1789.csv', newline='') as csv_reader_file:
    reader = csv.DictReader(csv_reader_file, quotechar='"')
    
    with open('data/navigo_pointcalls_sprint.csv', 'w', newline='') as csv_writer_file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csv_writer_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row['source_subset'] == 'Poitou_1789':
                writer.writerow(row)