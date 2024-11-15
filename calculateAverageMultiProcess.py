from collections import defaultdict
import os
import multiprocessing as mp


def create_result_dict():
    return {"min": float('inf'), "max": float('-inf'), "sum": 0.0, "count": 0}

def get_file_chunks(file_path, num_chunks):
    """Split file into chunks"""
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // num_chunks

    chunks = []

    with open(file=file_path, mode='r', encoding="utf-8") as f:
        start_pos = 0
        for i in range(num_chunks):
            end_pos = start_pos + chunk_size - 1 if i < num_chunks - 1 else file_size - 1
            f.seek(end_pos)         # move the file pointer to the end_pos
            f.readline()            # if current file pointer is in the middle of a line, then move it to the end of the line
            end_pos = f.tell() - 1
            chunks.append((start_pos, end_pos))
            start_pos = end_pos + 1
        
    return chunks

def process_chunk(file_path, start_pos, end_pos):
    """process each chunk and save the result into a dict"""
    city_result = defaultdict(create_result_dict)

    # read file from each chunk's start to end
    with open(file=file_path, mode='r', encoding="utf-8") as f:
        f.seek(start_pos)
        while f.tell() <= end_pos:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            city, measure = line.split(';')
            measure = float(measure)
            city_measure = city_result[city]
            city_measure["min"] = min(city_measure["min"], measure)
            city_measure["max"] = max(city_measure["max"], measure)
            city_measure["sum"] += measure
            city_measure["count"] += 1
    
    return city_result

def merge(results):
    """merge each chunk's result"""
    analysis_result = defaultdict(create_result_dict)

    for result in results:
        for city, measure in result.items():
            record = analysis_result[city]
            record["min"] = min(record["min"], measure["min"])
            record["max"] = max(record["max"], measure["max"])
            record["sum"] += measure["sum"]
            record["count"] += measure["count"]
    
    return analysis_result


def process_file(file_path, max_cores):
    num_chunks = min(max_cores, mp.cpu_count())
    chunks = get_file_chunks(file_path, num_chunks)

    with mp.Pool(processes=num_chunks) as pool:
        results = pool.starmap(process_chunk, [(file_path, start_pos, end_pos) for start_pos, end_pos in chunks])
    
    result = merge(results)

    for city, measure in sorted(result.items()):
        print(f"{city};{measure['min']:.1f};{measure['sum']/measure['count']:.1f};{measure['max']:.1f}")
    

if __name__ == "__main__":
    process_file(file_path="./measurements.txt", max_cores=8)
