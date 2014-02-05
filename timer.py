#! /usr/bin/python3

from gi.repository import Gtk
from gi.repository import GLib

import time

import countdown
from countdown import CountDown


def setTimeLabel(label): # Function which set a label to the current time
   label.set_text(time.strftime('%H:%M:%S')) # Set the label to the current time
   return True

class TimerWindow(Gtk.Window):
    
   def __init__(self):

      Gtk.Window.__init__(self,title='Timer') # Call the Gtk.Window constructor setting title of the window
      hbox = Gtk.Box(spacing=6) # Create a container in which put the timer 
      label = Gtk.Label('') # Create a label which will hold the current time

      GLib.timeout_add_seconds(1,setTimeLabel,label) # Set the clock:

      # To Do: Fare il coso per l'allarme

      self.label = label # Add a reference to the label in the object
      self.hbox = hbox # Add a reference to the box in the object
      hbox.pack_start(label, True, True, 0) # Put the label inside the container hbox

      alarmWindow = AlarmWindow()
      alarmWindow.show_all()

      self.add(hbox) # Put the box inside the window

#      self.alarm = AlarmWindow() # To be fixed
#      self.alarm.show_all()

class AlarmWindow(Gtk.Window):

   def __init__(self):

      Gtk.Window.__init__(self,title='Alarm')
      hbox = Gtk.Box(spacing=6)
      label = Gtk.Label('- 00:05:00')

      label.countdown = CountDown(hour=0,min=5,sec=0) # Add to the label a countdown

      self.hbox = hbox
      self.label = label
      hbox.pack_start(label, True, True, 0)

      GLib.timeout_add_seconds(1,upgradeCountdown,label)

      self.add(hbox)


def upgradeCountdown(label):

   flashTime = CountDown(min=4,sec=30) # Time when start to flashing
   finish = CountDown() # Time is end

   label.countdown.dec() # Decrement the countdown
   label.set_text('- '+str(label.countdown))
   if label.countdown < flashTime:# If we are up to 1 minute to the alarm
      if label.get_visible(): # we toggle visible status of the label
         label.hide()
      else:
         label.show()
   if label.countdown == finish: # if countdown is zero, we stop cycling
      return False
   else:
      return True # Otherwise we countinue to cycle

window = TimerWindow() # Create the window
window.connect('delete-event', Gtk.main_quit) # Connect the termination function to the event of deletion of the window
window.show_all() # Make visible the window and every element it contains
Gtk.main() # Start the Gtk loop engine

