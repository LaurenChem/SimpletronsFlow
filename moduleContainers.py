##################################################################################
import opentrons
#import openworkstation
from opentrons import robot, containers, instruments
#from openworkstation import robot2
from time import sleep
from moduleCommands import *
##################################################################################

def create_container(name, grid_c, grid_r, spacing_c, spacing_r, diameter, depth):
    """ Creating Container

    Due to nature of opentrons API, ensure you load this custom container each time you start 
    your protocol. 

    create_container( [name of you container], [specify amount of columns], [specify amount of rows], 
                     [distances (mm) between each column], [distances (mm) between each row], 
                     [diameter (mm) of each well on the plate], [depth (mm) of each well on the plate])

    """

    print('Creating "', name, '" Container') 
    containers.create(
        name,                    # name of your container
        grid=(grid_c, grid_r),                    # specify amount of (columns, rows)
        spacing=(spacing_c, spacing_r),               # distances (mm) between each (column, row)
        diameter=diameter,                     # diameter (mm) of each well on the plate
        depth=depth                     # depth (mm) of each well on the plate
    )


def load_container(name, location, container):
    """ 
    Load Container [Deprecated]

    """

    global A1
    global A2
    global A3

    global B1
    global B2
    global B3

    global C1
    global C2
    global C3

    global D1
    global D2
    global D3

    global E1
    global E2 
    global E3 

    print(name)

    name = name

    print('Loading Container', name) #                       
    name = containers.load(container, location, name) # Load Container to a location
    print('Loaded Container', name) # 

    #For Debug - To check the loaded container is correct or not
    
    #for well in name.wells():
    #    print(well)


#Load some useful default containers []
def load_dd_container():
    """ 
    Load Default Container [Deprecated]

    """
    print ('Loading Default Preset Containers')
    #trashA = containers.load('trash-box', 'A1') 
    #P_A = containers.load('tiprack-1000ul-chem', 'A2')
    #P_B = containers.load('tiprack-1000ul-chem', 'A3')
    print('Loaded default Container')

#create_container(test_c, 10, 10, 2, 5, 5, 1)