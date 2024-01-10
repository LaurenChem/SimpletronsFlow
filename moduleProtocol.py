from opentrons import robot, containers, instruments
#from opentrons import robot2

from moduleCommands import *
from moduleContainers import *
from modulePipetting import *
from time import sleep

import threading

#START UP GUI
from tkinter.ttk import Combobox
import tkinter as tk    
from tkinter import ttk
# For Jupiter Environment  
# from opentrons.util import environment
# environment.refresh()
# print(environment.get_path('CALIBRATIONS_FILE'))

# import os
# del os.environ['calibrations/calibrations.json']
# environment.refresh()

"""
 This Module require modules  modulePipetting and moduleContainer
 and moduleCommand to function. SQL read function are majority built in function
 below but some are reference using moduleCommands
 Please edit below test_save_data if you play around wish to use
 code to write your protocol. Please refer to documentation for more info 
"""

"""    
pipette_a = instruments.Pipette(
    axis='b',
    max_volume=200)
pipette_b = instruments.Pipette(
    axis='a',
    max_volume=200)
"""

def start_protocol():
    try:
        threading.Thread(target=start_protocol_temp('database/data.db')).start()
    except:
        print("Error Loading Protocol")
        pass


def start_protocol_temp(db_file):
    """
    Start Protocol based on information in database
    Any database shortcut please refer to moduleCommands
    Basic Transfer Supported 
    Other Shortcuts is currently WIP [Additional columns may be required for database more options]
    This API will grab all steps and send command to OT-1
    """
    #Home Robot (Note: Require user to be connected to robot using connection UI (Manual or Auto))
    #manual_connect()    
    #threading.Thread(target=home_robot()).start()
    home_robot()

    step_count = read_row('custom_protocol')
    print(step_count)

    #Connection to Custom Protocol Table
    conn = sqlite3.connect(db_file)
    c = conn.cursor()


    #Load Pipette
    # Load Blank Default Pipette
    global pipette_b
    global pipette_a


    #threading.Thread(target=New_UI()).start()

    sqlite_select_query = """SELECT * FROM custom_pipette"""
    c.execute(sqlite_select_query) 
    for row in c:
        print(row)

        rawTip = row[7]
        rawTrash = row[8]

        tipName = rawTip[0:2]
        tipType = rawTip[3:]

        trashName = rawTrash[0:2]
        trashType = rawTrash[3:]

        tiprack = containers.load(trashType, tipName, 'tiprack')
        trash = containers.load(tipType, trashName, 'trash')

        axis_s = row[1]

        if axis_s == 'b':
            pipette_b = instruments.Pipette(
            axis='b',
            name='pipette_b',
            max_volume=row[2],
            min_volume=row[3],
            channels = row[4],
            aspirate_speed=row[5],
            dispense_speed=row[6],
            tip_racks=tiprack,
            trash_container=trash
            )
            print ("Loaded B Axis Pipette")
            # Calibrate Tip Track and Bin
            #Load Calibration Data
            calibarate_data = find_data("custom_workspace", trashName)
            robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
            robot.move_head(z=calibarate_data[6], strategy='direct')

            pos = trash[0].from_center(x=0, y=0, z=-1, reference=trash)
            pipette_b.calibrate_position((trash, pos))
            robot.move_head(z=60, strategy='direct') # Move Clear Labware
            
            
            calibarate_data = find_data("custom_workspace", tipName)
            robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
            robot.move_head(z=calibarate_data[6], strategy='direct')

            pos = tiprack[0].from_center(x=0, y=0, z=-1, reference=tiprack)
            pipette_b.calibrate_position((tiprack, pos))
            robot.move_head(z=60, strategy='direct') # Move Clear Labware   

            #Pick Up Tip [ Pick Up Tips ]
            pipette_b.pick_up_tip(tiprack[0])
            robot.move_head(z=60, strategy='direct')           

        if axis_s == 'a':
            """ Not Complete Yet """
            pipette_a = instruments.Pipette(
            axis='a',
            name='pipette_a',
            max_volume=row[2],
            min_volume=row[3],
            channels = row[4],
            aspirate_speed=row[5],
            dispense_speed=row[6],
            tip_racks=tiprack,
            trash_container=trash
            )
            print ("Loaded A Axis Pipette")
            calibarate_data = find_data("custom_workspace", trashName)
            robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
            robot.move_head(z=calibarate_data[6], strategy='direct')

            pos = trash[0].from_center(x=0, y=0, z=-1, reference=trash)
            pipette_a.calibrate_position((trash, pos))
            robot.move_head(z=60, strategy='direct') # Move Clear Labware
            
            
            calibarate_data = find_data("custom_workspace", tipName)
            robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
            robot.move_head(z=calibarate_data[6], strategy='direct')

            pos = tiprack[0].from_center(x=0, y=0, z=-1, reference=tiprack)
            pipette_a.calibrate_position((tiprack, pos))
            robot.move_head(z=60, strategy='direct') # Move Clear Labware 

            #Pick Up Tip [ Pick Up Tips ]
            pipette_b.pick_up_tip(tiprack[0])
            robot.move_head(z=60, strategy='direct')  

    #Load protocol in loaded in workspace
    sqlite_select_query = """SELECT * FROM custom_protocol"""
    c.execute(sqlite_select_query) 
    """ Basic Transfer
    Load Temp Custom Protocol 
    It will read each row and send command for each step.
    Uncomment out print(row) if you wish to see output.

    """
    for row in c:
        print("Loaded Below Protocol from database")
        print(row)

        # global pipette_b
        # global pipette_a

        #Load Variable from database row
        id_count = row[0] 

        shortcut = row[2] # Shortcut 

        pipette = row[3] # Pipette

        volume = row[4] # Volume

        plateA = row[5] #Plate A
        wellA = row[6] #Well A

        plateB = row[7]
        wellB = row[8]

        change_tip = row[9] #Option 1: Change Tip

        row_col = row[10] #Conditional Option (One to Many - Rows or Columns)

        mix_after = row[11] # whether the well should be mixed after dispensing
        #Note: https://docs.opentrons.com/ot1/transfer.html 
        #Use above resource for opentrons implementing future API shortcut
        #Send Action to Robot 
        if shortcut == "Simple_Transfer":
            ''' [ Simple Transfer ] 
            Do Note: Calibration data is stored on database in separated columns for pipette A and B 
            The Protocol won't run if calibration data is incorrect or blank. 
            '''
            if pipette == "pipette_b":

                
                #First Plate Initialisation 
                plateAName = plateA[0:2]
                planteAType = plateA[3:]
                #print(plateAName)
                #print(planteAType)

                plateA = containers.load(planteAType, plateAName, 'plateA')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateAName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container:", plateBName)
                    break

                pos = plateA[0].from_center(x=0, y=0, z=-1, reference=plateA)
                pipette_b.calibrate_position((plateA, pos))
                robot.move_head(z=60, strategy='direct')

                #Second Plate Initialisation 
                plateBName = plateB[0:2]
                planteBType = plateB[3:]
                #print(plateBName)
                #print(planteBType)

                plateB = containers.load(planteBType, plateBName, 'plateB')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateBName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container:", plateBName)
                    break

                pos = plateB[0].from_center(x=0, y=0, z=-1, reference=plateB)
                pipette_b.calibrate_position((plateB, pos))
    
                #print(option)
                # This will send command to perform desire task  
                if change_tip == '1':
                    pipette_b.transfer(volume, plateA.wells(wellA), plateB.wells(wellB), new_tip='never')
                    print("Complete: Step", id_count, ": Option: Never Change")

                else:
                    pipette_b.transfer(volume, plateA.wells(wellA), plateB.wells(wellB), new_tip='always')
                    print("Complete: Step", id_count, ": Option: Always")

                for c in robot.commands():
                    print(c)                    

            if pipette == "pipette_a":
                ''' Pipette A'''
                #First Plate Initialisation 
                plateAName = plateA[0:2]
                planteAType = plateA[3:]
                #print(plateAName)
                #print(planteAType)

                plateA = containers.load(planteAType, plateAName, 'plateA')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateAName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container")
                    #break

                pos = plateA[0].from_center(x=0, y=0, z=-1, reference=plateA)
                pipette_a.calibrate_position((plateA, pos))
                robot.move_head(z=60, strategy='direct')


                #Second Plate Initialisation 
                plateBName = plateB[0:2]
                planteBType = plateB[3:]
                #print(plateBName)
                #print(planteBType)

                plateB = containers.load(planteBType, plateBName, 'plateB')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateBName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container")
                    #break

                pos = plateB[0].from_center(x=0, y=0, z=-1, reference=plateB)
                pipette_a.calibrate_position((plateB, pos))
    
                #print(option)
                # This will send command to perform desire task  
                if change_tip == '1':
                    pipette_a.transfer(volume, plateA.wells(wellA), plateB.wells(wellB), new_tip='never')
                    print("Complete: Step", id_count, ": Option: Never Change")

                else:
                    pipette_a.transfer(volume, plateA.wells(wellA), plateB.wells(wellB), new_tip='always')
                    print("Complete: Step", id_count, ": Option: Always")

                for c in robot.commands():
                    print(c)


        if shortcut == "One_to_Many":
            ''' One_to_Many
            [ You can transfer from a single source to multiple destinations, and the other way around 
            (many sources to one destination).  ] 
            '''
            if pipette == "pipette_b":

                #First Plate Initialisation 
                plateAName = plateA[0:2]
                planteAType = plateA[3:]
                print(plateAName)
                #print(planteAType)

                plateA = containers.load(planteAType, plateAName, 'plateA')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateAName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    """
                    Check and Visits Calibration Location
                    """
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container")
                    break

                pos = plateA[0].from_center(x=0, y=0, z=-1, reference=plateA)
                pipette_b.calibrate_position((plateA, pos))
                robot.move_head(z=60, strategy='direct')


                #Second Plate Initialisation 
                plateBName = plateB[0:2]
                planteBType = plateB[3:]
                #print(plateBName)
                #print(planteBType)

                plateB = containers.load(planteBType, plateBName, 'plateB')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateBName)
               
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    """
                    Check and Visits Calibration Location
                    """
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='arc')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container")
                    break

                pos = plateB[0].from_center(x=0, y=0, z=-1, reference=plateB)
                pipette_b.calibrate_position((plateB, pos))


                if row_col == "rows":
                    # Never Get a New Tip each steps
                    if change_tip == '1':
                        pipette_b.transfer(volume, plateA.wells(wellA), plateB.rows(wellB), new_tip='never')

                    if change_tip == '0':
                        pipette_b.transfer(volume, plateA.wells(wellA), plateB.rows(wellB), new_tip='always')

                if row_col == "cols":
                    if change_tip == '1':
                        pipette_b.transfer(volume, plateA.wells(wellA), plateB.cols(wellB), new_tip='never')

                    if change_tip == '0':
                        pipette_b.transfer(volume, plateA.wells(wellA), plateB.cols(wellB), new_tip='always')

                #consolidate (Don't change tip)


                for c in robot.commands():
                    print(c)                    

            if pipette == "pipette_a":

                #First Plate Initialisation 
                plateAName = plateA[0:2]
                planteAType = plateA[3:]
                print(plateAName)
                #print(planteAType)

                plateA = containers.load(planteAType, plateAName, 'plateA')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateAName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    """
                    Check and Visits Calibration Location
                    """
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container")
                    break

                pos = plateA[0].from_center(x=0, y=0, z=-1, reference=plateA)
                pipette_a.calibrate_position((plateA, pos))
                robot.move_head(z=60, strategy='direct')


                #Second Plate Initialisation 
                plateBName = plateB[0:2]
                planteBType = plateB[3:]
                #print(plateBName)
                #print(planteBType)

                plateB = containers.load(planteBType, plateBName, 'plateB')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateBName)
               
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    """
                    Check and Visits Calibration Location
                    """
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='arc')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container")
                    break

                pos = plateB[0].from_center(x=0, y=0, z=-1, reference=plateB)
                pipette_a.calibrate_position((plateB, pos))


                if row_col == "rows":
                    # Never Get a New Tip each steps
                    if change_tip == '1':
                        pipette_a.transfer(volume, plateA.wells(wellA), plateB.rows(wellB), new_tip='never')

                    if change_tip == '0':
                        pipette_a.transfer(volume, plateA.wells(wellA), plateB.rows(wellB), new_tip='always')

                if row_col == "cols":
                    if change_tip == '1':
                        pipette_a.transfer(volume, plateA.wells(wellA), plateB.cols(wellB), new_tip='never')

                    if change_tip == '0':
                        pipette_a.transfer(volume, plateA.wells(wellA), plateB.cols(wellB), new_tip='always') 
                for c in robot.commands():
                    print(c)
    
        if shortcut == "Mixing":
                      
            if pipette == "pipette_b":
                
                #First Plate Initialisation 
                plateAName = plateA[0:2]
                planteAType = plateA[3:]
                #print(plateAName)
                #print(planteAType)

                plateA = containers.load(planteAType, plateAName, 'plateA')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateAName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container:", plateBName)
                    break

                pos = plateA[0].from_center(x=0, y=0, z=-1, reference=plateA)
                pipette_b.calibrate_position((plateA, pos))
                robot.move_head(z=60, strategy='direct')

                #Second Plate Initialisation 
                plateBName = plateB[0:2]
                planteBType = plateB[3:]
                #print(plateBName)
                #print(planteBType)

                plateB = containers.load(planteBType, plateBName, 'plateB')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateBName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container:", plateBName)
                    break

                pos = plateB[0].from_center(x=0, y=0, z=-1, reference=plateB)
                pipette_b.calibrate_position((plateB, pos))
    
                #print(change_tip)
                # This will send command to perform desire task  
                if change_tip == '1':
                    for repeat in range(4):
                        pipette_b.transfer(volume, plateA.wells(wellA), plateB.wells(wellA), new_tip='never')

                    print("Complete: Step", id_count, ": Option: Never Change")

                else:
                    for repeat in range(3):
                        pipette_b.transfer(volume, plateA.wells(wellA), plateB.wells(wellA), new_tip='never')
                    pipette_b.transfer(volume, plateA.wells(wellA), plateB.wells(wellA), new_tip='always')
                    print("Complete: Step", id_count, ": Option: Always")

                for c in robot.commands():
                    print(c)                    

            if pipette == "pipette_a":
                ''' Pipette A'''
                #First Plate Initialisation 
                plateAName = plateA[0:2]
                planteAType = plateA[3:]
                #print(plateAName)
                #print(planteAType)

                plateA = containers.load(planteAType, plateAName, 'plateA')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateAName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container")
                    #break

                pos = plateA[0].from_center(x=0, y=0, z=-1, reference=plateA)
                pipette_a.calibrate_position((plateA, pos))
                robot.move_head(z=60, strategy='direct')


                #Second Plate Initialisation 
                plateBName = plateB[0:2]
                planteBType = plateB[3:]
                #print(plateBName)
                #print(planteBType)

                plateB = containers.load(planteBType, plateBName, 'plateB')
                
                #Load Calibration Data
                calibarate_data = find_data("custom_workspace", plateBName)
                #Check Calibration Data
                if (calibarate_data[4] != 0 and calibarate_data[5] != 0 and calibarate_data[6] != 0):
                    robot.move_head(x=calibarate_data[4],y=calibarate_data[5],z=60, strategy='arc')
                    robot.move_head(z=calibarate_data[6], strategy='direct')
                    print("Calibration Loaded")
                else:
                    print("Calibration Data not available. please calibrate this container")
                    #break

                pos = plateB[0].from_center(x=0, y=0, z=-1, reference=plateB)
                pipette_a.calibrate_position((plateB, pos))
    
                #print(option)
                # This will send command to perform desire task  
                # This will send command to perform desire task  
                if change_tip == '1':
                    for repeat in range(4):
                        pipette_a.transfer(volume, plateA.wells(wellA), plateB.wells(wellA), new_tip='never')

                    print("Complete: Step", id_count, ": Option: Never Change")

                else:
                    for repeat in range(3):
                        pipette_a.transfer(volume, plateA.wells(wellA), plateB.wells(wellA), new_tip='never')

                    pipette_a.transfer(volume, plateA.wells(wellA), plateB.wells(wellA), new_tip='always')
                    print("Complete: Step", id_count, ": Option: Always")

                for c in robot.commands():
                    print(c)           




    #Finally both Drop Tip at end of protocol
    try:
        pipette_b.drop_tip()
    except:
        pass
        print("Skip Drop Tip: B")
    try:
        pipette_a.drop_tip()
    except:
        pass
        print("Skip Drop Tip: A")

    #Exit Database 
    try:
        conn.close() 
    except:
        pass
        print("Error ")     


    print('Successfully Completed Protocol Run')

 
def test_save_data_demo():
    """ Debugging Temp Data"""

    #1 Setup Pipette Default
    # Axis , max volume , min volume, channel (1 or 8), aspirate speed, dispense speed, tip rack, bin
    insert = ('b', '1000', '100', '1', 800, 1200, 'A2_tiprack-1000ul', 'B2_point')
    save_data("custom_pipette", insert) 

    #2 Setup Bare Minimal Workspace
    name = "A1" # Container Name
    container = "24-well-plate" # Container Type 
    location = "A1" # Location Position on workspace
    x = "44.068" #Manual Calibration Data [DO NOT EDIT If you don't know actual value]
    y = "14.4053"
    z = "-65.9"
    xx = "0"
    yy ="0"
    zz = "0"

    insert = (name, container, location, x, y, z, xx, yy, zz)
    save_data("custom_workspace", insert)

    name = "B1" # Container Name
    container = "48-well-plate" # Container Type 
    location = "B1" # Location Position on workspace
    x = "131.0789" #Manual Calibration Data [DO NOT EDIT If you don't know actual value]
    y = "15.46" # Pipette B
    z = "-67.8"
    xx = "0"
    yy ="0"
    zz = "0"

    insert = (name, container, location, x, y, z, xx, yy, zz)
    save_data("custom_workspace", insert)
    
    name = "B2" # Container Name
    container = "B2_point" # Container Type 
    location = "B2" # Location Position on workspace
    x = "159.0074" #Manual Calibration Data [DO NOT EDIT If you don't know actual value]
    y = "190.4798"
    z = "-46.0"
    xx = "0"
    yy ="0"
    zz = "0"

    insert = (name, container, location, x, y, z, xx, yy, zz)
    save_data("custom_workspace", insert)
    
    name = "A2" # Container Name
    container = "A2_tiprack-1000ul" # Container Type 
    location = "A2" # Location Position on workspace
    x = "39.2424" #Manual Calibration Data [DO NOT EDIT If you don't know actual value]
    y = "146.85"
    z = "-72"
    xx = "0"
    yy ="0"
    zz = "0"

    insert = (name, container, location, x, y, z, xx, yy, zz)
    save_data("custom_workspace", insert)

    #4 Step Demo (Simple Transfer)
    name = "Step 1" # Step Name 
    shortcuts = "Simple_Transfer" #Transfer Shortcut [Refer To Documentation]
    sel_pipette = "pipette_b" # Pipette Name (pipette_b or pipette_a)
    volume = 100 # Volume (Double Variable)
    aspirate_container = "B1_48-well-plate"  #First Plate Full Name (Require initial 3 variable is require for location)
    aspirate_well = "B1" #Well Cell for first plate
    dispense_container = "B1_48-well-plate" #Second Plate Full Name (Require initial 3 variable is require for location)
    dispense_well = "B2" #Well Cell for second plate
    change_tip = True #Never Change Tip Enable (False for always change tip)
    row_col = None #Additional Parameters 
    mixing = None
    notes = "Simple Transfer From 24 well plate to 48 well plate"

    #Insert To Database Function
    insert = (name, shortcuts, sel_pipette, volume, aspirate_container, aspirate_well, dispense_container, dispense_well, change_tip, row_col, mixing, notes)
    save_data("custom_protocol", insert)
    
    
    #5 Step Demo (one to many)
    name = "Step 2" 
    shortcuts = "One_to_Many"
    sel_pipette = "pipette_b"
    volume = 200
    aspirate_container = "A1_24-well-plate"
    aspirate_well = "A2"
    dispense_container = "B1_48-well-plate"
    dispense_well = "1"
    change_tip = True
    row_col = 'rows' # For one to Many you can set to transfer to whole rows or cols by changing this. 
                    # DO not value need to just a number (rows) or a letter (cols)
    notes = "test notes"

    #Insert To Database Function
    insert = (name, shortcuts, sel_pipette, volume, aspirate_container, aspirate_well, dispense_container, dispense_well, change_tip, row_col, mixing, notes)
    save_data("custom_protocol", insert)  

#Load Test Data Condition [Comment Out if you require debugging Protocol API]
#It will load a test data



 
# setup_table("custom_protocol")
# setup_table("custom_pipette")
# setup_table("custom_workspace")


# test_save_data() #Load Test data in database
# start_protocol() #Start Protocol

# """
# You would need to delete table upon exiting database 

# If you getting data base lock, you need to delete database/data.db and 
# recreate the file. 

# [This is only require if the code crash during protocol]

# """
# deleteTable("custom_protocol") 
# deleteTable("custom_pipette")
# deleteTable("custom_workspace")

# Cross Linking Platform Code
# If you wish to work on this section, you require custom library from original raspberry pi with
# library "robot2" , standalone library does not include robot2 from opentrons pip library.
# 
# Another method is to copy original robot api from original source 

#transportposition = getTransportposition()

# intensity range
# PWM = (0-(-0.1251))/0.0161 = 8.0

# example: intensity = 2.5
# PWM = (2.5-(-0.1251))/0.0161 = 163

# lightON = 'M106'
# lightOFF = 'M107'

# def crosslinking():
#     # absolute movement
#     robot._driver.send_command('G90')
#     # move plate in crosslinker module
#     move_to_moduleCrosslinker()
#     # specifiy intensity
#     robot2._driver.send_command('G0 Z280')
#     # define PWM value for specified intensity
#     # example
#     robot2._driver.send_command('M106 S132')
#     # LEDs on
#     robot2._driver.send_command(lightON)
#     # crosslinking duration in seconds
#     # sleep(duration)
#     # example
#     # duration = 120 s
#     sleep(30)
#     # LEDs off
#     robot2._driver.send_command(lightOFF)
