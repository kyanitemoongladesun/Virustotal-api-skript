import os
import vt

# Replace with your actual VirusTotal API key
API_KEY = ''

# Initialize the VirusTotal client
client = vt.Client(API_KEY)

# Replace 'path/to/file' with the actual path of the file you want to scan
file = 'path/to/file'

# Submit the file for scanning and wait for the scan to complete
client.scan_file(file,wait_for_completion=True)

# Close the VirusTotal client connection
client.close
