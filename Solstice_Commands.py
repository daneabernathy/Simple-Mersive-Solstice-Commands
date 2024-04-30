from __future__ import print_function
import pyautogui
from tkinter import *
from tkinter import ttk
import sys
from sys import version
import time
import datetime
import requests
import pdb
import itertools
import pyautogui
import webbrowser


#Function to get screen key and pod name and keep them in variables
#Function also opens a web browser with the user IP address
def get_pod_info(*args):
    try:
        #get IP address from user
        value = ip_address.get()
        
        #set password for pod - comment out if there is no password
        admin_password = '*PASSWORD!'
        
        #URL to get config info from pod
        myconfigurl = 'http://'+value+'/api/config?password='+admin_password
        
        #json headers
        headers = {'content-type': 'application/json'}
        
        #GET from pod
        rc = requests.get(myconfigurl, headers = headers)
        
        #parse json to lib
        rconfig = rc.json()
        
        #parse screen code from lib
        screen_code.set(int(rconfig.get('m_authenticationCuration',{}).get('sessionKey')))
        
        #parse pod name from lib
        podname.set(rconfig.get('m_displayInformation',{}).get('m_displayName'))


    except ValueError:
        pass

def connect_to_pod(*args):
    try:
        #get IP address from user
        value = ip_address.get()
        
        #produce pod http link from user IP address
        pod_screen_code_link = 'https://'+value+':6443'

        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_screen_code_link)  

    except ValueError:
        pass

def pod_look_in(*args):
    try:
        #get IP address from user
        value = ip_address.get()

        admin_password = '*PASSWORD!'

        #URL to get config info from pod
        myconfigurl = 'http://'+value+'/api/config?password='+admin_password
        
        #json headers
        headers = {'content-type': 'application/json'}
        
        #GET from pod
        rc = requests.get(myconfigurl, headers = headers)
        
        #parse json to lib
        rconfig = rc.json()

        #parse screen code from lib
        screen_code.set(int(rconfig.get('m_authenticationCuration',{}).get('sessionKey')))
      
        #produce pod http link from user IP address
        pod_lookin_link = 'http://'+value+'/Look-in'
# ?Key='+screen_code.get()
        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_lookin_link)  

    except ValueError:
        pass

def pod_reboot(*args):
    try:
        #get IP address from user
        value = ip_address.get()

        admin_password = '*PASSWORD!'
        
        #produce pod http link from user IP address
        pod_reboot_link = 'http://'+value+'/api/control/reboot?password='+admin_password

        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_reboot_link)
        
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'w')

    except ValueError:
        pass


def pod_boot_users(*args):
    try:
        #get IP address from user
        value = ip_address.get()

        admin_password = '*PASSWORD!'
         
       #produce pod http link from user IP address
        pod_boot_users_link = 'http://'+value+'/api/control/boot?password='+admin_password

        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_boot_users_link)

        time.sleep(5)
        pyautogui.hotkey('ctrl', 'w')

    except ValueError:
        pass


def pod_clear(*args):
    try:
        #get IP address from user
        value = ip_address.get()

        admin_password = '*PASSWORD!'
        
        #produce pod http link from user IP address
        pod_clear_link = 'http://'+value+'/api/control/clear?password='+admin_password

        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_clear_link)

        time.sleep(5)
        pyautogui.hotkey('ctrl', 'w')

    except ValueError:
        pass

    
def pod_restart(*args):
    try:
        #get IP address from user
        value = ip_address.get()

        admin_password = '*PASSWORD!'
        
        #produce pod http link from user IP address
        pod_restart_link = 'http://'+value+'/api/control/restart?password='+admin_password

        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_restart_link)

        time.sleep(5)
        pyautogui.hotkey('ctrl', 'w')

    except ValueError:
        pass

def get_logs(*args):
    try:
        #get IP address from user
        value = ip_address.get()

        admin_password = '*PASSWORD!'
        
        #produce pod http link from user IP address
        pod_logs = 'http://'+value+'/diag/logs.zip?password='+admin_password

        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_logs)

        time.sleep(5)
        pyautogui.hotkey('ctrl', 'w')

    except ValueError:
        pass

def set_edid_1080p(*args):
    try:
        #get IP address from user
        value = ip_address.get()

        admin_password = '*PASSWORD!'
        
        #produce pod http link from user IP address
        pod_edid_1080p = 'http://'+value+'/diag/displaymode?mode=16?password='+admin_password

        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_edid_1080p)

        time.sleep(5)
        pyautogui.hotkey('ctrl', 'w')
        
    except ValueError:
        pass

def pod_key_reset(*args):
    try:
        #get IP address from user
        value = ip_address.get()

        admin_password = '*PASSWORD!'
        
        #produce pod http link from user IP address
        pod_key_reset_link = 'http://'+value+'/api/control/resetkey?password='+admin_password

        #open web browser with url for pod
        webbrowser.get('windows-default').open(pod_key_reset_link)

        time.sleep(5)
        pyautogui.hotkey('ctrl', 'w')
        
    except ValueError:
        pass
        
root = Tk()
root.title("Solstice Pod Info and Commands")

mainframe = ttk.Frame(root, padding="20 20 20 20")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ip_address = StringVar()
ip_address_entry = ttk.Entry(mainframe, width=15, textvariable=ip_address)
ip_address_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Button(mainframe, text="Get Pod Info", command=get_pod_info).grid(column=3, row=1, sticky=W)
ttk.Button(mainframe, text="Connect to Pod", command=connect_to_pod).grid(column=4, row=1, sticky=W)
ttk.Button(mainframe, text="Browser Look In", command=pod_look_in).grid(column=5, row=1, sticky=W)
ttk.Label(mainframe, text="Pod Commands:").grid(column=4, row=2, sticky=W)
ttk.Button(mainframe, text="Reboot Pod", command=pod_reboot).grid(column=4, row=3, sticky=W)
ttk.Button(mainframe, text="Clear All Posts", command=pod_clear).grid(column=4, row=4, sticky=W)
ttk.Button(mainframe, text="Reset Screen Key", command=pod_key_reset).grid(column=4, row=5, sticky=W)
ttk.Button(mainframe, text="Software Restart", command=pod_restart).grid(column=5, row=4, sticky=W)
ttk.Button(mainframe, text="Boot All Users", command=pod_boot_users).grid(column=5, row=3, sticky=W)
ttk.Button(mainframe, text="Get Pod Logs", command=get_logs).grid(column=4, row=6, sticky=W)
ttk.Button(mainframe, text="Set Pod EDID to 1080p", command=set_edid_1080p).grid(column=5, row=5, sticky=W)

podname = StringVar()
ttk.Label(mainframe, textvariable=podname).grid(column=2, row=2, sticky=(W, E))

screen_code = StringVar()
ttk.Label(mainframe, textvariable=screen_code).grid(column=2, row=3, sticky=(W, E))

screen_code_string = str(screen_code)

ttk.Label(mainframe, text="Enter the pod's IP address:").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="The Pod name is:").grid(column=1, row=2, sticky=W)                                                                        
ttk.Label(mainframe, text="The Screen Code is:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="If a three digit number is returned,\nadd a 0 to the front of the code").grid(column=2, row=4, sticky=W)
ttk.Label(mainframe, text="All Pod Commands will open a new\ntab in your default web browser").grid(column=2, row=5, sticky=W)
ttk.Label(mainframe, text="When the tab opens, please wait until you\nsee the tab close itself before you continue").grid(column=2, row=6, sticky=W)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

ip_address_entry.focus()
root.bind("<Return>", get_pod_info)

root.mainloop()
