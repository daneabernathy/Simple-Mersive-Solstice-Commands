# solstice_commands
Some solstice commands done through Python

This is a python program to get info from a solstice pod on your network and to send basic commands to the pod.

The only variable that needs to be changed is the admin_password. If there is no password on the pod, comment out the line.

When sending commands it will open the URL in a new tab of the Windows default browser.
It will then close the tab after 5 seconds to ensure the command was passed.
Some commands stay on an infinite loop if you do not close the tab.
