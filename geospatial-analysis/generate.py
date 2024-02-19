import csv
import random


def generate_synthetic_data(num_points, output_file):
    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["latitude", "longitude"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(num_points):
            latitude = random.uniform(40.0, 41.0)
            longitude = random.uniform(-100.0, -99.0)
            writer.writerow({"latitude": latitude, "longitude": longitude})


generate_synthetic_data(1000, "synthetic_data.csv")
