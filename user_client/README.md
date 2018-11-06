# User Client

## Overview
Provides a command-line interface for all functionalities on the web-based <i>Printzz</i> GUI. May be helpful for testing.

## Usage
All login information must be entered as arguments on the command line. The arguments available to the user are:
+ <i>-user:</i> Follow with appropriate username.
+ <i>-pwd:</i> Follow with appropriate password.
+ <i>-register:</i> Include if the indicated user has not been registered before.

For instance, the following shell command would register a new user with the username "Test_User" and the password "Test_Password":

```$ python3 user_client.py -user Test_User -pwd Test_Password -register```

Once the user has been registered, we can use a similar command that excludes the -register argument in order to log in.

```$ python3 user_client.py -user Test_User -pwd Test_Password```

Currently the program will log in, and then upload a test file to the Heroku server. Additional functionality will be added soon.