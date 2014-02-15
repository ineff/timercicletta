#! /usr/bin/python

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

import time

from timers.timer import Timer

from windows.windows import ClockWindow, AlarmWindow

# def setTimeLabel(label): # Function which set a label to the current time
#    label.set_text(time.strftime('%H:%M:%S')) # Set the label to the current time
#    return True

# class TimerWindow(Gtk.Window):
    
#    def __init__(self):

#       Gtk.Window.__init__(self,title='Timer') # Call the Gtk.Window constructor setting title of the window
#       hbox = Gtk.Box(spacing=6) # Create a container in which put the timer 
#       label = Gtk.Label('') # Create a label which will hold the current time

#       GLib.timeout_add_seconds(1,setTimeLabel,label) # Set the clock:

#       # To Do: Fare il coso per l'allarme

#       self.label = label # Add a reference to the label in the object
#       self.hbox = hbox # Add a reference to the box in the object
#       hbox.pack_start(label, True, True, 0) # Put the label inside the container hbox


#       self.add(hbox) # Put the box inside the window

# #      self.alarm = AlarmWindow() # To be fixed
# #      self.alarm.show_all()

# class AlarmWindow(Gtk.Window):

#    def __init__(self):

#       Gtk.Window.__init__(self,title='Alarm')
#       hbox = Gtk.Box(spacing=6)
#       label = Gtk.Label('- 00:05:00')

#       label.countdown = Timer(hour=0,min=5,sec=0) # Add to the label a countdown

#       self.hbox = hbox
#       self.label = label

# #      label.set_name('AlarmLabel')

#       hbox.pack_start(label, True, True, 0)

#       GLib.timeout_add_seconds(1,updateCountdown,self)
#       self.set_name('Alarm')
#       self.add(hbox)


# def updateCountdown(window):

#    flashTime = Timer(min=4,sec=30) # Time when start to flashing
#    finish = Timer() # Time is end

#    window.label.countdown.dec() # Decrement the countdown
#    window.label.set_text('- '+str(window.label.countdown))
#    if window.label.countdown < flashTime:# If we are up to 1 minute to the alarm
#       if window.label.get_visible(): # we toggle visible status of the label
#          window.label.hide()
#       else:
#          window.label.show()
#    if window.label.countdown == finish: # if countdown is zero, we stop cycling
#       window.destroy()
#       return False
#    else:
#       return True # Otherwise we countinue to cycle

# def alarmCreator(): # This callback has the only aim to set the alarms to give hours.

   # Idea da implementare ancora
   # alarmCreator dovrebbe prendere la lista dei programmi in onda oggi e verificare l'orario:
   # se quando giunge l'orario meno 5 minuti crea una alarmWindow ... to be continued

window = ClockWindow() # Create the window
window.connect('delete-event', Gtk.main_quit) # Connect the termination function to the event of deletion of the window
window.show_all() # Make visible the window and every element it contains

# For creating the alarm we let run in the background a routine that creates the alarm
# at a given time
#GLib.timeout_add_secs(60,alarmCreator) # run every minute the callback


provider = Gtk.CssProvider() # This object will serve to load the appearance property
display = Gdk.Display.get_default() 
screen = display.get_default_screen()

provider.load_from_data(b"""
#Alarm {
background-color: black;
color: white;
}
#AlarmLabel{
font-size: 100;
}
""")

# Next we tell the screen to use the appearance described in the provider
Gtk.StyleContext.add_provider_for_screen(screen,provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

Gtk.main() # Start the Gtk loop engine

timant = Timer()
