import os
import time
import vt

# Replace with your actual VirusTotal API key
API_KEY = ''

# Initialize the VirusTotal client
client = vt.Client(API_KEY)

# Replace 'path/to/folder' with the actual path of the folder you want to scan
FOLDER_PATH = 'path/to/folder'


# Set rate limiting parameters
RATE_LIMIT = 4  # Maximum number of lookups per minute
LOOKUP_INTERVAL = 60 / RATE_LIMIT  # Time between lookups in seconds

# Set daily quota parameters
DAILY_QUOTA = 500  # Maximum number of lookups per day
LOOKUP_COUNT = 0  # Counter for number of lookups made today

#counts all files in Directory and Subdirectorys
num_files = len([f for f in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, f))])
print(f"Number of files in directory: {num_files}")
# Define a list to store the file paths of files larger than 650MB
large_files = []
# Initialize counters for scan results
TOTAL_SCANNED = 0
TOTAL_MALICIOUS = 0
malicious_files = []
def is_malicious():
    TOTAL_MALICIOUS += 1
    malicious_files.append((filename, analysis.stats['malicious']))

# Iterate through all files in folder
for root,dirs ,filenames in os.walk(FOLDER_PATH):
    for filename in filenames:
        filepath = os.path.join(root, filename)
        # Check if file is not a directory
        if os.path.isfile(filepath):
            try:
                # Check rate limiting and daily quota limits
                if LOOKUP_COUNT >= DAILY_QUOTA:
                    print("Daily quota reached. Exiting...")
                    break
                elif LOOKUP_COUNT % RATE_LIMIT == 0 and LOOKUP_COUNT > 0:
                    time.sleep(LOOKUP_INTERVAL)

                if (os.path.getsize(filepath) / (1024 * 1024)) >= 650:
                    large_files.append(filepath)
                else:
                    # Scan the file and wait for completion
                    with open(filepath, 'rb') as f:
                        analysis = client.scan_file(f, wait_for_completion=True)

                # Update counters for scan results
                TOTAL_SCANNED += 1
                if 'malicious' in analysis.stats and analysis.stats['malicious'] != 0:
                    is_malicious()

                # Print scan results
                print(f"{filename}:")
                print(f"Analysis ID: {analysis.id}")
                print(f"Status: {analysis.status}")
                if 'total' in analysis.stats:
                    print(f"Total number of engines: {analysis.stats['total']}")
                if 'malicious' in analysis.stats:
                    print(f"Number of engines that detected the file as malicious: {analysis.stats['malicious']}")
                for scan in analysis.results:
                    print(f"{scan}: {analysis.results[scan]['result']}")
                print(f"{TOTAL_SCANNED} of {num_files}")
                print('')

            except vt.error.APIError as e:
                # Handle API errors
                print(f"An error occurred while scanning {filename}: {e}")
             
# Close the VirusTotal client connection
client.close
# Print summary of scan results
print(f"Scanned {TOTAL_SCANNED} files.")
if TOTAL_MALICIOUS > 0:
    print(f"{TOTAL_MALICIOUS} files detected as malicious:")
    for filename, num_engines in malicious_files:
        print(f"{filename} ({num_engines} engines detected as malicious)")
else:
    print("No malicious files detected.")
# Print the list of large files at the end
if large_files:
    print("The following files are larger than 650MB:")
    for large_file in large_files:
        print(f"- {large_file}")
else:
    print("No files are larger than 650MB.")
print('All Scans Completed')
