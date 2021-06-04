##################################################################################
import opentrons
#import openworkstation
from opentrons import robot, robot2, containers, instruments
#from openworkstation import robot2
from time import sleep
from moduleCommands import *
##################################################################################

    
def create_container(name, grid_c, grid_r, spacing_c, spacing_r, diameter, depth, deck):
    #Creating Container
    print('Creating "', name, '" Container') 
    containers.create(
        name,                    # name of you container
        grid=(grid_c, grid_r),                    # specify amount of (columns, rows)
        spacing=(spacing_c, spacing_r),               # distances (mm) between each (column, row)
        diameter=diameter,                     # diameter (mm) of each well on the plate
        depth=depth                     # depth (mm) of each well on the plate
    )
    print('Custom Container Created "', name '"')

    #Load Container 
    var = container.load(name, location)


def load_container(name, location, var):
    print('Loading Container', name) #                       
    var = container.load(name, location)
    print('Loaded Container', name) # 


#Load some useful default containers 
def load_dd_container():
    print ('Loading Default Preset Containers')
    trashA = container.load('point', 'A1') 
    P_A = container.load('tiprack-1000ul-chem', A2)
    P_B = ontainer.load('tiprack-1000ul-chem', A3)
    print('Loaded Containe "trashA" ')
