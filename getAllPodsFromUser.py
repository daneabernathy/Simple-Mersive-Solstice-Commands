#This Application will ask the user if there is an updated list of solstice pods to work with
#If there are updates needed, it will ask the user for the location of the csv file with the list of pods. with their names, building, IP addresses, and MAC addresses
#It will then read the csv file and store the information in a dictionary
#If there are no updates needed it will read the dictionary and ask the user which pod they would like to work with with a building and pod selector, filtering on building
# we will import all the necessary libraries
import csv
import os
import webbrowser
import time
import pyautogui
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import simpledialog
from tkinter import scrolledtext
from tkinter import Menu

#This function will open the csv file and read the information into a dictionary
def read_csv_file(file_path):
    #initialize the dictionary
    pods = {}
    #open the csv file
    with open(file_path, mode='r') as file:
        #read the csv file
        csv_reader = csv.DictReader(file)
        #iterate through each row in the csv file
        for row in csv_reader:
            #store the information in the dictionary
            pods[row['Name']] = {'Building': row['Building'], 'IP Address': row['IP Address'], 'MAC Address': row['MAC Address']}
    #return the dictionary
    return pods

#This function will ask the user for the location of the csv file with the list of pods
def get_csv_file():
    #ask the user to select the csv file
    file_path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
    #return the file path
    return file_path

#This function will ask the user if there is an updated list of solstice pods to work with
def check_for_updates():
    #ask the user if there are updates needed
    answer = messagebox.askyesno('Update Pods', 'Are there updates needed for the list of Solstice Pods?')
    #return the answer
    return answer

#This function will ask the user which pod they would like to work with

def get_pod_from_user(pods):
    #create a list of buildings
    buildings = list(set([pod['Building'] for pod in pods.values()]))
    #create a list of pods
    pod_names = list(pods.keys())
    #create a list of buildings and pods
    building_pods = {building: [pod for pod in pod_names if pods[pod]['Building'] == building] for building in buildings}
    #ask the user to select a building
    building = simpledialog.askstring('Select Building', 'Select a building:', parent=root, initialvalue=buildings[0], list=buildings)
    #ask the user to select a pod
    pod = simpledialog.askstring('Select Pod', 'Select a pod:', parent=root, initialvalue=building_pods[building], list=building_pods[building])
    #return the pod
    return pod

#This function will open the web browser with the pod information
def open_pod_in_browser(pod, pods):
    #get the pod information
    pod_info = pods[pod]
    #get the IP address
    ip_address = pod_info['IP Address']
    #get the admin password
    admin_password = '*PASSWORD!'
    #produce the pod http link
    pod_link = f'http://{ip_address}/diag/logs.zip?password={admin_password}'
    #open the web browser with the pod link
    webbrowser.get('windows-default').open(pod_link)
    #wait for the web browser to open
    time.sleep(5)
    #close the web browser
    pyautogui.hotkey('ctrl', 'w')
    