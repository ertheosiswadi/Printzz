# User Client

## Overview
Provides a command-line interface for all functionalities on the web-based <i>Printzz</i> GUI. May be helpful for testing.

## Usage
All login information must be entered as arguments on the command line. The arguments available to the user are:
+ <i>-user:</i> Follow with appropriate username.
+ <i>-pwd:</i> Follow with appropriate password.
+ <i>-register:</i> Include if the indicated user has not been registered before.
+ <i>-file:</i> Follow with relative path of file to be uploaded.

For instance, the following shell command would register a new user with the username "Test_User" and the password "Test_Password":

```$ python3 user_client.py -user Test_User -pwd Test_Password -register```

Once the user has been registered, we can use a similar command that excludes the -register argument in order to log in. The following just logs the user in, then exits.

```$ python3 user_client.py -user Test_User -pwd Test_Password```

Suppose we have a file <i>test.pdf</i> located in the current directory. We can upload the file to the server with the following command.

```$ python3 user_client.py -user Test_User -pwd Test_Password -file test.pdf```