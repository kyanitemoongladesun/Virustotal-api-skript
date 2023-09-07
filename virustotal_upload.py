import os
import vt
import time

# Replace with your actual VirusTotal API key
API_KEY = ''

# Initialize the VirusTotal client
client = vt.Client(API_KEY)

# Replace 'path/to/folder' with the actual path of the folder you want to scan
folder_path = ''


# Set rate limiting parameters
RATE_LIMIT = 4  # Maximum number of lookups per minute
LOOKUP_INTERVAL = 60 / RATE_LIMIT  # Time between lookups in seconds

# Set daily quota parameters
DAILY_QUOTA = 500  # Maximum number of lookups per day
lookup_count = 0  # Counter for number of lookups made today

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
        try:
            # Check rate limiting and daily quota limits
            if lookup_count >= DAILY_QUOTA:
                print("Daily quota reached. Exiting...")
                break
            elif lookup_count % RATE_LIMIT == 0 and lookup_count > 0:
                time.sleep(LOOKUP_INTERVAL)

            if (os.path.getsize(file_path) / (1024 * 1024)) >= 650:
                large_files.append(filepath)
            else:
                # Scan the file and wait for completion
                with open(filepath, 'rb') as f:
                    analysis = client.scan_file(f, wait_for_completion=True)

            # Update counters for scan results
            total_scanned += 1
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
            print(f"{total_scanned} of {num_files}")
            print('')

        except vt.error.APIError as e:
            # Handle API errors
            print(f"An error occurred while scanning {filename}: {e}")
             
# Close the VirusTotal client connection
client.close
# Print summary of scan results
print(f"Scanned {total_scanned} files.")
if total_malicious > 0:
    print(f"{total_malicious} files detected as malicious:")
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