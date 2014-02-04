#! /usr/bin/python3

from gi.repository import Gtk
from gi.repository import GLib

import time

def fromTime2Str(num):   # Auxiliary function to transform integer in secons/minutes/hours
   sTime = ''
   if num < 10:
      sTime = '0'+str(num)
   else:
      sTime = str(num)
   return sTime

def setTimeLabel(label): # Function which set a label to the current time
   now = time.localtime() 
   listTime = [now.tm_hour,now.tm_min,now.tm_sec] # Extract from now a list of form [hours,minutes,seconds]

   timeLabel = ':'.join(map(fromTime2Str,listTime)) # Turn the integer list into a string list and concatenate using ':'
                                                    # as separator
   label.set_text(timeLabel) # Set the label to the current time
   return True

class TimerWindow(Gtk.Window):
    
   def __init__(self):

      Gtk.Window.__init__(self,title='Timer') # Call the Gtk.Window constructor setting title of the window
      hbox = Gtk.Box(spacing=6) # Create a container in which put the timer 
      label = Gtk.Label('') # Create a label which will hold the current time

      GLib.timeout_add_seconds(1,setTimeLabel,label) # Set the clock:
                                                     # timeout_add_seconds call the function setTimeLabel 
                                                     # 1 seconds until the function return False (which means always)
                                                     # and passes to the function the argument label

      # To Do: Fare il coso per l'allarme

      self.label = label # Add a reference to the label in the object
      self.hbox = hbox # Add a reference to the box in the object
      hbox.pack_start(label, True, True, 0) # Put the label inside the container hbox

      self.add(hbox) # Put the box inside the window

window = TimerWindow() # Create the window
window.connect('delete-event', Gtk.main_quit) # Connect the termination function to the event of deletion of the window
window.show_all() # Make visible the window and every element it contains
Gtk.main() # Start the Gtk loop engine

