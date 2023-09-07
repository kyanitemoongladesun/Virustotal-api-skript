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

# Define a list to store the file paths of files larger than 650MB
large_files = []
# Initialize counters for scan results
total_scanned = 0
total_malicious = 0
malicious_files = []
def is_malicious():
    total_malicious += 1
    malicious_files.append((filename, analysis.stats['malicious']))
    
# Iterate through all files in folder
for root,dirs ,filename in os.walk(folder_path):
    filepath = os.path.join(folder_path, filename)
    # Check if file is not a directory
    if os.path.isfile(filepath):
        if (os.path.getsize(file_path) / (1024 * 1024)) >= 650:
            large_files.append(filepath)
        else:
            # Scan the file and wait for completion
            with open(filepath, 'rb') as f:
                analysis = client.scan_file(f, wait_for_completion=True)

# Close the VirusTotal client connection
client.close

# Print the list of large files at the end
if large_files:
    print("The following files are larger than 650MB:")
    for large_file in large_files:
        print(f"- {large_file}")
else:
    print("No files are larger than 650MB.")
print('All Scans Completed')