import os
import json
from datetime import datetime

def extract_and_count_paths(input_dir='tanner_files', output_dir='paths_tanner'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #  TIMESTAMPS
    start_time = datetime.strptime("2024-09-22 20:00", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime("2024-09-29 20:00", "%Y-%m-%d %H:%M")

    for file in os.listdir(input_dir):
        if not file.endswith('.json'):
            continue

        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, f"{file.split('.')[0]}_processed.json")

        path_counts = {}

        with open(input_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except Exception as e:
                    print(f"Error parsing line {i} in {file}: {e}")
                    continue

                timestamp_str = data.get('timestamp')
                if timestamp_str:
                    try:
                        timestamp = datetime.strptime(
                            timestamp_str, "%Y-%m-%dT%H:%M:%S.%f"
                        )
                    except ValueError:
                        try:
                            timestamp = datetime.strptime(
                                timestamp_str, "%Y-%m-%dT%H:%M:%S"
                            )
                        except ValueError:
                            continue

                    if not (start_time <= timestamp <= end_time):
                        continue

                path = data.get('path')
                if path:
                    path_counts[path] = path_counts.get(path, 0) + 1

        with open(output_path, 'w', encoding='utf-8') as out_f:
            json.dump(path_counts, out_f, indent=4)


extract_and_count_paths()
