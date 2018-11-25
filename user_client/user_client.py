import argparse
import json
import requests

url = 'http://printzz.herokuapp.com/'

def sign_in(username, password, need_register):
    # Send Request to Server
    data_json = {'username': username, 'password': password}
    if (need_register):
        resp_obj = requests.post(url+'register', json=data_json)  # Registration
    else:
        resp_obj = requests.post(url+'login', json=data_json)     # Login
    resp_json = resp_obj.json()

    # If Successful, Return the Key
    if (resp_json["status"]):
        print ("User Authenticated")
        return resp_json["data"]["user_id"]

    # Otherwise, End the Program
    else:
        print ("ERROR: " + resp_json['error'])
        exit()

def upload_file(key, file_in, double_sided, copies, color):

    # Upload File to Server
    params = { 'user_id': key }
    with open(file_in, 'rb') as file:
        files = {'input_file': file}
        res = requests.post(url + 'add_doc_file', files=files, params=params)

        # Exit on Error
        res_dict =  res.json()
        if res_dict['status'] is False:
            print ("ERROR: " + res_dict['error'])
            exit()

    # Upload Settings to Server
    params = { 'user_id': key }
    settings = {
       'double_sided': double_sided,
       'copies': copies,
       'color': color
    }
    res = requests.post(url + 'add_doc_settings', json=settings, params=params)

    # Exit on Error
    res_dict =  res.json()
    if res_dict['status'] is False:
        print ("ERROR: " + res_dict['error'])
        exit()

    # Notify If Upload Successful
    print ("File Upload Successful")


def main():
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-user", action="store")
    parser.add_argument("-pwd", action="store")
    parser.add_argument("-register", action="store_true")
    parser.add_argument("-file", action="store")
    parser.add_argument("-color", action="store_true")
    parser.add_argument("-copies", action="store", type=int)
    parser.add_argument("-double-sided", action="store")
    args = parser.parse_args()

    # Check That We Were Provided Username and Password
    if ( (args.user == None) or (args.pwd == None) ):
        print ("ERROR: Must Provide Login Information")
        exit()

    # Register or Sign the User In
    key = sign_in(args.user, args.pwd, args.register)


    ############################
    ###       ACTIONS        ###
    ############################

    # Upload File
    if (args.file != None):

        # Set Default Arguments if None Type
        double_sided = 0
        if args.double_sided == 'long-edge':
            double_sided = 1
        elif args.double_sided == 'short-edge':
            double_sided = 2
        copies = 1
        if args.copies is not None:
            copies = args.copies

        # Call Upload File Method
        upload_file(key, args.file, double_sided, copies, args.color)


if __name__ == "__main__":
    main()
