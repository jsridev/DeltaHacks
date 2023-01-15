'''
------------- PLAN MY BUS ROUTE APP ------------- 

Preliminary ideation and conceptulization of a mobile application to assist users in commuting using buses.
This graphical user interface (GUI) includes various widgets and an interactive, scalable map of the bus stops.
The code is developed using Python and Python's standard built-in GUI framework - Tkinter.
Additionally, the tile based interactive map render widget for the Python Tkinter library created by Tom Schimansky was used.
*** Note: the code was developed using Python GUI Tkinter which is only for desktop application,
                further development would be needed to create a moblie application

Grace Burns, Alexandra Levert, Lauren McCrae, Janani Sridev
DeltaHacks Janurary 13-15, 2023
'''


''' CREATING THE MAP '''

from tkinter import *
import tkintermapview
import time
import math
import geocoder


''' MAIN FUNCTION '''
def main():
    '''
    enter stop
    enter distance of notification
    stop to coordinate
    map
    loop on timer?
        get current location
        distance from stop
        check for alarm 1
            if met, check for alarm 2
                once met, break
    '''


    
    
    stop = Enter_Stop()
   
    stop_coords = get_coords(stop) # Convert Stop name to coordinates
    needed_dist = required_distance() # get Distance from stop passenger wants to be notified
    map(get_current_location(),stop_coords ) # Show stop in map

    sleep_time = 0.1 # Time between checking current location

    while (alarm(needed_dist, stop_coords) == 0): # first alarm goes off at user inputed distance
        time.sleep(sleep_time)
    
    needed_dist = 0
    
    while (alarm(needed_dist, stop_coords) == 0): # second alarm goes off at stop
        time.sleep(sleep_time)
    Arrive_Stop() # display success window
      
  


''' WHICH STOP? - widget '''

# Function that allows user to choose stop from drop down menu
def Enter_Stop():
    root1 = Tk()
    root1.title("List of Bus Stops")
    # Add a grid
    mainframe = Frame(root1)
    mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)
    mainframe.pack(pady = 100, padx = 100)
    # Create a Tkinter variable
    tkvar = StringVar(root1)
    # Dictionary with options
    stop_choice = { 'Main@Paisley','Main@Dalewood','Main@Bowman','Main@Norfolk'}
    tkvar.set('Pick a Stop') # set the default option
    popupMenu = OptionMenu(mainframe, tkvar, *stop_choice)
    Label(mainframe, text="Choose a Bus Stop").grid(row = 1, column = 1)
    popupMenu.grid(row = 2, column =1)
    # on change dropdown value
    def change_dropdown(*args):
        global bus_stop
        bus_stop = tkvar.get()
    # link function to change dropdown
    tkvar.trace('w', change_dropdown)
    def close():
        root1.destroy()
    done_button =  Button(root1, text="Done", command=close)
    done_button.pack()
    root1.mainloop()
    return bus_stop




''' CURRENT LOCATION '''
#get location of user
def get_current_location():
    g = geocoder.ip('me')
    return(g.latlng)


''' GET COORDINATES '''
# Get to coordinates of a given stop
def get_coords(stop_name):
    if (stop_name == 'Main@Paisley'):
        coords = [43.25889273505845, -79.9050637225097]
    elif (stop_name == 'Main@Dalewood'):
        coords = [43.25805178362588, -79.91373907234784]
    elif (stop_name == 'Main@Bowman'):
        coords = [43.25810291665473, -79.91670756919602]
    elif (stop_name == 'Main@Norfolk'):
        coords = [43.25773582701893, -79.9233433042064]
    return coords



''' FINDING DISTANCE AWAY FROM STOP '''
# calculates the distance between 2 coordinates 
def FindDistance(list1, list2):
    lat1 = list1[0]*math.pi/180 #calculate radial latitudes and longitudes
    lat2 = list2[0]*math.pi/180
    long1 = list1[1]*math.pi/180
    long2 = list2[1]*math.pi/180
    distance = 6377.8*math.acos((math.sin(lat1)*math.sin(lat2))+(math.cos(lat1)*math.cos(lat2)*math.cos(long2 - long1))) #Haversine formula to convert latitude and longitude to distance
    return distance


''' REQUIRED DISTANCE '''
#User input for distance away from the stop that they would like to be warned at
def required_distance():
    rootreq = Tk()
    rootreq.title('required distance')
    my_label = Label(rootreq,text="How far from the stop would you like to be notified? (m)")
    my_label.pack(pady=20)
    e = Entry(rootreq,width=50,borderwidth=5)
    e.pack()
    def myClick():
        my_label = Label(rootreq,text=e.get())
        global required_distance
        required_distance = e.get()
        required_distance = int(required_distance)
        required_distance = required_distance/1000
        my_label.pack(pady=20)
    enter_button = Button(rootreq,text="Enter", command=myClick)
    enter_button.pack()
    def close():
        rootreq.destroy()
    done_button = Button(rootreq,text="Done", command=close)
    done_button.pack()
    rootreq.mainloop()
    return required_distance



''' MAP '''
# can we make this a bottom window that all other window open on top of?
def map(start, finish):
    root2 = Tk()

    root2.title('Planning Your Bus Trip!')                                                                    # title of map
    my_label = LabelFrame(root2)
    my_label.pack(pady=20)                                                                                    # pady pushes lable down the screen a bit

    map_widget = tkintermapview.TkinterMapView(my_label,width=800,height=600,corner_radius=0)

    map_widget.set_position(43.26215341843237, -79.9055270026129)       # coordinates of westdale
    map_widget.set_zoom(15)                                                                                 # zoom of map

    # bus stop marker location coordinates
    on_stop = map_widget.set_position(start[0], start[1], marker=True, marker_color_circle="light blue", marker_color_outside="blue", text="Get On Here") 
    off_stop = map_widget.set_position(finish[0], finish[1], marker=True, text="Get Off Here")

    map_widget.pack()
    def close():
        root2.destroy()
    done_button =  Button(root2, text="Done", command=close)
    done_button.pack()
    root2.mainloop()



''' ALARM '''
# Displays alarm when user reached specified distance from stop
def alarm(req_dist,coords):
    distance = FindDistance(get_current_location(),coords)
    buffer = 10
    alarm = 0
    if distance<=(req_dist+buffer):
        alarm = 1
        root3 = Tk()
        root3.title('Alarm')
        my_label = Label(root3, text="Alarm is going off")
        my_label.pack(pady=20)
        def close():
            root3.destroy()
        done_button =  Button(root3, text="Turn off alarm", command=close)
        done_button.pack()
        root3.mainloop()
    return alarm


''' FINAL MESSAGE '''
#Displays success window upon arrival
def Arrive_Stop():
    root3 = Tk()
    root3.title('Success')
    my_label = Label(root3, text="You have reached the bus stop!")
    my_label.pack(pady=20)
    def close():
        root3.destroy()
    done_button =  Button(root3, text="Done", command=close)
    done_button.pack()
    root3.mainloop()


 
main()              # calling the main function to run other functions
