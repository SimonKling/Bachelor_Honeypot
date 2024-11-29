Due to Privacy Concerns, this data is not available publicly.


To make the pathcategorizers run you also need to get the BotPoke list (https://github.com/F5-Labs/topcves/tree/main/2024/08) and put it in ./WebBased/ directory

GALAH 

If you have permission to use the data extract data/Galah and put it into the Galah Directory

Run the go run extractor.go which will return the logs of Galah displayed as a .csv file


With These files the python pathCategorizerGalah.py can be run, however the file which should be investigated must be determined in line 
49 of the script 

python IPtoCountry.py - assigns the IP addresses to countries 

python IPtoASN.py


TANNER

If you have permission to use the data extract data/cloud_provider/instance_1_2/data/tanner/log, mkdir tanner_files and put the data there 

python extract_paths - Returns the paths targeted by adversaries, must be used for pathCategorizerTanner.py

python pathCategorizerTanner.py can be run 

IF Files not available use data displayed by KIBANA 