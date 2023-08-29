import os
import vt

API_KEY = ''
client = vt.Client(API_KEY)

file = 'path/to/file'

client.scan_file(file,wait_for_completion=True)


client.close