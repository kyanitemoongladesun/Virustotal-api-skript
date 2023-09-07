import os
import vt

# Replace with your actual VirusTotal API key
API_KEY = ''

# Initialize the VirusTotal client
client = vt.Client(API_KEY)

# Replace 'path/to/folder' with the actual path of the folder you want to scan
file = 'path/to/folder'

#counts all files in Directory and Subdirectorys
num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

# Submit the file for scanning and wait for the scan to complete
client.scan_file(file,wait_for_completion=True)

# Close the VirusTotal client connection
client.close

print('All Scans Completed')