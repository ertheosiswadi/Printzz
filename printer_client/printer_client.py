import json
import requests
import subprocess
import time
import urllib

url = 'http://printzz.herokuapp.com/'
refresh_time = 2
print_time = 30

def main():
    # Delete Any Existing Print Files
    subprocess.call('rm -f print*', shell=True)
    
    # Check if There is a File Ready to Print
    doc_obj = urllib.request.urlopen(url+'get_doc')
    doc = doc_obj.read()
    
    # Restart Loop if No File Exists
    if ("{\"status\":false}" in doc.decode('ascii')):
        exit()

    # Check For Common File Headers
    extension = ""
    if ("%PDF-" in doc.splitlines()[0].decode('ascii')):   # PDF
        extension = "pdf"
    else:                                                  # TXT
        extension = "txt"

    # Write File to Disk
    f = open("print."+extension, "wb")
    f.write(doc)
    f.close

    # Send to the Printer
    

if __name__ == "__main__":
    main()