# This module provide the classes for the clock-window
# and the window for the alarm.

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

import time

from timers.timer import Timer

# Here follow the definitions of the classes for the two windows

class ClockWindow(Gtk.Window):
    
   def __init__(self):

      Gtk.Window.__init__(self,title='Timer') # Call the Gtk.Window constructor setting title of the window
      hbox = Gtk.Box(spacing=6) # Create a container in which put the timer 
      label = Gtk.Label('') # Create a label which will hold the current time

      GLib.timeout_add_seconds(1,setTimeLabel,label) # Set the clock:

      self.label = label # Add a reference to the label in the object
      self.hbox = hbox # Add a reference to the box in the object
      hbox.pack_start(label, True, True, 0) # Put the label inside the container hbox


      self.add(hbox) # Put the box inside the window

      self.alarm = AlarmWindow() # To be fixed
      self.alarm.show_all()

class AlarmWindow(Gtk.Window):

   def __init__(self):

      Gtk.Window.__init__(self,title='Alarm')
      hbox = Gtk.Box(spacing=6)
      label = Gtk.Label('- 00:05:00')

      label.countdown = Timer(hour=0,min=5,sec=0) # Add to the label a countdown

      self.hbox = hbox
      self.label = label

      hbox.pack_start(label, True, True, 0)

      GLib.timeout_add_seconds(1,updateCountdown,self)
      self.set_name('Alarm')
      self.add(hbox)


# Here are some auxiliary functions used to update the windows.

def setTimeLabel(label): # Function which set a label to the current time
   label.set_text(time.strftime('%H:%M:%S')) # Set the label to the current time
   return True


def updateCountdown(window):

   flashTime = Timer(min=4,sec=30) # Time when start to flashing
   finish = Timer() # Time is end

   window.label.countdown.dec() # Decrement the countdown
   window.label.set_text('- '+str(window.label.countdown))
   if window.label.countdown < flashTime:# If we are up to 1 minute to the alarm
      if window.label.get_visible(): # we toggle visible status of the label
         window.label.hide()
      else:
         window.label.show()
   if window.label.countdown == finish: # if countdown is zero, we stop cycling
      window.destroy()
      return False
   else:
      return True # Otherwise we countinue to cycle
