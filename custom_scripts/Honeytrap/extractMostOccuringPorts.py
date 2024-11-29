import os
import re
from datetime import datetime 


def find_Ports(filename, start_time, end_time):
    found_ports = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        port_pattern = re.compile(r'"local_port":\s*(\d+)')
        timestamp_pattern = re.compile(r'"@timestamp":\s*"([\d\-T:Z]+)"')
        
        
        
        for line in lines:
            timestamp_match = timestamp_pattern.search(line)
            if timestamp_match:
                timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%dT%H:%M:%SZ")
                
                if start_time <= timestamp <= end_time:
                        port_match = port_pattern.search(line)
                        if port_match:
                            port = port_match.group(1)
                            found_ports[port] = found_ports.get(port, 0) + 1

    sorted_ports = sorted(found_ports.items(), key=lambda x: x[1], reverse=True)
    return sorted_ports

def main():
    folder_path = 'raw_files'
    output_folder = 'output_files_ports'
    os.makedirs(output_folder, exist_ok=True)
    
        
    
    start_time = datetime.strptime("2024-09-22T20:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    end_time = datetime.strptime("2024-09-29T20:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            
            output_file = os.path.join(output_folder, f"{filename}_summary.txt")
            with open(output_file, 'w') as f:
                f.write("Top 5 IP addresses and their occurrences:\n")
                
               
                ports = find_Ports(filepath,  start_time, end_time)
                for port, occurrences in ports[:5]:
                    f.write(f"Port: {port}, Occurrences: {occurrences}\n")


main()
