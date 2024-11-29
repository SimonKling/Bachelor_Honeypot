import os
import re
from datetime import datetime

def findIP(filename, start_time, end_time):
    found_ips = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        ip_pattern = re.compile(r'"remote_ip":\s*"(\d+\.\d+\.\d+\.\d+)"')
        timestamp_pattern = re.compile(r'"@timestamp":\s*"([\d\-T:Z]+)"')
        
        for line in lines:
            timestamp_match = timestamp_pattern.search(line)
            if timestamp_match:
                timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%dT%H:%M:%SZ")
                
                if start_time <= timestamp <= end_time:
                    ip_match = ip_pattern.search(line)
                    if ip_match:
                        ip_address = ip_match.group(1)
                        found_ips[ip_address] = found_ips.get(ip_address, 0) + 1

    sorted_ips = sorted(found_ips.items(), key=lambda x: x[1], reverse=True)
    return sorted_ips

def find_Ports(filename, ip, start_time, end_time):
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
                    ip_match = re.search(r'"remote_ip":\s*"' + re.escape(ip) + r'"', line)
                    if ip_match:
                        port_match = port_pattern.search(line)
                        if port_match:
                            port = port_match.group(1)
                            found_ports[port] = found_ports.get(port, 0) + 1

    sorted_ports = sorted(found_ports.items(), key=lambda x: x[1], reverse=True)
    return sorted_ports

def main():
    folder_path = 'raw_files'
    output_folder = 'test_output_files'
    os.makedirs(output_folder, exist_ok=True)
    
    #Timestamps
    
    start_time = datetime.strptime("2024-09-22T20:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
    end_time = datetime.strptime("2024-09-29T20:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            ips = findIP(filepath, start_time, end_time)
            
            output_file = os.path.join(output_folder, f"{filename}_summary.txt")
            with open(output_file, 'w') as f:
                
                
                f.write(f"Attack Count: {sum(count for count in ips)}\n")
                f.write("Top 10 IP addresses and their occurrences:\n")
                for ip, count in ips[:10]: 
                    f.write(f"{ip}\n")
                for ip, count in ips[:10]:
                    f.write(f"IP Address: {ip}, Occurrences: {count}\n")
                    ports = find_Ports(filepath, ip, start_time, end_time)
                    for port, occurrences in ports:
                        f.write(f"Port: {port}, Occurrences: {occurrences}\n")


main()
