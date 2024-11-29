import json
import os

def extractDionaeaData(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            source_ips = {}
            total_attacks = 0
            total_protocols = {}

            with open(os.path.join(input_folder, filename)) as f:
                for line in f:
                    data = json.loads(line)



                    #Timestamps
                    
                    if data['timestamp'] < "2024-09-22T20:00:00Z" or data['timestamp'] > "2024-09-29T20:00:00Z":
                        continue
                    
                    src_ip = data['src_ip']
                    protocol = data['connection']['protocol']

                    if src_ip not in source_ips:
                        source_ips[src_ip] = {}
                    
                    source_ips[src_ip][protocol] = source_ips[src_ip].get(protocol, 0) + 1
                    total_attacks += 1
                    total_protocols[protocol] = total_protocols.get(protocol, 0) + 1

            sorted_ips = sorted(source_ips.items(), key=lambda item: sum(item[1].values()), reverse=True)[:10]

            output_file_path = os.path.join(output_folder, f"{filename}_summary.txt")
            with open(output_file_path, 'w') as output_file:
                output_file.write(f"Overall Total Attacks: {total_attacks}\n\n")
                output_file.write("Top 10 Most Active Attackers:\n")

                for ip, protocols in sorted_ips:
                    output_file.write(f"{ip}\n")  


                for ip, protocols in sorted_ips:
                    total_ip_attacks = sum(protocols.values())
                    output_file.write(f"\nIP: {ip} - Total Attacks: {total_ip_attacks}\n")
                    for protocol, occurrences in protocols.items():
                        output_file.write(f"Protocol: {protocol}, Occurrences: {occurrences}\n")

                output_file.write("\nTotal Counts of All Targeted Protocols:\n")
                for protocol, count in total_protocols.items():
                    output_file.write(f"Protocol: {protocol}, Total Count: {count}\n")



input_folder = 'raw_files_dionaea'
output_folder = 'dionaea_reports'
extractDionaeaData(input_folder, output_folder)
