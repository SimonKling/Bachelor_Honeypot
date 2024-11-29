# Bachelor's Thesis: Attacks on the Cloud

### **Unveiling Cyber Assaults on Cloud Infrastructure Through Honeypot Analysis**

---

## Repository Overview
This repository contains all the code developed and used for the bachelor's thesis.

---

## Viewing Data in the ELK Stack
To analyze the data using the ELK stack, follow these steps:

1. **Install T-Pot**  
   Clone and install T-Pot from its official repository:  
   [T-Pot GitHub Repository](https://github.com/telekom-security/tpotce)

2. **Reboot the System**  
   After installation, reboot your system to ensure proper setup.

3. **Stop the T-Pot Service**
   ```bash
   sudo systemctl stop tpot
   
4. **Replace Docker Compose**
   ```bash
   mv docker-compose-data-extraction.yaml ~/tpotce/docker-compose.yaml

6. **Copy Desired Data**
   ```bash
   Copy the data from the instance you wish to inspect into the ~/tpotce directory.

8. **Start Tpot**
   ```bash
   sudo systemctl start tpot
   

## Note
⚠️ Some datasets are unfortunately missing.
