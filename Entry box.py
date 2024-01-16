import os


import tkinter as tk
from tkinter import ttk

root = tk.Tk()
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='Step 1 Containers Setup')
tabControl.pack(expand = 1, fill ="both")

##-----------Select Pipette-----------##
var_pipette_axis = tk.IntVar()
#Selection 1 - Axis
label_axis = ttk.Label(tab1, text='Select a Axis:', font = ('Arial', 12))
label_axis.grid(column = 1, row = 0)

#Scale Bar
select_pipette_scale = tk.Scale(tab1, from_=0, to=1, resolution = 1, orient="horizontal", variable = var_pipette_axis)
select_pipette_scale.grid(column = 1, row = 1)


#----------------Selection 2 - Max Volume---------------------
var_max_volume = tk.IntVar()
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
scale_2 = tk.Scale(tab1, from_=100, to=2000, resolution = 1, orient="horizontal", variable = scale_var2, command = update_var_max_volume1)
scale_2.grid(column = 1, row = 3)

# Entry Box
text_2 = tk.Entry(tab1, width=4, textvariable=entry_var2)
text_2.grid(column=0, row=3, padx=5)
text_2.bind("<Enter>", update_var_max_volume)

label = ttk.Label(tab1, text='uL', font = ('Arial', 12))
label.grid(column = 2, row = 3)

#---------------------Selection 3 - Min Volume-----------------------
var_min_volume = tk.IntVar()
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
scale_3 = tk.Scale(tab1, from_=100, to=2000, resolution = 1, orient="horizontal", variable = scale_var3, command = update_var_min_volume1)
scale_3.grid(column = 1, row = 5)

#Entry Box
text_3 = tk.Entry(tab1, width=4, textvariable=entry_var3)
text_3.grid(column = 0, row = 5, padx=5)
text_3.bind("<Enter>", update_var_min_volume)
#Unit
label = ttk.Label(tab1, text='uL', font = ('Arial', 12))
label.grid(column = 2, row = 3)

#Unit
label = ttk.Label(tab1, text='uL', font = ('Arial', 12))
label.grid(column = 2, row = 5)



#------------------------Selection 3 - aspirate_speed-----------------------
var_aspirate_speed = tk.IntVar()
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
scale_4 = tk.Scale(tab1, from_=100, to=1500, resolution = 1, orient="horizontal", variable = scale_var4, command = update_var_aspirate_speed1)
scale_4.grid(column = 1, row = 7)

#Sync Entry Box
text_4 = tk.Entry(tab1, width=4, textvariable=entry_var4)
text_4.grid(column = 0, row = 7, padx=5)
text_4.bind("<Enter>", update_var_aspirate_speed)
#Unit
label = ttk.Label(tab1, text='mm/min', font = ('Arial', 12))
label.grid(column = 2, row = 7)

# Separator object
separator = ttk.Separator(tab1, orient='vertical')
separator.grid(row=0,column=4, rowspan=10, ipady=180)

#----------------------Selection 4 - dispense_speed-----------------------
var_dispense_speed = tk.IntVar()
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
scale_5 = tk.Scale(tab1, from_=100, to=1500, resolution = 1, orient="horizontal", variable = scale_var5, command = update_var_dispense_speed1)
scale_5.grid(column = 1, row = 9)

#Sync Entry Box
text_5 = tk.Entry(tab1, width=4, textvariable=entry_var5)
text_5.grid(column = 0, row = 9, padx=5)
text_5.bind("<Enter>", update_var_dispense_speed)
#Unit
label = ttk.Label(tab1, text='mm/min', font = ('Arial', 12))
label.grid(column = 2, row = 9)

root.mainloop()

print(var_max_volume.get(), var_dispense_speed.get(), var_aspirate_speed.get(), var_dispense_speed.get())
