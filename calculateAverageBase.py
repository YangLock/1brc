from collections import defaultdict


def create_result_dict():
    return {"min": float('inf'), "max": float('-inf'), "sum": 0.0, "count": 0}

def process_data(file_path):
    analysis_result = defaultdict(create_result_dict)
    with open(file_path, mode='r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            location, measurement = line.split(';')
            measurement = float(measurement)
            record = analysis_result[location]
            if record["min"] > measurement:
                record["min"] = measurement
            if record["max"] < measurement:
                record["max"] = measurement
            record["sum"] += measurement
            record["count"] += 1

    for location, measurement in sorted(analysis_result.items()):
        print(f"{location};{measurement['min']:.1f};{measurement['sum']/measurement['count']:.1f};{measurement['max']:.1f}")

if __name__ == "__main__":
    process_data("./measurements.txt")
