import json
import requests
import subprocess
import time
import urllib

url = 'http://printzz.herokuapp.com/'
refresh_time = 2
print_time = 30

def poll_server():    
    # Check if There is a File Ready to Print
    settings_obj = requests.get(url+'get_doc_settings')
    settings = settings_obj.json()
    
    # Return to Loop if No File Exists
    if (settings['status'] == False):
        return

    # File Exists, So Download the Actual File
    doc_obj = urllib.request.urlopen(url+'get_doc')
    doc = doc_obj.read()

    # Check For Common File Headers
    extension = ""
    if ( (doc[0] == 80) and (doc[1] == 75) ):                # DOCX
        extension = "docx"
    elif ("%PDF-" in doc.splitlines()[0].decode('ascii')):   # PDF
        extension = "pdf"
    else:                                                    # TXT
        extension = "txt"

    # Write File to Disk
    f = open("print."+extension, "wb")
    f.write(doc)
    f.close

    # TODO Check If .docx can be printed directly, or need to convert

    # Generate Print Command Based on Provided Options
    print_cmd = "lp print." + extension + " -n "
    print_cmd += str(settings['data']['copies']) + " "      # Number of Copies
    if (settings['data']['double_sided']):                  # Double-Sided
        print_cmd += "-o sides=two-sided-long-edge "
    #TODO Need Printer-Specific Option for Setting Color
    
    # Issue Print Command to the System
    #subprocess.call(print_cmd, shell=True)
    print (print_cmd)

    # Perform Cleanup
    #subprocess.call('rm -f print.*', shell=True)
    #requests.get(url+'pop_doc')
    
def main():
    # Delete Any Existing Print Files
    subprocess.call('rm -f print.*', shell=True)

    # Continuously Poll the Server, Printing Any Files Found
    while (True):
        poll_server()
        time.sleep(refresh_time)


if __name__ == "__main__":
    #main()
    poll_server()