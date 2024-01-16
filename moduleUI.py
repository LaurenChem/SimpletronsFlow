#Import User Interface Library 
from tkinter import *


#Database
import sqlite3
from sqlite3 import Error

#START UP GUI
from tkinter.ttk import Combobox
import tkinter as tk    
from tkinter import ttk

from opentrons import robot, containers, instruments
import opentrons

#Import RE
import re

#Import threading
import threading

#Custom module Imports
from moduleContainers import *
from moduleCommands import *
from moduleCalibrate import *
from modulePipetting import *
from moduleProtocol import *
from moduleClass import *

## OS Path
import os.path
###########################################################################################################

# Python TK Graphical Interface Note: [Run on Start]
# Note: This Is Only UI Section (If you want to expand or start from scratch use other python script such as
# moduleProtocol, moduleCommands, moduleCalibrate)

###########################################################################################################



###########################################################################################################
#
# Start Up Command
#
###########################################################################################################
#connect()
create_connection()

###########################################################################################################
#
# Start UI
#
###########################################################################################################
root = Tk()
root.title('Simpletrons - OT')
#root.configure(bg="#96c4c3")
#root.geometry("740x400")
#root.pack_propagate(0)

#Setup Windows Location (Center Top Left Corner)
windowWidth = root.winfo_reqwidth() 
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/4 - windowWidth/4)
positionDown = int(root.winfo_screenheight()/4 - windowHeight/4)
root.geometry("+{}+{}".format(positionRight, positionDown))

###########################################################################################################

###########################################################################################################
#
# Global Variable 
#
###########################################################################################################
# Remember to verify the custom container exist before adding into this container list to reduce errors

shortcuts_list = ['Simple_Transfer', 'One_to_Many', 'Mixing']
container_list = [ '','point', 'tiprack-10ul', 'tiprack-200ul', 'tiprack-1000ul', '96-flat', 
                    '96-PCR-flat', '96-PCR-tall',  '96-deep-well', '48-well-plate', '24-well-plate',
                   'custom'
                   ]
loaded_pipette_list = ['','']
loaded_container_type = []
loaded_containers = []
count_CT = 0
count_CTT = 0
count_C = 0



###########################################################################################################

###########################################################################################################
#
# Class Tool Tip
#
###########################################################################################################
wraplength=200
###########################################################################################################



###########################################################################################################

###########################################################################################################
#
# Update Position Pipetting 
#
###########################################################################################################


position_display_xx = StringVar()

position_display_x = StringVar()
position_display_y = StringVar()
position_display_z = StringVar()



def update_position_display():
    """ Update Graphic Position """
    global position_display_x
    global position_display_y
    global position_display_z
    global robot

    position=list(robot._driver.get_head_position()["current"]) 

    position_display_x = ("X:", position[0])
    position_display_y = ("Y:", position[1])
    position_display_z = ("Z:", position[2])

def update_position_display_x():
    """ Update Pipette Position"""
    """ Require more - testing """
    global position_display_xx
    global pipette_a
    global pipette_b
    global plungerPos

    pip = varpip.get()
    plungerTarget = pippos.get()

    #if pip == "pipette_b":
    #    plungerPos = pipette_b._get_plunger_position(plungerTarget)

    #if pip == "pipette_a":
    #     plungerPos = pipette_a._get_plunger_position(plungerTarget)

    #plungerPos = pipette.get_plunger_position(plungerTarget)

    #position_display_xx = ("X:", plungerPos)



###########################################################################################################

###########################################################################################################
#
# Update Container and Pipetting
#
###########################################################################################################


def update_containers_list_type():
    """ Update Type of containers loaded """
    global loaded_container_type
    global count_C

    for name, container in robot.get_containers():
        loaded_container_type.append(count_C)
        loaded_container_type[count_C]= name
        count_C = count_C + 1

    #Sort List
    loaded_container_type = sorted(loaded_container_type)
    print('Loaded Container Type:', loaded_container_type)

def update_containers_list(name):
    """ Update Loaded Container List """
    global loaded_containers
    global count_CT

    loaded_containers.append(count_CT)
    loaded_containers[count_CT]= name
    count_CT = count_CT + 1

#Update Loaded Pipette List
def update_pipette(name, num):
    loaded_pipette_list[num]= name

#Update Tip Rack List in Setup Pipette
def update_dropdown_tip_rack():
    list = loaded_containers
    dropdown_tip_rack['values'] = list
    print('Updating Drop-down List: tip rack pipette setup')

#Update Tip Rack List in Setup Pipette
def update_dropdown_trash():
    list = loaded_containers
    dropdown_trash['values'] = list
    print('Updating Drop-down List: trash pipette setup')

#Update Pipette in Pipette Dropdown
def update_dropdown_pip():
    list = loaded_pipette_list
    dropdown_cpip['values'] = list
    print('Updating Drop-down List: Pipette pipette calibrate')
    calibration_mode_toggle(1)

#Update Pipette in Calibration Dropdown
def update_dropdown_pip_c():
    list = loaded_pipette_list
    dropdown_varpip_c['values'] = list
    print('Updating Drop-down List: Pipette container calibrate')
    calibration_mode_toggle(1)
#Update Container in Calibration Dropdown
def update_dropdown_con_c():
    list = loaded_containers
    dropdown_varcon_c['values'] = list
    print('Updating Drop-down List: containers containers calibrate')
    calibration_mode_toggle(1)

def update_dropdown_pos():
    calibration_mode_toggle(1)


###########################################################################################################

###########################################################################################################
#
# PRE LOAD
#
###########################################################################################################
count_preload_c = 0
count_preload_p = 0

# Load Pre Configured Workspace
def load_pre_workspace(): #For Testing

    global count_preload_c

    if count_preload_c == 0:
        #load_container('A3', 'A3', 'trash-box')
        #insert = ('A3', 'trash-box', 'A3')
        #save_data("custom_workspace", insert)

        #load_container('A2', 'A2', 'tiprack-1000ul')
        #insert = ('A3', 'tiprack-1000ul', 'A3')
        #save_data("custom_workspace", insert)

        #load_container('B2', 'B2', 'tiprack-100ul')
        insert = ('B2', 'tiprack-1000ul', 'B2')
        #save_data("custom_workspace", insert)

        #load_container('A1', 'A1', '24-well-plate')
        insert = ('A1', '24-well-plate', 'A1')
        #save_data("custom_workspace", insert)

        #load_container('B1', 'B1', '48-well-plate')
        insert = ('B1', '48-well-plate', 'B1')
        #save_data("custom_workspace", insert)

        #load_container('A3', 'A3', 'point')
        insert = ('B2', 'point', 'B2')
        #save_data("custom_workspace", insert)


        #update_containers_list('C1_trash-box')
        update_containers_list('A2_tiprack-1000ul')
        #update_containers_list('A3_tiprack-1000ul')
        update_containers_list('A1_24-well-plate')
        update_containers_list('B1_48-well-plate')
        update_containers_list('B2_point')


        temp = robot.containers()
        print("Robot Loaded Container List:", temp)

        confirmation_box(6)
        count_preload_c = count_preload_c + 1
    

# Load Pre Configured PIp
def load_pre_pip(): #For Testing
    global count_preload_p

    if count_preload_p == 0:
        #loadpipette ('a', 1000, 100, 800, 1200, 'B1', 'A2')
        insert = ('a', '1000', '100', '1', 600, 800, 'A3_tiprack-1000ul', 'B2_point')
        save_data("custom_pipette", insert) 
        update_pipette('pipette_a', 1)
        #loadpipette ('b', 1000, 100, 800, 1200, 'B2', 'A2')
        insert = ('b', '1000', '100', '1', 600, 800, 'A2_tiprack-1000ul', 'B2_trash-box')
        save_data("custom_pipette", insert) 
        update_pipette('pipette_b', 0)
        confirmation_box(7)
        count_preload_p = count_preload_p + 1

###########################################################################################################

###########################################################################################################
#
# Function Link for Calibration
#
###########################################################################################################


#
#Pipette Control
#
def save_pip_action():
    ''' Save Calibration  Pipette'''
    ''' Grab Value from combo box and send to save calibration'''
    pip = varpip.get()
    pos = pippos.get()

    print(pip)
    print(pos)

    saveCalibrationPip(pip, pos)
    confirmation_box(4)

def move_pip_action_up():
    """ Send Pipette Down """
    pip = varpip.get()
    speed = head_speed_p.get()

    ControlPlugger(pip, 'z_up', speed)
    update_position_display_x()

def move_pip_action_down():
    """ Send Pipette Down """
    pip = varpip.get()
    speed = head_speed_p.get()

    ControlPlugger(pip, 'z_down', speed)
    update_position_display_x()

def move_prepip_action():
    """ Send Pipette Pre-Configured Position Command """
    pip = varpip.get()
    plunger = pippos.get()

    moveDefaultLocation_p(pip, plunger)

def move_pip_action_home():
    """ Send Pipette Home Command """
    pip = varpip.get()
    pip_action_home(pip)

##
# Robot Control for calibration
##
def move_x_neg():
    """ Move Robot X Negative"""
    try:
        speed = head_speed_a.get()
        changeDirectionSpeed(speed)
        calibrationControl('x_left')
        update_position_display()
    except:
        print("[K1-XP] Keyboard Input Not Accepted At this Stage") 
    

def move_x_pos():
    """ UI Link to Calibrate Control"""
    try:
        speed = head_speed_a.get()
        changeDirectionSpeed(speed)
        calibrationControl('x_right')
        update_position_display()
    except:
        print("[K1-XP] Keyboard Input Not Accepted At this Stage") 

def move_y_neg():
    try:
        speed = head_speed_a.get()
        changeDirectionSpeed(speed)
        calibrationControl('y_down')
        update_position_display()
    except:
        print("[K1-YN] Keyboard Input Not Accepted At this Stage") 

def move_y_pos():
    try:
        speed = head_speed_a.get()
        changeDirectionSpeed(speed)
        calibrationControl('y_up')
        update_position_display()
    except:
        print("[K1-YP] Keyboard Input Not Accepted At this Stage")  


def move_z_neg():
    try:
        speed = head_speed_a.get()
        changeDirectionSpeed(speed)
        calibrationControl('z_down')
        update_position_display()
    except:
        print("[K1-ZN] Keyboard Input Not Accepted At this Stage") 

def move_z_pos():
    try:
        speed = head_speed_a.get()
        changeDirectionSpeed(speed)
        calibrationControl('z_up')
        update_position_display()
    except:
        print("[K1-ZP] Keyboard Input Not Accepted At this Stage")  

def home_axis():
    calibrationControlHome()

def save_containers_calibration():
    """
    Save Container Calibration
    """
    pip = varpip.get()
    con = c_varcon.get()
    
    contype = con[3:]
    con = con[0:2]
    

    saveCalibration(pip, con, contype)

    confirmation_box(5)


def load_axis():

    pip = varpip.get()
    con = c_varcon.get()
    
    print("Before:", con)
    contype = con[3:]
    con = con[0:2]
    print(con)

    moveDefaultLocation_C(pip, con, contype)


# Setup Workspace
def setup_workspace():
    """ Setup Workspace Function Link"""

    #Reset Counter
    global count_C
    global count_CT
    global robot

    count_CT = 0

    loaded_containers.clear()
    robot.reset() # Reset Containers

    if A1_W.get() != '':
        print('Entry Found in A1')
        AA = 'A1_'+str(A1_W.get())
        BB = A1_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('A1', 'A1', BB)
        #insert = ('A1', BB, 'A1')
        #save_data("custom_workspace", insert)

    if A2_W.get() != '':
        print('Entry Found in A2')
        AA = 'A2_'+str(A2_W.get())
        BB = A2_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('A2', 'A2', BB)
        #insert = ('A2', BB, 'A2')
        #save_data("custom_workspace", insert)

    if A3_W.get() != '':
        print('Entry Found in A3')
        AA = 'A3_'+str(A3_W.get())
        BB = A3_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('A3', 'A3', BB)
        #insert = ('A3', BB, 'A3')
        #save_data("custom_workspace", insert)

    if B1_W.get() != '':
        print('Entry Found in B1')
        AA = 'B1_'+str(B1_W.get())
        BB = B1_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('B1', 'B1', BB)
        #insert = ('B1', BB, 'B1')
        #save_data("custom_workspace", insert)

    if B2_W.get() != '':
        print('Entry Found in B2')
        AA = 'B2_'+str(B2_W.get())
        BB = B2_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('B2', 'B2', BB)
        #insert = ('B2', BB, 'B2')
        #save_data("custom_workspace", insert)

    if B3_W.get() != '':
        print('Entry Found in B3')
        AA = 'B3_'+str(B3_W.get())
        BB = B3_W.get()
        #print(AA)

        update_containecontypers_list(AA)
        load_container('B3', 'B3', BB)
        #insert = ('B3', BB, 'B3')
        #save_data("custom_workspace", insert)

    if C1_W.get() != '':
        print('Entry Found in C1')
        AA = 'C1_'+str(C1_W.get())
        BB = C1_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('C1', 'C1', BB)
        #insert = ('C1', BB, 'C1')
        #save_data("custom_workspace", insert)

    if C2_W.get() != '':
        print('Entry Found in C2')
        AA = 'C2_'+str(C2_W.get())
        BB = C2_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('C2', 'C2', BB)
        #insert = ('C2', BB, 'C2')
        #save_data("custom_workspace", insert)

    if C3_W.get() != '':
        print('Entry Found in C3')
        AA = 'C3_'+str(C3_W.get())
        BB = C3_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('C3', 'C3', BB)
        #insert = ('C3', BB, 'C3')
        #save_data("custom_workspace", insert)

    if D1_W.get() != '':
        print('Entry Found in D1')
        AA = 'D1_'+str(D1_W.get())
        BB = D1_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('D1', 'D1', BB)
        #insert = ('D1', BB, 'D1')
        #save_data("custom_workspace", insert)

    if D2_W.get() != '':
        print('Entry Found in D2')
        AA = 'D2_'+str(D2_W.get())
        BB = D2_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('D2', 'D2', BB)
        #insert = ('D2', BB, 'D2')
        #save_data("custom_workspace", insert)

    if D3_W.get() != '':
        print('Entry Found in D3')
        AA = 'D3_'+str(D3_W.get())
        BB = D3_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('D3', 'D3', BB)
        #insert = ('D3', BB, 'D3')
        #save_data("custom_workspace", insert)

    if E1_W.get() != '':
        print('Entry Found in E1')
        AA = 'E1_'+str(E1_W.get())
        BB = E1_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('E1', 'E1', BB)
        #insert = ('E1', BB, 'E1')
        #save_data("custom_workspace", insert)

    if E2_W.get() != '':
        print('Entry Found in E2')
        AA = 'E2_'+str(E2_W.get())
        BB = E2_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('E2', 'E2', BB)
        #insert = ('E2', BB, 'E2')
        #save_data("custom_workspace", insert)

    if E3_W.get() != '':
        print('Entry Found in E3')
        AA = 'E3_'+str(E3_W.get())
        BB = E3_W.get()
        #print(AA)

        update_containers_list(AA)
        load_container('E3', 'E3', BB)
        #insert = ('E3', BB, 'E3')
        #save_data("custom_workspace", insert)

    #Update Loaded in Workspace Container List
    try:
        update_containers_list_type()
        print(loaded_containers)
        temp = robot.containers()
        print("Robot Loaded Container List:", temp)

        confirmation_box(2)
    except:
        confirmation_box(9)

def action_save_pip():
    """
    Save Custom Pipette
    Note: The Load Pipette Function is placeholder, it just error checking argument is acceptable
    """
    if var_p_a.get() == 0:
        axis = 'b'
        print(axis)
        update_pipette('pipette_b', 0)
        update_pipette('pipette_a', 1)
    elif var_p_a.get() == 1:
        axis = 'a'
        print(axis)
        update_pipette('pipette_a', 1)
        update_pipette('pipette_b', 0)

    max_vol = var_max_volume.get()
    min_vol = var_min_volume.get()
    asp_speed = var_aspirate_speed.get()
    dis_speed = var_dispense_speed.get()


    temp = s_tip_rack.get()
    #temp = temp[0:2]

    tiprack = temp
    print(temp)

    temp = s_trash.get()
    #temp = temp[0:2]

    trash = temp
    print(temp)

    # print(max_vol)
    # print(min_vol)
    # print(asp_speed)
    # print(dis_speed)

    # print(tiprack)
    # print(trash)

    #Send Command to module load pipette [loadpipette] and save to database [save_data]
    try:
        loadpipette(axis, max_vol, min_vol, asp_speed, dis_speed, tiprack, trash)
        insert = (axis, max_vol, min_vol, '1', asp_speed, dis_speed, tiprack, trash)
        save_data("custom_pipette", insert) 
        print(loaded_pipette_list)

        confirmation_box(10)
    except:
        confirmation_box(8)

###########################################################################################################



###########################################################################################################
#
# Send Job to OT-1 [ WORKING IN PROGRESS ]
#
###########################################################################################################
def opencontainer(location):
    """
    Start Protocol from pre-configured/save protocol from database
    [ WORKING IN PROGRESS ]
    """

    pass


###########################################################################################################

###########################################################################################################
#
# Containers Creation UI [ WORKING IN PROGRESS ]
#
###########################################################################################################
def containersCreationUi():
    """ 
    Graphical UI for Custom Container Creation 
    [ WORKING IN PROGRESS ]

    """

    rootCustomContainer = Tk()
    rootCustomContainer.title('Simpletrons - OT - Container Creation')


    #Create Containers
    var_container_name = StringVar()

    label = ttk.Label(rootCustomContainer, text='Set a Name:', font = ('Arial', 12))
    label.grid(column = 0, row = 1) 
    
    e_container_name = Entry(rootCustomContainer, bd =5, justify = CENTER, textvariable = var_container_name)
    e_container_name.grid(column = 0, row = 2)  



def import_protocol_ui():
    pass

###########################################################################################################
#
# Containers Creation UI [ WORKING IN PROGRESS ]
#
###########################################################################################################
def export_protocol():
    """
    Export UI
    """
    global version
    global root


    ExportWindow = Toplevel(root)

    ExportWindow.title("Simpletrons - OT")
    ExportWindow.geometry("130x120")

    save_name = StringVar()

    #Set Window Location
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth()/3.5 - windowWidth/3.5)
    positionDown = int(root.winfo_screenheight()/3.5 - windowHeight/3.5)
    ExportWindow.geometry("+{}+{}".format(positionRight, positionDown))


    def close_popup():

        ExportWindow.destroy()
        ExportWindow.update()

    label = ttk.Label(ExportWindow, text="Export As ")
    label.grid(column = 0, row = 0)

    textboxA = Entry(ExportWindow, textvariable=save_name)
    textboxA.grid(column = 0, row = 1)


    def export_database():
        if os.path.isfile('export/'+str(save_name.get())+'.db'):
            print(print(save_name.get()))
            print('Database Already Exits, please try another name')
        else:
            print(save_name.get())
            dump_database(save_name.get())

    #Save Button
    save_button_image_pro = PhotoImage(file="graphic/content-save-outline.png") 
    save_step = ttk.Button(ExportWindow, image = save_button_image, width = 5, command = export_database)
    save_step.grid(column = 0, row = 2)
    Tooltip(save_step, text='Export File as entered name - Cannot be blank or same as existing files on export folder', wraplength=wraplength)

###########################################################################################################
#
# UI Protocol [Pop Up]
#
###########################################################################################################


well_1 = 0
well_2 = 0
dropdown_ppip = StringVar()

#Update Protocol Dropdown
def update_dropdown_source_pip():
    """
    Update source pipette Source Rack Dropdown List for Protocol UI
    """
    list = loaded_pipette_list
    dropdown_ppip['values'] = list
    print('Updating Dropdown List: Pipette Protocol')

def update_aspirate_source_rack():
    """
    Update Aspirate Source Rack Dropdown List for Protocol UI
    """
    list = loaded_containers
    dropdown_aspirate_c['values'] = list
    print('Updating Dropdown List: Containers Protocol')

def update_dispense_source_rack():
    """
    Update Dispense Source Rack Dropdown List for Protocol UI
    """
    list = loaded_containers
    dropdown_dispense_c['values'] = list
    print('Updating Dropdown List: Containers Protocol')

v1 = StringVar()
v2 = StringVar()
v3 = StringVar()
v4 = StringVar()
current_step_label_v = StringVar()
delete_button_image_pro = PhotoImage(file="graphic/delete-circle.png") 



def graphicalUIprotocol():
    """ 
    Code for Graphical Protocol Creation 
    Note: Remember to include global variable for any PhotoImage
    """ 
    global v1
    global v2
    global v3 
    global v4
    global shortcuts_list
    global dropdown_dispense_c
    global dropdown_aspirate_c
    global dropdown_ppip
    global dispense_con
    global well_1
    global well_2
    global save_button_image_pro
    global save_button_image_pro
    global background_image2
    global background_image3
    global background3
    global background2
    global step
    global max_step
    global current_row
    global current_step_label_v

    deleteTable("custom_protocol")

    current_row = 1
    step = 1
    max_step = 1
    #root = root
 

    f_name = StringVar()
    volume_well = DoubleVar()
    value_b = StringVar()
    value_c = StringVar()
    f_note = StringVar()
    shortcuts = StringVar()
    p_varpip = StringVar()
    aspirate_con = StringVar()
    dispense_con = StringVar()

    proroot = Toplevel(root)

    proroot.title("Simpletrons - OT: Protocol Designer")
    proroot.configure(background="#f9f4f2")
    #newWindow.geometry("200x60")
    
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth()/3.5 - windowWidth/3.5)
    positionDown = int(root.winfo_screenheight()/3.5 - windowHeight/3.5)
    proroot.geometry("+{}+{}".format(positionRight, positionDown))

    def close_popup():
        proroot.destroy()
        proroot.update()

    ###########################################################################################################
    # Start Pre Configured Software 
    ##########################################################################################################



    #Start Protocol
    def start_protocol_ui():
        con_pro_ui_root = Toplevel(root)

        con_pro_ui_root.title("Simpletrons - OT: Start Protocol")

        con_pro_ui_root.lift()
        con_pro_ui_root. attributes("-topmost", True)

        windowWidth = proroot.winfo_reqwidth()
        windowHeight = proroot.winfo_reqheight()
        positionRight = int(proroot.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(proroot.winfo_screenheight()/2 - windowHeight/2)
        con_pro_ui_root.geometry("+{}+{}".format(positionRight, positionDown))

        def close_popup():
            con_pro_ui_root.destroy()
            con_pro_ui_root.update()
        ###
        s_menu = Menu(root)
        con_pro_ui_root.config(menu = s_menu)

        #Title
        file_menu = Menu(s_menu)
        s_menu.add_cascade(label = "File", menu = file_menu)
        file_menu.add_command(label = "Exit", command = close_popup )


        label = ttk.Label(con_pro_ui_root, text = 'Start Protocol:')
        label.grid(column = 0, row = 1)

        def send_command_start_protocol():
            threading.Thread(target=start_protocol()).start()
        
        start_step = ttk.Button(con_pro_ui_root, text = 'Start', width = 8, command = send_command_start_protocol)
        start_step.grid(column = 0, row = 2)
        Tooltip(start_step, text='Start Protocol', wraplength=wraplength)

        stop_step = ttk.Button(con_pro_ui_root, text = 'STOP', width = 6, command = resume_robot)
        stop_step.grid(column = 1, row = 2)
        Tooltip(stop_step, text='Stop Protocol - Note Will Close Application', wraplength=wraplength)



    ###########################################################################################################
    # Draw Graphics (Containers)
    ########################################################################################################### 

    def callback_a(eventObject):
        ''' Draw Container 1 / a'''
        ''' Use the below template to add more labware photo reference'''
        ''' For instance change re.search to a labware name and PhotoImage'''
        ''' to path of the resource'''

        global background_image2
        global background2
        nonlocal textboxB


        temp = 0

        print(eventObject.widget.get())
        container_lookup = eventObject.widget.get()
        #Grab Value From Entry Box
        if re.search('96-deep-well', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/96-Deep-Well.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('96-PCR-flat', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/96-PCR-Flatt.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('96-PCR-tall', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/96-PCR-Tall.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('tiprack-10ul', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/Tiprack-10ul.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('tiprack-1000ul', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/Tiprack-1000.png')
            print("Load Container Image:", container_lookup)            
            temp = 1

        if re.search('96-flat', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/96-PCR-Flatt.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('24-well-plate', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/24-well-plate.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('48-well-plate', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/48-well-plate.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('point', container_lookup):
            background_image2=tk.PhotoImage(file='graphic/labware/point.png')
            print("Load Container Image:", container_lookup)
            temp = 1
            textboxB.delete(0, 'end')
            textboxB.insert(0,"A1")

        # if bool(re.search('point', container_lookup)) == False:
        #     #background_image3=tk.PhotoImage(file='graphic/labware/point.png')
        #     print("Reload Entry Box", container_lookup)
        #     temp = 1


        label = ttk.Label(proroot, text="Plate A")
        label.grid(column = 0, row = 9)
        background2 = ttk.Label(proroot, image = background_image2)
        background2.grid(column = 0, row = 10, columnspan = 5)

    #Draw Graphics - Second Container
    def callback_b(eventObject):
        ''' Draw Container 2 / b'''
        ''' Use the below template to add more labware photo reference'''
        ''' For instance change re.search to a labware name and PhotoImage'''
        ''' to path of the resource'''

        global background_image3
        global background3
        nonlocal textboxC

        temp = 0


        print(eventObject.widget.get())
        container_lookup = eventObject.widget.get()
        #Grab Value From Entry Box
        if re.search('96-deep-well', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/96-Deep-Well.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('96-PCR-flat', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/96-PCR-Flatt.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('96-PCR-tall', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/96-PCR-Tall.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('tiprack-10ul', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/Tiprack-10ul.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('tiprack-1000ul', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/Tiprack-1000.png')
            print("Load Container Image:", container_lookup)    
            temp = 1        

        if re.search('96-flat', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/96-PCR-Flatt.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('24-well-plate', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/24-well-plate.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('48-well-plate', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/48-well-plate.png')
            print("Load Container Image:", container_lookup)
            temp = 1

        if re.search('point', container_lookup):
            background_image3=tk.PhotoImage(file='graphic/labware/point.png')
            print("Load Container Image:", container_lookup)
            temp = 1
            textboxC.delete(0, 'end')
            textboxC.insert(0,"A1")

        # if bool(re.search('point', container_lookup)) == False:
        #     #background_image3=tk.PhotoImage(file='graphic/labware/point.png')
        #     print("Reload Entry Box", container_lookup)
        #     temp = 1


        label = ttk.Label(proroot, text="Plate B")
        label.grid(column = 0, row = 11)
        background3 = ttk.Label(proroot, image = background_image3)
        background3.grid(column = 0, row = 12, columnspan = 5)

    ###########################################################################################################
    #
    # Save Steps to Database
    #
    ###########################################################################################################
    def delete_protocol():
        global step
        deleteTable("custom_protocol")
        step = 1
        max_step = 1
        current_step_label_v.set("Step: " + str(step))



    def view_protocol():    
        conn = sqlite3.connect(db_file)
        #c = conn.cursor()
        proto_data = conn.execute("SELECT id, shortcuts, volume, aspirate_container, aspirate_well, dispense_container, dispense_well FROM custom_protocol") 
        records = proto_data.fetchall()

        viewWindow = Tk()

        e=Label(viewWindow,width=20,text='ID',borderwidth=2, relief='ridge',anchor='w',bg='turquoise')
        e.grid(row=0,column=0)
        e=Label(viewWindow,width=20,text='Type',borderwidth=2, relief='ridge',anchor='w',bg='turquoise')
        e.grid(row=0,column=1)
        e=Label(viewWindow,width=20,text='Volume (uL)',borderwidth=2, relief='ridge',anchor='w',bg='turquoise')
        e.grid(row=0,column=2)
        e=Label(viewWindow,width=20,text='Aspirate Container',borderwidth=2, relief='ridge',anchor='w',bg='turquoise')
        e.grid(row=0,column=3)
        e=Label(viewWindow,width=20,text='Aspirate Cell',borderwidth=2, relief='ridge',anchor='w',bg='turquoise')
        e.grid(row=0,column=4)
        e=Label(viewWindow,width=20,text='Dispense Container',borderwidth=2, relief='ridge',anchor='w',bg='turquoise')
        e.grid(row=0,column=5)
        e=Label(viewWindow,width=20,text='Dispense Cell',borderwidth=2, relief='ridge',anchor='w',bg='turquoise')
        e.grid(row=0,column=6)
        i=1

        for line in records: 
            for j in range(len(line)):
                e = Entry(viewWindow, width=20, fg='gray4') 
                e.grid(row=i, column=j) 
                e.insert(END, line[j])
            i=i+1
        
        # for line in records:
        #     #print(line)
        #     viewText.insert(END, line)
        #     viewText.insert(END, "\n")

        viewWindow.mainloop()
        # viewTable = ttk.Treeview(viewWindow)
        # viewTable['columns']=("ID", "volume", "aspirate container", "aspirate cell", "dispense container", "dispense cell")
        # for line in records:
        #     viewTable.insert("", 'end', line)

       # viewTable.pack()


        #print(proto_data)
        #print()
        conn.close()


    def back_step():
        global step
     
        global current_step_label_v
        #global max_step
        if step>1:
            step = step-1
            current_step_label_v.set("Step: " + str(step))
            
    def next_step():
        global step
        global max_step
        global current_step_label_v
        #global max_step
        if step < max_step:
            step = step+1
            current_step_label_v.set("Step: " + str(step))   
        


    def save_step():
        """ Save Step to Database """
        global step
        notes = 'null'
        step_count = False
        # Reference
        # shortcuts_list = ['Simple_Transfer', 'Multiple_Wells_Transfer', 'One_to_Many', 'Few_to_Many']
        print(shortcuts.get())

        ##SIMPLE TRANSFER 
        if shortcuts.get() == "Simple_Transfer":
            ''' Simple Transfer '''
            #Check if Friendly Name is available if not set a default based of step
            if len(f_name.get()) == 0:
                name = "step" + str(step)
            else:
                name = f_name.get()

            #Shortcut
            shortcuts_v = shortcuts.get()

            #Volume
            if volume_well.get() == 0:
                print("Please Check Volume Entry Box")
                step_count = True
            else:
                volume = volume_well.get()

            #Value 1 (Pipette)
            sel_pipette = p_varpip.get()
            #Value 2 (First Container)
            aspirate_container = aspirate_con.get()
            #Value 2 (First Container Syntax)
            container_lookup = aspirate_con.get()

            #Check if Point Container (Single Well Items)
            if re.search('point', container_lookup):
                aspirate_well = "A1"
            else:
                aspirate_well = value_b.get()
            #Value 3 (Second Container)
            dispense_container = dispense_con.get()
            #Value 4 (Second Container Syntax)
            container_lookup = dispense_con.get()

            if re.search('point', container_lookup):
                dispense_well = "A1"
            else:
                dispense_well = value_c.get()

            if len(f_note.get()) == 0:
                notes = "NULL"
            else:
                notes = f_note.get()


            #print("TEST: changetip variable", tipchange.get())
            if tipchange.get() == 1:
                change_tip = True

            else:
                change_tip = False
                
            row_col = "None"

            if mix_after.get() == 1:
                mixing = True
            else:
                mixing = False


        ##ONE TO MANY 
        if shortcuts.get() == "One_to_Many":
            #Check if Friendly Name is available if not set a default based of step
            if len(f_name.get()) == 0:
                name = "step" + str(step)
            else:
                name = f_name.get()
            #Shortcut
            shortcuts_v = shortcuts.get()

            #Volume
            if volume_well.get() == 0:
                print("Please Check Volume Entry Box")
                step_count = True
            else:
                volume = volume_well.get()
            #Value 1 (Pipette)
            sel_pipette = p_varpip.get()
            #Value 2 (First Container)
            aspirate_container = aspirate_con.get()
            #Value 2 (First Container Syntax)
            container_lookup = aspirate_con.get()

            #Check if Point Container (Single Well Items)
            if re.search('point', container_lookup):
                aspirate_well = "A1" #aspirate_well is aspirate cell
            else:
                aspirate_well = value_b.get()

            dispense_container = dispense_con.get() #value 3 is dispense container

            # Code To Find if row or column ()
            # If you need higher rows count adjust pattern2
            # pattern1 = re.compile("[A-Za-z]+")
            # pattern2 = re.compile("[0-12]+")
            container_lookup = value_c.get() #value_c is dispense container


            if re.match("[A-Za-z]+" , container_lookup) is not None:
                dispense_well = value_c.get()
                row_col = "cols"
                print("Loaded Cols")
                print("Check Input Cell")
            elif re.match("[0-9]+", container_lookup)  is not None:
                dispense_well = value_c.get()
                row_col = "rows"
                print("Loaded Row")
            else:
                step_count = True
                confirmation_box(11)
                print("Warning: Check Input Cell (Only if you see Warning)")

            if len(f_note.get()) == 0:
                notes = "NULL"
            else:
                notes = f_note.get()


            #print("TEST: changetip variable", tipchange.get())
            if tipchange.get() == 1:
                change_tip = True

            else:
                change_tip = False

            if mix_after.get() == 1:
                mixing = True
            else:
                mixing = False


        if shortcuts.get() == "Mixing":
            
            #Check for name
            if len(f_name.get()) == 0:
                name = "step" + str(step)
            else:
                name = f_name.get()

            #Shortcut name
            shortcuts_v = shortcuts.get()

            #Volume to mix
            if volume_well.get() == 0:
                print("Please Check Volume Entry Box")
                step_count = True
            else:
                volume = volume_well.get()

            #Value 1 (Pipette)
            sel_pipette = p_varpip.get()

            #Value 2 (First Container)
            aspirate_container = aspirate_con.get()
            #Value 2 (First Container Syntax)
            container_lookup = aspirate_con.get()

            #Check if Point Container (Single Well Items)
            if re.search('point', container_lookup):
                aspirate_well = "A1"
            else:
                aspirate_well = value_b.get()

            dispense_container = aspirate_container
            dispense_well = aspirate_well

            #Value 3 (Second Container)
            # dispense_container = dispense_con.get()
            # #Value 4 (Second Container Syntax)
            # container_lookup = dispense_con.get()

            # if re.search('point', container_lookup):
            #     dispense_well = "A1"
            # else:
            #     dispense_well = value_c.get()

            if len(f_note.get()) == 0:
                notes = "NULL"
            else:
                notes = f_note.get()

            #print("TEST: changetip variable", tipchange.get())
            if tipchange.get() == 1:
                change_tip = True
            else:
                change_tip = False
                
            row_col = "None"

            if mix_after.get() == 1:
                mixing = True
            else:
                mixing = False


        # if shortcuts.get() == "Multiple_Wells_Transfer":
        #     pass
            

        # if shortcuts.get() == "Few_to_Many":
        #     pass


        #Save or update

        global max_step
        global current_row
        global conn
        global cursor

        #If the current step number is the max step, add a new protocol step entry
        if step_count == False and step == max_step:
            insert = (name, shortcuts_v, sel_pipette, volume, aspirate_container, aspirate_well, dispense_container, dispense_well, change_tip, row_col, mixing, notes)
            save_data("custom_protocol", insert)

            step = step + 1
            current_row = current_row + 1
            max_step = max_step + 1

            current_step_label_v.set("Step: " + str(step)) #Set Default Label


        #If not, edit the 
        elif step_count == False:
            try:
                update = (name, shortcuts_v, sel_pipette, volume, aspirate_container, aspirate_well, dispense_container, dispense_well, change_tip, row_col, mixing, notes, step)
                #cursor.execute("UPDATE custom_protocol SET name=?, shortcuts = ?, pipette=?, volume=?, aspirate_container=?, aspirate_well=?, dispense_container = ?, dispense_well = ?, change_tip = ?, row_col = ?, notes =  WHERE id=?", insert)
                #conn.commit()

                update_data("custom_protocol", update)

                #step = max_step
                #messagebox.showinfo("Success", "Data updated successfully!")
            except Exception as e:
                pass
                #messagebox.showerror("Error", f"An error occurred: {e}")

        #Reset Count if error occurs in step creation 
        if step_count == True:
           # step = step - 1
            step_count = False
            confirmation_box(13)
        else:
            confirmation_box(12)



    def on_dropdown_change(event):
        selected_option = shortcuts.get()

        if selected_option == "Mixing":
            dropdown_dispense_c.config(state="disabled")
            textboxC.config(state="disabled")
        else:
            dropdown_dispense_c.config(state="normal")
            textboxC.config(state="normal")



    ###########################################################################################################

    ###########################################################################################################
    # Menu
    ###########################################################################################################

    ###
    s_menu = Menu(proroot)
    proroot.config(menu = s_menu)

    #Title
    file_menu = Menu(s_menu)
    start_protocol_menu = Menu(s_menu)
    s_menu.add_cascade(label = "File", menu = file_menu)
    file_menu.add_command(label = "Start Protocol", command = start_protocol_ui)
    file_menu.add_command(label = "Export Protocol", command = export_protocol)
    file_menu.add_command(label = "Import Protocol", command = import_protocol)
    file_menu.add_command(label = "Exit", command = close_popup )
    ####

    ###########################################################################################################
    # Draw Main Graphical Interface
    ###########################################################################################################

    # Short Cut Function
    label = ttk.Label(proroot, textvariable=v1)
    label.grid(column = 0, row = 0)
    v1.set("Transfer: Basic") #Set Default Label

    label = ttk.Label(proroot, text = 'Step Type:*').grid(column = 0, row = 1)

    current_step_label = ttk.Label(proroot, width=12, textvariable=current_step_label_v)
    current_step_label.grid(column = 1, row = 0)
    current_step_label_v.set("Step: 1") #Set Default Label
    
    dropdown_shortcuts = ttk.Combobox(proroot, state="readonly", textvariable = shortcuts)
    dropdown_shortcuts['values'] = shortcuts_list
    dropdown_shortcuts.bind("<<ComboboxSelected>>", on_dropdown_change)
    dropdown_shortcuts.current(0)   #Set Default Selection
    dropdown_shortcuts.grid(column = 0, row = 2)
    Tooltip(dropdown_shortcuts, text='Select a shortcut Function', wraplength=wraplength)

    # Friendly Note Input
    label = ttk.Label(proroot, text="Friendly Note:")
    label.grid(column = 2, row = 1)
    textboxF = Entry(proroot, textvariable=f_note)
    textboxF.grid(column = 2, row = 2)
    Tooltip(textboxF, text='Enter a more readable note for this step', wraplength=wraplength)

    tipchange = IntVar()
    mix_after = IntVar()

    #Change Tip Tick Box
    label = ttk.Label(proroot, text="Change Tip?")
    label.grid(column = 2, row = 3)
    textboxI = Checkbutton(proroot, onvalue=1, offvalue=0, variable=tipchange, text='Never')
    textboxI.grid(column = 2, row = 4)    
    #textboxI.select()
    Tooltip(textboxI, text='Do you wish to change tip per liquid transfer - applicable for multiple well transfer', wraplength=wraplength)


    label = ttk.Label(proroot, text="Mix after dispense?")
    label.grid(column = 3, row = 3)
    textboxQ = Checkbutton(proroot, onvalue=1, offvalue=0, variable=mix_after, text='Mix?')
    textboxQ.grid(column = 3, row = 4)    
    #textboxI.select()
    Tooltip(textboxQ, text='Do you wish to mix the well after a dispense?', wraplength=wraplength)


    # Friendly Name Input
    label = ttk.Label(proroot, text="Friendly Name:")
    label.grid(column = 1, row = 1)
    textboxF = Entry(proroot, width=12, textvariable=f_name)
    textboxF.grid(column = 1, row = 2)
    Tooltip(textboxF, text='Set a Friendly for this step in the protocol', wraplength=wraplength)

    #Select Pipette
    label = ttk.Label(proroot, text = 'Pipette:*')
    label.grid(column = 0, row = 3)
    dropdown_ppip = ttk.Combobox(proroot, state="readonly", textvariable = p_varpip, postcommand = update_dropdown_source_pip)
    dropdown_ppip.grid(column = 0, row = 4)
    Tooltip(dropdown_ppip, text='Select a Pipette', wraplength=wraplength)

    label = ttk.Label(proroot, textvariable=v2)
    label.grid(column = 1, row = 3)
    v2.set("Volume Per Well: (uL)*") #Set Default Label
    textboxA = Entry(proroot, width=12, textvariable=volume_well)
    textboxA.grid(column = 1, row = 4)
    Tooltip(textboxF, text='Set a level to transfer', wraplength=wraplength)

    #First Container
    label = ttk.Label(proroot, text = 'Aspirate:*')
    label.grid(column = 0, row = 5)
    dropdown_aspirate_c = ttk.Combobox(proroot, state="readonly", textvariable = aspirate_con, postcommand = update_aspirate_source_rack)
    dropdown_aspirate_c.grid(column = 0, row = 6)
    dropdown_aspirate_c.bind("<<ComboboxSelected>>", callback_a)

    label = ttk.Label(proroot, textvariable=v3)
    label.grid(column = 1, row = 5)
    v3.set("Wells:*") #Set Default Label
    textboxB = tk.Entry(proroot, width=12, textvariable=value_b)
    textboxB.grid(column = 1, row = 6)
    Tooltip(textboxB, text='Insert Well Position', wraplength=wraplength)

    #Second Container
    label = ttk.Label(proroot, text = 'Dispense:*')
    label.grid(column = 2, row = 5)
    dropdown_dispense_c = ttk.Combobox(proroot, state="readonly", textvariable = dispense_con, postcommand = update_dispense_source_rack)
    dropdown_dispense_c.grid(column = 2, row = 6)
    dropdown_dispense_c.bind("<<ComboboxSelected>>", callback_b)

    label = ttk.Label(proroot, textvariable=v4)
    label.grid(column = 3, row = 5)
    v4.set("Wells:*") #Set Default Label
    textboxC = tk.Entry(proroot, width=12, textvariable=value_c)
    textboxC.grid(column = 3, row = 6)
    Tooltip(textboxC, text='Insert Well Position', wraplength=wraplength)


    #Save Button
    #save_button_image_pro = PhotoImage(file="graphic/content-save-outline.png") 
    save_step = ttk.Button(proroot, image = save_button_image, width = 5, command = save_step)
    save_step.grid(column = 4, row = 6)
    Tooltip(save_step, text='Save Protocol Step', wraplength=wraplength)

    #Delete Protocol
    #delete_button_image_pro = PhotoImage(file="graphic/delete-circle.png") 
    delete_protocol = ttk.Button(proroot, image = delete_button_image_pro, width = 5, command = delete_protocol)
    delete_protocol.grid(column = 4, row = 0)
    Tooltip(delete_protocol, text='Delete ALL Protocol Step', wraplength=wraplength)

    #View protocol
    view_protocol = ttk.Button(proroot, text = "View Protocol", width = 15, command = view_protocol, )
    view_protocol.grid(column = 4, row = 5)


        #View protocol
    go_back = ttk.Button(proroot, text = "Back", width = 5, command = back_step)
    go_back.grid(column = 4, row = 7)

    go_next = ttk.Button(proroot, text = "Next", width = 5, command = next_step)
    go_next.grid(column = 4, row = 8)


##########################################################################################################

###########################################################################################################
#
#
#
# Calibration UI
#
#
#
###########################################################################################################
# root = Tk()
# root.title('Simpletrons - OT')
###########################################################################################################
#
#Tab Creation
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab1b = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

#Tab Header Name
tabControl.add(tab1b, text ='Step 1 Containers Setup')
tabControl.add(tab1, text ='Step 2 Pipette Setup')
tabControl.add(tab2, text ='Step 3 Calibrate Pipette')
tabControl.add(tab3, text ='Step 4 Calibrate Containers')
#tabControl.add(tab4, text ='Step 3 Protocol Programmer')
#tabControl.add(tab5, text ='Step 4 Start Protocol')

tabControl.pack(expand = 1, fill ="both")
#tabControl.grid(column = 3, row = 1, padx = 1)

########################################################################################################
#
#Top Menu 
#
#########################################################################################################

def aboutPage():
    confirmation_box(1)
    pass

s_menu = Menu(root)
root.config(menu = s_menu)

file_menu = Menu(s_menu)
s_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "New Protocol..." , command=graphicalUIprotocol)
file_menu.add_command(label = "About", command = aboutPage)
file_menu.add_command(label = "Source Code", command = open_url_github)
file_menu.add_command(label = "Exit", command = root.quit )

file2_menu = Menu(s_menu)
s_menu.add_cascade(label = "Troubleshooting", menu = file2_menu)
file2_menu.add_command(label = "Robot Connections Options", command = connecton_graphical)
file2_menu.add_command(label = "Start Demo Protocol", command = load_demo_protocol)
file2_menu.add_command(label = "Documentation", command = open_url_doc)



#Start Up UI
#connecton_graphical()
########################################################################################################
#
#Container Setup
#
A1_W = StringVar(root, value='')
A2_W = StringVar(root, value='')
A3_W = StringVar(root, value='')
B1_W = StringVar(root, value='')
B2_W = StringVar(root, value='')
B3_W = StringVar(root, value='')
C1_W = StringVar(root, value='')
C2_W = StringVar(root, value='')
C3_W = StringVar(root, value='')
D1_W = StringVar(root, value='')
D2_W = StringVar(root, value='')
D3_W = StringVar(root, value='')
E1_W = StringVar(root, value='')
E2_W = StringVar(root, value='')
E3_W = StringVar(root, value='')

background_image=PhotoImage(file='graphic/workspace.png')
my_canvas = ttk.Label(tab1b, image = background_image)
my_canvas.grid(column = 0, row = 0, rowspan = 3, columnspan = 5)

#Col A
dropdown_1 = ttk.Combobox(tab1b, textvariable = A1_W, width = 19)
dropdown_1['values'] = container_list 
dropdown_1.grid(column = 0, row = 2, padx = 1)
dropdown_1.lift()
Tooltip(dropdown_1, text='Workspace A1 Cell', wraplength=wraplength)


dropdown_2 = ttk.Combobox(tab1b, textvariable = A2_W, width = 19)
dropdown_2['values'] = container_list 
dropdown_2.grid(column = 0, row = 1, padx = 1)
dropdown_2.lift()
Tooltip(dropdown_2, text='Workspace A2 Cell', wraplength=wraplength)


dropdown_3 = ttk.Combobox(tab1b, textvariable = A3_W, width = 19)
dropdown_3['values'] = container_list 
dropdown_3.grid(column = 0, row = 0, padx = 1)
dropdown_3.lift()
Tooltip(dropdown_3, text='Workspace A3 Cell', wraplength=wraplength)

#Col B
dropdown_4 = ttk.Combobox(tab1b, textvariable = B1_W, width = 19)
dropdown_4['values'] = container_list 
dropdown_4.grid(column = 1, row = 2, padx = 1)
dropdown_4.lift()
Tooltip(dropdown_4, text='Workspace B1 Cell', wraplength=wraplength)

dropdown_5 = ttk.Combobox(tab1b, textvariable = B2_W, width = 19)
dropdown_5['values'] = container_list 
dropdown_5.grid(column = 1, row = 1, padx = 1)
dropdown_5.lift()
Tooltip(dropdown_5, text='Workspace B2 Cell', wraplength=wraplength)

dropdown_6 = ttk.Combobox(tab1b, textvariable = B3_W, width = 19)
dropdown_6['values'] = container_list 
dropdown_6.grid(column = 1, row = 0, padx = 1)
dropdown_6.lift()
Tooltip(dropdown_6, text='Workspace B3 Cell', wraplength=wraplength)


#Col C
dropdown_7 = ttk.Combobox(tab1b, textvariable = C1_W, width = 19)
dropdown_7['values'] = container_list 
dropdown_7.grid(column = 2, row = 2, padx = 1)
dropdown_7.lift()
Tooltip(dropdown_7, text='Workspace C1 Cell', wraplength=wraplength)


dropdown_8 = ttk.Combobox(tab1b, textvariable = C2_W, width = 19)
dropdown_8['values'] = container_list 
dropdown_8.grid(column = 2, row = 1, padx = 1)
dropdown_8.lift()
Tooltip(dropdown_8, text='Workspace C2 Cell', wraplength=wraplength)


dropdown_9 = ttk.Combobox(tab1b, textvariable = C3_W, width = 19)
dropdown_9['values'] = container_list 
dropdown_9.grid(column = 2, row = 0, padx = 1)
dropdown_9.lift()
Tooltip(dropdown_9, text='Workspace C3 Cell', wraplength=wraplength)


#Col D
dropdown_10 = ttk.Combobox(tab1b, textvariable = D1_W, width = 19)
dropdown_10['values'] = container_list 
dropdown_10.grid(column = 3, row = 2, padx = 1)
dropdown_10.lift()
Tooltip(dropdown_10, text='Workspace D1 Cell', wraplength=wraplength)

dropdown_11 = ttk.Combobox(tab1b, textvariable = D2_W, width = 19)
dropdown_11['values'] = container_list 
dropdown_11.grid(column = 3, row = 1, padx = 1)
dropdown_11.lift()
Tooltip(dropdown_11, text='Workspace D2 Cell', wraplength=wraplength)

dropdown_12 = ttk.Combobox(tab1b, textvariable = D3_W, width = 19)
dropdown_12['values'] = container_list 
dropdown_12.grid(column = 3, row = 0, padx = 1)
dropdown_12.lift()
Tooltip(dropdown_12, text='Workspace D3 Cell', wraplength=wraplength)
#Col E
dropdown_13 = ttk.Combobox(tab1b, textvariable = E1_W, width = 19)
dropdown_13['values'] = container_list 
dropdown_13.grid(column = 4, row = 2, padx = 1)
dropdown_13.lift()
Tooltip(dropdown_13, text='Workspace E1 Cell', wraplength=wraplength)


dropdown_14 = ttk.Combobox(tab1b, textvariable = E2_W, width = 19)
dropdown_14['values'] = container_list 
dropdown_14.grid(column = 4, row = 1, padx = 1)
dropdown_14.lift()
Tooltip(dropdown_14, text='Workspace E2 Cell', wraplength=wraplength)


dropdown_14 = ttk.Combobox(tab1b, textvariable = E3_W, width = 19)
dropdown_14['values'] = container_list 
dropdown_14.grid(column = 4, row = 0, padx = 1)
dropdown_14.lift()
Tooltip(dropdown_14, text='Workspace E3 Cell', wraplength=wraplength)


#Save Button - Save Workspace 
label = ttk.Label(tab1b, text='Save Workspace:', font = ('Arial', 12))
label.grid(column = 1, row = 3)

save_button_image = PhotoImage(file="graphic/content-save-outline.png") 
save_w = ttk.Button(tab1b, image = save_button_image, width = 5, command = setup_workspace)
save_w.grid(column = 2, row = 3)

Tooltip(save_w, text='Load Current Workspace', wraplength=wraplength)

#Save Button - Load Pre-Configured Workspace
label = ttk.Label(tab1b, text='Load Workspace:', font = ('Arial', 12))
label.grid(column = 3, row = 3)

pree_home_image = PhotoImage(file="graphic/cog-refresh-outline.png")
save_ww = ttk.Button(tab1b, image = pree_home_image, width = 5, command = load_pre_workspace)
save_ww.grid(column = 4, row = 3)

Tooltip(save_ww, text='Load Pre Configured Workspace', wraplength=wraplength)

#Button

########################################################################################################




########################################################################################################
#
#Calibrate Containers
#
########################################################################################################
#Drop Down Default Selection
varpip = StringVar(root, value='')
head_speed_a = DoubleVar()


def callback_con(eventObject):
    global vpc1

    global background_cal
    global background_image_cc

    container_lookup = eventObject.widget.get()


    if re.search('tiprack', container_lookup):
        background_cal=tk.PhotoImage(file='graphic/calibrate/calibrate_tip.png')
        vpc1.set("Tip Rack: pressed down just a in small intervals")

    if re.search('well', container_lookup):
        background_cal=tk.PhotoImage(file='graphic/calibrate/calibrate_con.png')
        vpc1.set("Well Plate: Ensure a Tip is installed and location is touching the base ")

    background_image_cc = ttk.Label(tab3, image = background_cal)
    background_image_cc.grid(column = 6, row = 2, rowspan = 7)

    label = ttk.Label(tab3, textvariable=vpc1)
    label.grid(column = 6, row = 1)


#Selection 1 - Pipette
label_select_pipette_c = ttk.Label(tab3, text='Select a Pipette', font = ('Arial', 12))
label_select_pipette_c.grid(column = 1, row = 1, padx = 1)
dropdown_varpip_c = ttk.Combobox(tab3,  state="readonly" , textvariable = varpip, postcommand = update_dropdown_pip_c)
dropdown_varpip_c.grid(column = 1, row = 2, padx = 1)
Tooltip(label_select_pipette_c, text='Select Pipette that will be used for following container', wraplength=wraplength)
Tooltip(dropdown_varpip_c, text='Select Pipette that will be used for following container', wraplength=wraplength)


#Drop Down Default Selection
c_varcon = StringVar(root, value='')

#Selection 1 - Containers
label_select_container_c = ttk.Label(tab3, text='Select a Container', font = ('Arial', 12))
label_select_container_c.grid(column = 1, row = 3, padx = 1)
dropdown_varcon_c = ttk.Combobox(tab3,  state="readonly", textvariable = c_varcon, postcommand = update_dropdown_con_c)
dropdown_varcon_c.grid(column = 1, row = 4, padx = 1)
dropdown_varcon_c.bind("<<ComboboxSelected>>", callback_con)
Tooltip(label_select_container_c, text='Please calibrate all container and Press Save even if calibration point is correct', wraplength=wraplength)
Tooltip(dropdown_varcon_c, text='Please calibrate all container and Press Save even if calibration point is correct', wraplength=wraplength)



#Section 2 - Pipette Movement 

#Pipette Movement Increments
#Movement Pad - X Axis
#Set Image to variable
xn_button_image = PhotoImage(file="graphic/arrow-left-bold-circle.png") # [ X Axis Negative ]
left_b = ttk.Button(tab3, image = xn_button_image, width = 5, command = move_x_neg)
left_b.grid(column = 3, row = 2)
Tooltip(left_b, text='Move Robot X Axis - [Left]', wraplength=wraplength)


#Movement Pad - X Axis
#Set Image to variable 
xp_button_image = PhotoImage(file="graphic/arrow-right-bold-circle.png") # [ X Axis Positive ]
right_b = ttk.Button(tab3, image = xp_button_image, width = 5, command = move_x_pos)
right_b.grid(column = 5, row = 2)
Tooltip(right_b, text='Move Robot X Axis - [Right]', wraplength=wraplength)


#Movement Pad - Y Axis
#Set Image to variable
yn_button_image = PhotoImage(file="graphic/arrow-up-bold-circle.png")  # [ y Axis Positive ]
down_b = ttk.Button(tab3, image = yn_button_image, width = 5, command = move_y_pos)
down_b.grid(column = 4, row = 1)
Tooltip(down_b, text='Move Robot Y Axis - [Down]', wraplength=wraplength)


#Movement Pad - Y Axis
#Set Image to variable
yp_button_image = PhotoImage(file="graphic/arrow-down-bold-circle.png") # [ y Axis Negative ]
up_b = ttk.Button(tab3, image = yp_button_image, width = 5, command = move_y_neg)
up_b.grid(column = 4, row = 3)
Tooltip(up_b, text='Move Robot Y Axis - [Up]', wraplength=wraplength)

#Movement Pad - Z Axis [Pipette Movement] Down
zd_button_image = PhotoImage(file="graphic/arrow-down-bold-circle.png")  # [ Z Axis Negative ]
z_up_b = ttk.Button(tab3, image = zd_button_image, width = 5, command = move_z_neg)
z_up_b.grid(column = 3, row = 3)
Tooltip(z_up_b, text='Move Robot Pipette Arm - [Up]', wraplength=wraplength)

#Movement Pad - Z Axis [Pipette Movement] UP
zu_button_image = PhotoImage(file="graphic/arrow-up-bold-circle.png") # [ z Axis Positive ]
z_down_b = ttk.Button(tab3, image = zu_button_image, width = 5, command = move_z_pos)
z_down_b.grid(column = 3, row = 1)
Tooltip(z_up_b, text='Move Robot Pipette Arm - [Down]', wraplength=wraplength)


#Home
home_image = PhotoImage(file="graphic/home.png") 
home_b = ttk.Button(tab3, image = home_image, width = 5, command = home_axis)
home_b.grid(column = 4, row = 4)
Tooltip(home_b, text='Home all axis on robot (OT-1)', wraplength=wraplength)


#Move to preconfigured 
pre_home_image = PhotoImage(file="graphic/cog-refresh-outline.png")
pre_home_b = ttk.Button(tab3, image = pre_home_image, width = 5, command = load_axis)
pre_home_b.grid(column = 5, row = 4)
Tooltip(pre_home_b, text='Go To Selected Container Calibration Point', wraplength=wraplength)


#Save Button - Calibration 
#save_button_image = PhotoImage(file="graphic/content-save-outline.png") 
save_c = ttk.Button(tab3, image = save_button_image, width = 5, command = save_containers_calibration)
save_c.grid(column = 3, row = 4)
Tooltip(save_c, text='Save Calibration', wraplength=wraplength)


#Change Movement Speed
label_movenment_speed = ttk.Label(tab3, text='Set Movement Speed:', font = ('Arial', 10))
label_movenment_speed.grid(column = 1, row = 5)
Tooltip(label_movenment_speed, text='Set Movement Speed of Robot', wraplength=wraplength)

#Scale Bar
scale_a = Scale(tab3, from_=0.1, to=80, resolution = 0.1, orient="horizontal", variable = head_speed_a)
scale_a.grid(column = 1, row = 6)
scale_a.set(2)
Tooltip(scale_a, text='Set Movement Speed of Robot', wraplength=wraplength)

#Sync Entry Box
text = Entry(tab3, width=4, textvariable=head_speed_a)
text.grid(column = 0, row = 6, padx=5)
text.bind("<Return>", lambda event: scale_a.configure(to=head_speed_a.get()))
#Unit
label = ttk.Label(tab3, text='mm', font = ('Arial', 10))
label.grid(column = 2, row = 6)

# Start Command Threading [LL]
def set_calibration_location():
    threading.Thread(target=moveDefaultLocation_p("pipette_a", "bottom")).start()

def set_calibration_drop_tip():
    threading.Thread(target=moveDefaultLocation_p("pipette_a", "drop_tip")).start()
    
label_set_calibration = ttk.Button(tab3, text='Pickup Tip', command = set_calibration_location)
label_set_calibration.grid(column = 3, row = 5, columnspan = 3)
Tooltip(label_set_calibration, text='Set Calibration Point for Tip Calibration', wraplength=wraplength)


label_drop_tip_c = ttk.Button(tab3, text='Drop Tip', command = set_calibration_drop_tip)
label_drop_tip_c.grid(column = 3, row = 6, columnspan = 3)
Tooltip(label_drop_tip_c, text='Drop Pipette Tip', wraplength=wraplength)

label_set_calibration = ttk.Button(tab3, text='Connect to Robot', command = connecton_graphical)
label_set_calibration.grid(column = 0, row = 7, columnspan = 3)
Tooltip(label_set_calibration, text='Connect to Robot UI, ensure robot is homed before calibration', wraplength=wraplength)

#Keyboard Input
root.bind("<Left>", move_x_neg)
root.bind("<Right>", move_x_pos)
root.bind("<Up>", move_y_neg) 
root.bind("<Down>", move_y_pos)

def key_press(event):
    if event.char == "R":
        move_z_neg()
    if event.char == "r":
        move_z_neg()
    if event.char == "f":
        move_z_pos()
    if event.char == "F":
        move_z_pos()
    if event.char == "a":
        move_x_neg()
    if event.char == "d":
        move_x_pos()
    if event.char == "w":
        move_y_neg()
    if event.char == "s":
        move_y_pos()

    pass

root.bind("<Key>", key_press)

#########################################################################################################
#
#Setup Pipette
#
#########################################################################################################
#Drop Down Default Selection
#varcon = StringVar(root, value='')
var_p_a = IntVar()
#var_max_volume = DoubleVar()
#var_min_volume = DoubleVar()
#var_aspirate_speed = DoubleVar()
#var_dispense_speed = DoubleVar()
s_tip_rack = StringVar(root, value='')
s_trash = StringVar(root, value='')



#Selection 1 - Axis
label_axis = ttk.Label(tab1, text='Select a Axis:', font = ('Arial', 12))
label_axis.grid(column = 1, row = 0)
Tooltip(label_axis, text='Select Pipette Axis [Left or Right]', wraplength=wraplength)
#Scale Bar
scale_1 = Scale(tab1, from_=0, to=1, resolution = 1, orient="horizontal", variable = var_p_a)
scale_1.grid(column = 1, row = 1)
Tooltip(scale_1, text='Select Pipette Axis [Left or Right]', wraplength=wraplength)

left_hand_image = PhotoImage(file="graphic/hand-left.png")
right_hand_image = PhotoImage(file="graphic/hand-right.png")

label = ttk.Label(tab1, image=left_hand_image).grid(column = 0,  row =0)
label = ttk.Label(tab1, text='L', font = ('Arial', 12) ).grid(column = 0,  row =1)
label = ttk.Label(tab1, image=right_hand_image).grid(column = 2,  row =0)
label = ttk.Label(tab1, text='R', font = ('Arial', 12) ).grid(column = 2,  row =1)

#----------------Selection 2 - Max Volume---------------------
var_max_volume = IntVar()
var_max_volume.set(1000)

label = ttk.Label(tab1, text='Select a max volume:', font = ('Arial', 12))
label.grid(column = 1, row = 2)

def update_var_max_volume(event):
    try:
        max_volume = entry_var2.get()
        if 100 <= max_volume <= 2000:
            scale_2.set(max_volume)
            var_max_volume.set(max_volume)
        else:
            scale_var2.set(1000)
          
    except ValueError:
        pass

def update_var_max_volume1(event):
    try:
        max_volume = scale_var2.get()
        text_2.delete(0, tk.END)  
        text_2.insert(0, max_volume)
        var_max_volume.set(max_volume)
    except ValueError:
        pass
      
# Separate variables for Scale and Entry Box
scale_var2 = tk.IntVar()
scale_var2.set(1000)

entry_var2 = tk.IntVar()
entry_var2.set(1000)


label = ttk.Label(tab1, text='Select a max volume:', font=('Arial', 12))
label.grid(column=1, row=2)

# Scale Bar
scale_2 = Scale(tab1, from_=100, to=2000, resolution = 1, orient="horizontal", variable = scale_var2, command = update_var_max_volume1)
scale_2.grid(column = 1, row = 3)
Tooltip(scale_2, text='Set Pipette Max Volume', wraplength=wraplength)
# Entry Box
text_2 = Entry(tab1, width=4, textvariable=entry_var2)
text_2.grid(column=0, row=3, padx=5)
text_2.bind("<Enter>", update_var_max_volume)

label = ttk.Label(tab1, text='uL', font = ('Arial', 12))
label.grid(column = 2, row = 3)

#---------------------Selection 3 - Min Volume-----------------------
var_min_volume = IntVar()
var_min_volume.set(100)

label = ttk.Label(tab1, text='Select a min volume:', font = ('Arial', 12))
label.grid(column = 1, row = 4)

def update_var_min_volume(event):
    try:
        min_volume = entry_var3.get()
        if 100 <= min_volume <= 2000:
            scale_3.set(min_volume)
            var_min_volume.set(min_volume) 
        else:
            scale_var3.set(100)
    except ValueError:
        pass

def update_var_min_volume1(event):
    try:
        min_volume = scale_var3.get()
        text_3.delete(0, tk.END) 
        text_3.insert(0, min_volume)
        var_min_volume.set(min_volume)
    except ValueError:
        pass
      
# Separate variables for Scale and Entry Box
scale_var3 = tk.IntVar()
scale_var3.set(100)

entry_var3 = tk.IntVar()
entry_var3.set(100)
    
#Scale Bar
scale_3 = Scale(tab1, from_=100, to=2000, resolution = 1, orient="horizontal", variable = scale_var3, command = update_var_min_volume1)
scale_3.grid(column = 1, row = 5)
Tooltip(scale_2, text='Set Pipette Min Volume', wraplength=wraplength)

#Entry Box
text_3 = Entry(tab1, width=4, textvariable=entry_var3)
text_3.grid(column = 0, row = 5, padx=5)
text_3.bind("<Enter>", update_var_min_volume)
#Unit
label = ttk.Label(tab1, text='uL', font = ('Arial', 12))
label.grid(column = 2, row = 3)

#Unit
label = ttk.Label(tab1, text='uL', font = ('Arial', 12))
label.grid(column = 2, row = 5)



#------------------------Selection 3 - aspirate_speed-----------------------
var_aspirate_speed = IntVar()
var_aspirate_speed.set(100)

label = ttk.Label(tab1, text='Select aspirate speed:', font = ('Arial', 12))
label.grid(column = 1, row = 6)

def update_var_aspirate_speed(event):
    try:
        aspirate_speed = entry_var4.get()
        if 100 <= aspirate_speed <= 2000:
            scale_4.set(aspirate_speed)
            var_aspirate_speed.set(aspirate_speed) 
        else:
            scale_var4.set(100)
    except ValueError:
        pass

def update_var_aspirate_speed1(event):
    try:
        aspirate_speed = scale_var4.get()
        text_4.delete(0, tk.END) 
        text_4.insert(0, aspirate_speed)
        var_aspirate_speed.set(aspirate_speed)
    except ValueError:
        pass


# Separate variables for Scale and Entry Box
scale_var4 = tk.IntVar()
scale_var4.set(100)

entry_var4 = tk.IntVar()
entry_var4.set(100)

#Scale Bar
scale_4 = Scale(tab1, from_=100, to=1500, resolution = 1, orient="horizontal", variable = scale_var4, command = update_var_aspirate_speed1)
scale_4.grid(column = 1, row = 7)
Tooltip(scale_4, text='Set Pipette aspirate speed', wraplength=wraplength)

#Sync Entry Box
text_4 = Entry(tab1, width=4, textvariable=entry_var4)
text_4.grid(column = 0, row = 7, padx=5)
text_4.bind("<Enter>", update_var_aspirate_speed)
#Unit
label = ttk.Label(tab1, text='mm/min', font = ('Arial', 12))
label.grid(column = 2, row = 7)

# Separator object
separator = ttk.Separator(tab1, orient='vertical')
separator.grid(row=0,column=4, rowspan=10, ipady=180)

#----------------------Selection 4 - dispense_speed-----------------------
var_dispense_speed = IntVar()
var_dispense_speed.set(100)

label = ttk.Label(tab1, text='Select a dispense speed:', font = ('Arial', 12))
label.grid(column = 1, row = 8)

def update_var_dispense_speed(event):
    try:
        dispense_speed = entry_var5.get()
        if 100 <= dispense_speed <= 2000:
            scale_5.set(dispense_speed)
            var_dispense_speed.set(dispense_speed) 
        else:
            scale_var5.set(100)
    except ValueError:
        pass

def update_var_dispense_speed1(event):
    try:
        dispense_speed = scale_var5.get()
        text_5.delete(0, tk.END) 
        text_5.insert(0, dispense_speed)
        var_dispense_speed.set(dispense_speed)
    except ValueError:
        pass


# Separate variables for Scale and Entry Box
scale_var5 = tk.IntVar()
scale_var5.set(100)

entry_var5 = tk.IntVar()
entry_var5.set(100)
    
#Scale Bar
scale_5 = Scale(tab1, from_=100, to=1500, resolution = 1, orient="horizontal", variable = scale_var5, command = update_var_dispense_speed1)
scale_5.grid(column = 1, row = 9)
Tooltip(scale_5, text='Set Pipette dispense speed', wraplength=wraplength)

#Sync Entry Box
text_5 = Entry(tab1, width=4, textvariable=entry_var5)
text_5.grid(column = 0, row = 9, padx=5)
text_5.bind("<Enter>", update_var_dispense_speed)
#Unit
label = ttk.Label(tab1, text='mm/min', font = ('Arial', 12))
label.grid(column = 2, row = 9)

#-------------------Selection 5 - Select a Tip Rack----------------------
label = ttk.Label(tab1, text='Select a Tip Rack:*', font = ('Arial', 12))
label.grid(column = 6, row = 0)
dropdown_tip_rack = ttk.Combobox(tab1, state="readonly",  textvariable = s_tip_rack, postcommand = update_dropdown_tip_rack)
#dropdown['values'] = loaded_containers # Replace to Global pipette variable
dropdown_tip_rack.grid(column = 6, row = 1)
Tooltip(dropdown_tip_rack, text='Set a Pipette Tip Rack', wraplength=wraplength)

#--------------------Selection 6 - Select a Bin----------------------------
label = ttk.Label(tab1, text='Select a Bin:*', font = ('Arial', 12))
label.grid(column = 6, row = 2)
dropdown_trash = ttk.Combobox(tab1,  state="readonly" , textvariable = s_trash, postcommand = update_dropdown_trash)
#dropdown['values'] = loaded_containers # Replace to Global pipette variable
dropdown_trash.grid(column = 6, row = 3)
Tooltip(dropdown_trash, text='Set a Pipette Trash Rack', wraplength=wraplength)

# Save Button
label = ttk.Label(tab1, text='Save Pipette Config:', font = ('Arial', 12))
label.grid(column = 6, row = 4)
save_pip = ttk.Button(tab1, image = save_button_image, width = 5, command = action_save_pip)
save_pip.grid(column = 6, row = 5)
Tooltip(save_pip, text='Save and Load Current Pipette Based off your selected slider', wraplength=wraplength)

# Separator object
separator = ttk.Separator(tab1, orient='vertical')
separator.grid(row=0,column=8, rowspan=10, ipady=180)

#Use Pre-Configured Pipetting in script/database
label = ttk.Label(tab1, text='Load Pre-Configured:', font = ('Arial', 12))
label.grid(column = 6, row = 6)
pre_select_pip = ttk.Button(tab1, image = pre_home_image, width = 5, command = load_pre_pip)
pre_select_pip.grid(column = 6, row = 7)
Tooltip(pre_select_pip, text='Load Pre Configured Pipette [Ask Tech or Check Documentation for pipette parameters] ', wraplength=wraplength)



#########################################################################################################
#
#Calibrate Pipette
#
#########################################################################################################
#Change Photo
#Load Graphics According to Position Calibration
vpc1 = StringVar()
head_speed_p = DoubleVar()

def callback_p(eventObject):
    global vpc1

    global background_img_pc
    global background_image_pc

    if eventObject.widget.get() == "top":
        background_image_pc=tk.PhotoImage(file='graphic/calibrate/Top.png')
        vpc1.set("Top: Plunger is positioned almost all the way up (but still being \n pressed down just a tiny bit")

    if eventObject.widget.get() == "bottom":
        background_image_pc=tk.PhotoImage(file='graphic/calibrate/Bottom.png')
        vpc1.set("Bottom: Plunger is at or slightly above it’s “first-stop” or “soft-stop” ")

    if eventObject.widget.get() == "blow_out":
        background_image_pc=tk.PhotoImage(file='graphic/calibrate/Blowout.png')
        vpc1.set("Blow Out: Plunger is all the way down to it's “second-stop” or \n “hard-stop”,  making sure any attached tip do not get pushed off")

    if eventObject.widget.get() == "drop_tip":
        background_image_pc=tk.PhotoImage(file='graphic/calibrate/Blowout.png')
        vpc1.set("Drop Tip: Forces any attached tip to fall off ")

    background_img_pc = ttk.Label(tab2, image = background_image_pc)
    background_img_pc.grid(column = 6, row = 2, rowspan = 7)

    label = ttk.Label(tab2, textvariable=vpc1)
    label.grid(column = 6, row = 1)


#Selection 1 - Pipette
label = ttk.Label(tab2, text='Select a Pipette:', font = ('Arial', 12))
label.grid(column = 1, row = 1, padx = 1)
dropdown_cpip = ttk.Combobox(tab2,  state="readonly", textvariable = varpip, postcommand = update_dropdown_pip)
dropdown_cpip.grid(column = 1, row = 2, padx = 1)
Tooltip(dropdown_cpip, text='Select Pipette To Calibrate', wraplength=wraplength)

#Drop Down Default Selection
pippos = StringVar(root, value=' ')
#Selection 2 - Which Selection
label = ttk.Label(tab2, text='Select a Position:', font = ('Arial', 12))
label.grid(column = 1, row = 3, padx = 1)
dropdown_cpos = ttk.Combobox(tab2,  state="readonly", textvariable = pippos, postcommand = update_dropdown_pos)
dropdown_cpos['values'] = [ 'top','bottom', 'blow_out','drop_tip']
dropdown_cpos.grid(column = 1, row = 4, padx = 1)
dropdown_cpos.bind("<<ComboboxSelected>>", callback_p)
Tooltip(dropdown_cpos, text='Select a Calibration Point', wraplength=wraplength)

#Pipette Movement Increments
#Movement Pad - Z Axis [Pipette Movement] Down
z_up_bp = ttk.Button(tab2, image = zd_button_image, width = 5, command = move_pip_action_down)
z_up_bp.grid(column = 3, row = 3)
Tooltip(z_up_bp, text='Move Pipette Piston Location [Down] ', wraplength=wraplength)


#Movement Pad - Z Axis [Pipette Movement] UP 
z_down_bp = ttk.Button(tab2, image = zu_button_image, width = 5, command = move_pip_action_up)
z_down_bp.grid(column = 3, row = 1)
Tooltip(z_down_bp, text='Move Pipette Piston Location [Up] ', wraplength=wraplength)


#Home Button
home_b = ttk.Button(tab2, image = home_image, width = 5, command = move_pip_action_home)
home_b.grid(column = 4, row = 4)
Tooltip(home_b, text='Home Selected Pipette Axis ', wraplength=wraplength)


#Move to pre configured 
pre_home_b = ttk.Button(tab2, image = pre_home_image, width = 5, command = move_prepip_action)
pre_home_b.grid(column = 5, row = 4)
Tooltip(pre_home_b, text='Move to selected calibration position', wraplength=wraplength)


#Save Button - Calibration  
save_p = ttk.Button(tab2, image = save_button_image, width = 5, command = save_pip_action)
save_p.grid(column = 3, row = 4)
Tooltip(save_p, text='Save Calibration Point', wraplength=wraplength)

label_set_calibration = ttk.Button(tab2, text='Connect to Robot', command = connecton_graphical)
label_set_calibration.grid(column = 0, row = 7, columnspan = 3)
Tooltip(label_set_calibration, text='Connect to Robot UI, ensure robot is homed before calibration', wraplength=wraplength)


#Change Movement Speed
label = ttk.Label(tab2, text='Set Movement Speed:', font = ('Arial', 10))
label.grid(column = 1, row = 5)
#Scale Bar
scale_b = Scale(tab2, from_=0.1, to=10, resolution = 0.1, orient="horizontal", variable = head_speed_p)
scale_b.grid(column = 1, row = 6)
scale_b.set(1)
#Sync Entry Box
text = Entry(tab2, width=4, textvariable=head_speed_p)
text.grid(column = 0, row = 6, padx=5)
text.bind("<Return>", lambda event: scale_b.configure(to=head_speed_p.get()))
#Unit
label = ttk.Label(tab2, text='mm', font = ('Arial', 10))
label.grid(column = 2, row = 6)

# label = ttk.Label(tab2, text='Robot Position:', font = ('Arial', 10))
# label.grid(column = 1, row = 7)
# #Display Coordinate
# label = ttk.Label(tab2, textvariable=position_display_x)
# label.grid(column = 1, row = 8)
# position_display_x.set("x: 0") #Set Default Label


#Keyboard Input
root.bind("<Prior>", move_pip_action_up) #Page UP
root.bind("<Next>", move_pip_action_down) #PageDown


def key_press(event):
    if event.char == "R":
        move_pip_action_up()
    if event.char == "r":
        move_pip_action_up()
    if event.char == "f":
        move_pip_action_down()
    if event.char == "F":
        move_pip_action_down()

root.bind("<Key>", key_press)



#########################################################################################################

root.mainloop() 
#########################################################################################################

#Debugging (Run Graphical Interface without backend code)
