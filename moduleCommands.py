######################################################################
# Please Do NOT Modify Unless You Know What you're doing #

######################################################################


#from time import sleep

import sqlite3
from sqlite3 import Error

#import json
import re

#import warnings
import serial
import serial.tools.list_ports

#import opentrons
# Opentrons 2.5.2 (pip install opentrons==2.5.2)
from opentrons import robot
#from opentrons import robot, containers, instruments

#from moduleTransportation import getTransportposition
#from modulePipetting import *
#from moduleCalibrate import *

#Import threading
import threading

#Copy File
from shutil import copyfile
######################################################################
db_file = 'database/data.db' 

def find_robot(serial_number):
    """ # Self Find Serial Port # """
    for pinfo in serial.tools.list_ports.comports():
        if pinfo.serial_number == serial_number:
            return serial.Serial(pinfo.device)
    raise IOError("[#A1] Could not find an Robot - is it plugged in or is serial number setup correct?")

def check_file():
    """" Read text file """
    try:
        with open('usbSerial.txt') as f:
            lines = f.readlines() #Read UsbSerial file
            lines = [line.replace(' ', '') for line in lines] #Remove Empty Spaces
        return lines
    except:
        return lines
        print('[#A7] Error reading usbSerial text file, please double check the file exist and value is entered within the brackets')
        pass

    
# Default Load QUT OT-1 Robot
def find_ot():
    """Load Serial Number from File"""
    try:
        # Run 'python3 tools/toolScanner.py' to obtain serial number for your printer
        serial = check_file()
        print(serial)
        #robotUSB = find_arduino(serial_number='05012004AEFC104858093B9CF50020C3') #Configurable Serial
        robotUSB = find_robot(serial) #Configurable Serial
        robotUSB = str(robotUSB) #Array to Convert to string
        robotUSB = re.findall(r"port='(.*?)'", robotUSB)
        robotUSB = str(robotUSB) #Array to Convert to string
        robotUSB = str(robotUSB).strip('['']') #Remove Brackets
        robotUSB = eval(robotUSB) #Remove Quotation
    except:
        print('[#A2] Error Phrasing serial number, please submit issue on github')
        pass
    #print(robotUSB)

#######################################################################
#Connection To both Robot
#######################################################################

def connect():
    """Connect to Robot"""
    print('Connecting to Robots')
    try:
        #find_ot()
        robot.connect('Virtual Smoothie')
        versions = robot.versions()
        print('Opentrons Robot Connected, Robot Firmware Version:', versions)

        try:    
            robot2.connect()
            robot2.connect(robot2USB)
            print('Opentrons Robot Connected')
        except:
            print('Opentrons Robot Not Connected')
            print('[#A3] Running Debugging Mode')            
    except:
        print('Opentrons Robot Not Connected')
        print('[#A3] Running Debugging Mode')

def manual_connect():
    """ Connect to Robot """
    print('Manual - Connecting to Robots')
    try:
        robot.connect("/dev/ttyACM0")
        versions = robot.versions()
        print('Opentrons Robot Connected, Robot Firmware Version:', versions)
    except:
        print('Opentrons Robot Not Connected')
        print('[#A3] Running Debugging Mode')

def home_all():
    """Home Both Robot [Home Main Opentron Robot First - Then Storage]"""
    try:
        print('Homing Opentrons Robot in progress')
        robot.home()
        print('Successfully Homed Opentrons Robot Complete')
        try: 
            #Home Robot 2
            robot2._driver.send_command('G28.2 Y Z')
            robot2._driver.send_command('G28.2 A')
            robot2._driver.send_command('G28.2 B')
            robot2._driver.send_command('G28.2 X')
            robot2._driver.send_command('G90')
            print('Successfully Homed Transport Robot')
        except:
            print('[#A4] Robot 2 Not Loaded')
            pass
    except: 
        print('[#A5] Running Debugging Mode')
        pass


def home_robot():
    """Homes OT-1 Axis For Opentrons Robot"""
    try:
        print('Homing Opentrons Robot in progress')
        robot.home()
        print('Successfully Homed Opentrons Robot Complete')
    except: 
        print('[#A6] Running Debugging Mode')
        print('[#H1] Unable to Home Robot')
        pass

def home_robot2():
    """Homes Storage Robot Axis For Transport Robot"""
    try:
        print('Homing Transport Robot in progress')
        robot2._driver.send_command('G28.2 Y Z')
        robot2._driver.send_command('G28.2 A')
        robot2._driver.send_command('G28.2 B')
        robot2._driver.send_command('G28.2 X')
        robot2._driver.send_command('G90')
        print('Successfully Homed Transport Robot')
    except: 
        print('[#A5] Note: Running Debugging Mode')
        print('[#H2] Unable to Home Robot2')
        pass

#Reset Connection [OT-1 First - Then Storage Robot]
def reset_all():
    """Reset Connection"""
    try:
        #Reset Robot Opentron Robot
        print('Reseting Opentrons Robot')
        robot.reset()
        print('Successfully Rested Opentrons Robot')
        try: 
            #ResetRobot 2(Transport Platforms)
            print('Reseting Transport Robot')
            robot2.reset()
            print('Successfully Rested Robot2')
        except:
            print('[#A5] Note: Running Debugging Mode')
            print('[#H2] Unable to Reset Robot2')
            pass
    except:
        print('[#A5] Note: Only Opentrons Is connected')
        print('[#H2] Unable to Reset Robot2')
        pass

def stop_robot():
    threading.Thread(target=robot.stop()).start()
    print('STOPPING ROBOT / Protocol')


def pause_robot():
    threading.Thread(target=robot.pause()).start()
    print('PAUSING ROBOT / Protocol')


def resume_robot():
    threading.Thread(target=robot.resume()).start()
    print('RESUMING ROBOT / Protocol')


##################################################################
# Database
##################################################################
# Test Connection


def create_connection():
    """create a test database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        print('Database Found')
    except Error as e:
        print(e)
        print('[#A8] Error Loading Database')


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement"""
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)

#Delete A Single Record
def deleteRecord(variable, id):
    """Delete Single Record Table"""
    try:
        c = conn.cursor()
        print("Connected to SQLite")

        # Delete single row of data
        if variable == "custom_container":
            sql_delete_query = """DELETE FROM custom_container WHERE id=?;"""

        if variable == "custom_workspace":
            sql_delete_query = """DELETE FROM custom_workspace WHERE id=?;"""

        if variable == "custom_protocol":
            sql_delete_query = """DELETE FROM custom_protocol WHERE id=?;"""

        c.execute(sql_delete_query)
        conn.commit()
        print("Record deleted successfully ")
        conn.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)

#Delete Whole Table
def deleteTable(variable):
    """Delete Table"""
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        #print("Connected to SQLite")

        # Deleting Whole Table Values
        if variable == "custom_container":
            sql_delete_query = """DELETE FROM custom_container;"""

        if variable == "custom_workspace":
            sql_delete_query = """DELETE FROM custom_workspace;"""

        if variable == "custom_protocol":
            sql_delete_query = """DELETE FROM custom_protocol;"""

        if variable == "custom_pipette":
            sql_delete_query = """DELETE FROM custom_pipette;"""
        c.execute(sql_delete_query)
        conn.commit()
        print("Record deleted successfully ")
        conn.close()

    except sqlite3.Error as error:
        print("Failed to delete whole table from sqlite", error)

#Save Data to specific database
def save_data(table, insert):
    """Insert/Save Data into table"""
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    if table == "custom_pipette":
        sql_insert_template = ''' INSERT INTO custom_pipette(axis, max_volume, min_volume, channels, aspirate_speed, dispense_speed, tip_racks, trash_container)
            VALUES(?,?,?,?,?,?,?,?) '''

    if table == "custom_container":
        sql_insert_template = ''' INSERT INTO custom_container(name, grid_c, gri`d_r, spacing_c, diameter, depth)
            VALUES(?,?,?,?,?,?) '''

    if table == "custom_workspace":
        sql_insert_template = ''' INSERT INTO custom_workspace(name, container, location, x , y, z, xx, yy, zz)
            VALUES(?,?,?,?,?,?,?,?,?) '''

    if table == "custom_workspace_a":
        sql_insert_template = ''' INSERT INTO custom_workspace(name, container, location, xx, yy, zz)
            VALUES(?,?,?,?,?,?) '''

    if table == "custom_workspace_b":
        sql_insert_template = ''' INSERT INTO custom_workspace(name, container, location, x , y, z)
            VALUES(?,?,?,?,?,?) '''


    if table == "custom_protocol":
        sql_insert_template = ''' INSERT INTO custom_protocol(name, shortcuts, pipette, volume, aspirate_container, aspirate_well, dispense_container, dispense_well, change_tip, row_col, mix_after, notes)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''

    #Excute Task to Database
    c.execute(sql_insert_template, insert)
    conn.commit() # Save
    print("Record Added successfully to", table)
    conn.close()  # Close database


def update_data(table, update):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # if table == "custom_pipette":
    #     sql_insert_template = ''' INSERT INTO custom_pipette(axis, max_volume, min_volume, channels, aspirate_speed, dispense_speed, tip_racks, trash_container)
    #         VALUES(?,?,?,?,?,?,?,?) '''

    # if table == "custom_container":
    #     sql_insert_template = ''' INSERT INTO custom_container(name, grid_c, gri`d_r, spacing_c, diameter, depth)
    #         VALUES(?,?,?,?,?,?) '''

    # if table == "custom_workspace":
    #     sql_insert_template = ''' INSERT INTO custom_workspace(name, container, location, x , y, z, xx, yy, zz)
    #         VALUES(?,?,?,?,?,?,?,?,?) '''

    # if table == "custom_workspace_a":
    #     sql_insert_template = ''' INSERT INTO custom_workspace(name, container, location, xx, yy, zz)
    #         VALUES(?,?,?,?,?,?) '''

    # if table == "custom_workspace_b":
    #     sql_insert_template = ''' INSERT INTO custom_workspace(name, container, location, x , y, z)
    #         VALUES(?,?,?,?,?,?) '''

    if table == "custom_protocol":
        sql_insert_template = '''UPDATE custom_protocol 
                        SET name=?, 
                        shortcuts = ?, 
                        pipette=?, 
                        volume=?, 
                        aspirate_container=?, 
                        aspirate_well=?, 
                        dispense_container = ?, 
                        dispense_well = ?, 
                        change_tip = ?, 
                        row_col = ?,
                        mix_after = ?,
                        notes =  ?
                        WHERE id = ?;'''


    #Excute Task to Database
    c.execute(sql_insert_template, update)
    conn.commit() # Save
    print("Record Added successfully to", table)
    conn.close()  # Close database


# Find Data
def find_data(table, name):
    if table == "custom_workspace":
        if name == "A1":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%A1%'"""
        if name == "A2":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%A2%'"""        
        if name == "A3":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%A3%'"""
        if name == "B1":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%B1%'"""
        if name == "B2":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%B2%'"""        
        if name == "B3":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%B3%'"""
        if name == "C1":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%C1%'"""
        if name == "C2":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%C2%'"""        
        if name == "C3":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%C3%'"""
        if name == "D1":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%D1%'"""
        if name == "D2":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%D2%'"""        
        if name == "D3":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%D3%'"""
        if name == "E1":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%E1%'"""
        if name == "E2":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%E2%'"""        
        if name == "E3":
            sqlite_select_query = """SELECT * FROM custom_workspace where name like '%E3%'"""

    conn = sqlite3.connect(db_file)
    c = conn.cursor()           

    c.execute(sqlite_select_query)        
    for row in c:
        print(row)

    #Close Database Connection
    conn.close()          
    return(row)

# #Read Data
def read_row(table):
    """Read Number of Rows from Database"""
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    #Read Number of rows
    if table == "custom_container":
        sqlite_select_query = """SELECT * FROM custom_container"""
    if table == "custom_workspace":
        sqlite_select_query = """SELECT * FROM custom_workspace"""
    if table == "custom_protocol":
        sqlite_select_query = """SELECT * FROM custom_protocol"""

    c.execute(sqlite_select_query)        
    x = c.fetchall()

    result = c.fetchall()
    

    # while row is not None:
    #     print(row)
    #     row = c.fetchone()
    
    print("Total rows are:  ", len(x))

    for row in result:
        print(row)

    #Close Database Connection
    conn.close()  
    return len(x)

#read_row('custom_protocol')

def setup_table(variable):
    """Custom container Database Creation"""
    if variable == "custom_container":
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS custom_container (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            grid_c REAL,
                                            grid_r REAL,
                                            spacing_c REAL,
                                            diameter REAL,
                                            depth REAL
                                        ); """

    """Custom Pipette Database Creation"""
    if variable == "custom_pipette":
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS custom_pipette (
                                            id integer PRIMARY KEY,
                                            axis text NOT NULL,
                                            max_volume REAL,
                                            min_volume REAL,
                                            channels int,
                                            aspirate_speed REAL,
                                            dispense_speed REAL,
                                            tip_racks text,
                                            trash_container text
                                        ); """

    #Custom workspace Database Creation
    if variable == "custom_workspace":
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS custom_workspace (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            container text,
                                            location text,
                                            x REAL, 
                                            y REAL,
                                            z REAL,
                                            xx REAL, 
                                            yy REAL,
                                            zz REAL
                                        ); """

    #Custom protocol Database Creation - Temp
    if variable == "custom_protocol":
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS custom_protocol (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            shortcuts text NOT NULL,
                                            pipette text NOT NULL,
                                            volume REAL NOT NULL,
                                            aspirate_container text,
                                            aspirate_well text,
                                            dispense_container text,
                                            dispense_well text,
                                            change_tip text,
                                            row_col text,
                                            mix_after text,
                                            notes text
                                        ); """

    # Persist Storage 
    if variable == "persist_protocol":
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS custom_protocol (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            shortcuts text NOT NULL,
                                            pipette text NOT NULL,
                                            volume REAL NOT NULL,
                                            aspirate_container text,
                                            aspirate_well text,
                                            dispense_container text,
                                            dispense_well text,
                                            change_tip boolean,
                                            row_col text,
                                            mix_after text,
                                            notes text
                                        ); """

    #Data Base Connection                                    
    conn = sqlite3.connect(db_file)

    #Check if connection is made successfully before writing data
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)
        print("Successfully Created", variable)

    else:
        print("Error! cannot create the database connection.")




def dump_database(filename):
    '''
    Copy/Export Database 

    '''
    filename = 'export/'+str(filename)+'.db'    

    copyfile(db_file, str(filename))
    print("Successfully Copied db to another db")

###########################################################################################################
#
# JSON IMPORT FUNCTION
#
###########################################################################################################
#WIP - Require JSON file to be updated to have proper separation of each container
# def load_default_containers():
#     with open("database/default-containers.json") as file:
#         default_containers = json.load(file)

#     temp = default_containers['containers'][0]
#     print(temp)

#load_default_containers()