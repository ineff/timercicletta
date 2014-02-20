# This module provide the classes for the clock-window
# and the window for the alarm.

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

from json import JSONDecoder
from urllib2 import urlopen

import time

from timers.timer import Timer,fromArr2Time

# Here follow the definitions of the classes for the two windows

class ClockWindow(Gtk.Window):
    
   def __init__(self):

      Gtk.Window.__init__(self,title='Timer') # Call the Gtk.Window constructor 

      self.hbox = Gtk.Box(spacing=6) # Create a container in which put the timer 
      self.label = Gtk.Label('') # Create a label which will hold the current time
      self.schedule = {'lu':[],'ma':[],'me':[],'gi':[],'ve':[],'sa':[],'do':[]} 
      # schedule is a dictionary containing for every day a field which contain 
      # the list of start time of programs
      # for the day

      self.hbox.pack_start(self.label, True, True, 0) # Put the label inside the container hbox

      self.add(self.hbox) # Put the box inside the window

      self.alarm = AlarmWindow() # Create the alarm window
      # self.alarm.reset()
      # self.alarm.start()

      self.updateSchedule()

      self.connect('delete-event', Gtk.main_quit) # Connect the termination function to the event 
                                                  # of deletion of the window
      self.show_all() # Make visible the window and every element it contains


      GLib.timeout_add_seconds(1,self.setTimeLabel) # Set the clock
      GLib.timeout_add_seconds(60*60*24,self.updateSchedule) # Every day update the schedule


   def updateSchedule(self): # This function will update the schedule
      
      days = ['lu','ma','me','gi','ve','sa','do'] 
      dec = JSONDecoder(encoding='ascii') 
      rawdata = urlopen('http://www.radiocicletta.it:80/programmi.json').read() # We retrive the json in str type
      # Now we extract from string rawdata the list of programs active (stato == 1)
      listaProgs = filter(lambda x: x['stato'] == '1',dec.decode(rawdata)['programmi']) 
      # Finally insert in the dictionary schedule the list of start time of the programs
      for today in days:
         self.schedule[today] = map(lambda x: fromArr2Time(x['start'][1:3]),
                                    filter(lambda x: x['start'][0] == today, listaProgs)) 
      
      return True

   def setTimeLabel(self):

      day = ['lu','ma','me','gi','ve','sa','do']
      self.label.set_text(time.strftime('%H:%M:%S')) # Set the label to the current time
      # Next we control if in five minutes start a new program.
      now = time.localtime()
      today = now.tm_wday
      hour = now.tm_hour
      minutes = now.tm_min
      
      timeNow = Timer(hour=hour,min=minutes)
      
      for index in range(0,5):
         timeNow.incMin()

      if timeNow in self.schedule[day[today]] and not self.alarm.get_property('visible'):
         self.alarm.reset() # Reset the countdown of the self
         self.alarm.start() # start the countdown
      
      return True
      
      

class AlarmWindow(Gtk.Window):

   def __init__(self):

      Gtk.Window.__init__(self,title='Alarm')
      self.hbox = Gtk.Box(spacing=6)
      self.label = Gtk.Label('')
      self.countdown = Timer(hour=0,min=5,sec=0) # Add to the label a countdown

      self.hbox.pack_start(self.label, True, True, 0)
      self.set_name('Alarm')
      self.add(self.hbox)

   def reset(self): # Reset the counter
      self.countdown = Timer(hour=0,min=5,sec=0)

   def start(self): # Start countdown
      
      if self.countdown == Timer(): # If the countdown is on zero we do nothing
         return False 
      # Otherwise ...
      self.show_all()
      GLib.timeout_add_seconds(1,self.updateCountdown)      
      return True

   def updateCountdown(self):

      flashTime = Timer(min=1,sec=0) # Time when start to flashing
      finish = Timer() # Time is end
      
      self.countdown.dec() # Decrement the countdown
      self.label.set_text('- '+str(self.countdown))
      if self.countdown < flashTime:# If we are up to 1 minute to the alarm
         if self.label.get_visible(): # we toggle visible status of the label
            self.label.hide()
         else:
            self.label.show()
      if self.countdown == finish: # if countdown is zero, we stop cycling
         self.hide()               # make the self disappear
         return False # and stop the countdown
   
      return True # Otherwise we countinue to cycle




