import argparse
import json
import requests

url = 'http://printzz.herokuapp.com/'

def sign_in(username, password, need_register):
    # Send Request to Server
    data_json = {'username': username, 'password': password}
    if (need_register):
        resp_obj = requests.post(url+'register', json=data_json)    # Registration
    else:
        resp_obj = requests.post(url+'login', json=data_json)       # Login
    resp_json = resp_obj.json()
    
    # If Registration Successful, Return Key
    if (resp_json["status"]):
        return resp_json["data"]["user_id"]
    
    # Otherwise, End the Program
    else:
        if (need_register):
            print ("ERROR: Account Could Not Be Created")
        else:
            print ("ERROR: Login Could Not Be Completed")
        exit()


def login_parser():
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-user", action="store")
    parser.add_argument("-pwd", action="store")
    parser.add_argument("-register", action="store_true")
    args = parser.parse_args()
    
    # Check That We Were Provided Username and Password
    if ( (args.user == None) or (args.user == None) ):
        print ("ERROR: Must Provide Login Information")
        exit()

    # Register or Sign the User In, Return Key
    return sign_in(args.user, args.pwd, args.register)

def upload_file(key):
    params = { 'user_id': key }
    with open('test.txt', 'rb') as file:
        files = {'input_file': file}

        res = requests.post(url + 'add_doc_file', files=files, params=params)
    
    params = { 'user_id': key }

    settings = {
        'double_sided': True,
        'copies': 19,
        'color': False
    }

    res = requests.post(url + 'add_doc_settings', json=settings, params=params)

    print(res.text)
    

def main():
    user_key = login_parser()
    upload_file(user_key)


if __name__ == "__main__":
    main()