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
      hbox = Gtk.Box(spacing=6) # Create a container in which put the timer 
      label = Gtk.Label('') # Create a label which will hold the current time

      self.schedule = {'lu':[],'ma':[],'me':[],'gi':[],'ve':[],'sa':[],'do':[]} 
      # schedule is a dictionary containing for every day a field which contain 
      # the list of start time of programs
      # for the day

      self.label = label # Add a reference to the label in the object
      self.hbox = hbox # Add a reference to the box in the object
      hbox.pack_start(label, True, True, 0) # Put the label inside the container hbox


      self.add(hbox) # Put the box inside the window

      self.alarm = AlarmWindow() # Create the alarm window
      # self.alarm.reset()
      # self.alarm.start()

      self.updateSchedule()

      GLib.timeout_add_seconds(1,setTimeLabel,self) # Set the clock
      GLib.timeout_add_seconds(60*60*24,self.updateSchedule,self) # Every day update the schedule


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
      

class AlarmWindow(Gtk.Window):

   def __init__(self):

      Gtk.Window.__init__(self,title='Alarm')

#      self.__state__ = False # A boolean stating if the alarm is active

      hbox = Gtk.Box(spacing=6)
      label = Gtk.Label('')

      countdown = Timer(hour=0,min=5,sec=0) # Add to the label a countdown

      self.hbox = hbox
      self.label = label
      self.countdown = countdown

      hbox.pack_start(label, True, True, 0)

      self.set_name('Alarm')
      self.add(hbox)

   def reset(self): # Reset the counter
      self.label.countdown = Timer(hour=0,min=5,sec=0)

   def start(self): # Start countdown
      
      if self.countdown == Timer(): # If the countdown is on zero we do nothing
         return False 
      # Otherwise ...
      self.show_all()
#      self.__state__ = True 
      GLib.timeout_add_seconds(1,updateCountdown,self)      
      return True

# Here are some auxiliary functions used to update the windows.

def setTimeLabel(window): # Function which set a label to the current time

   day = ['lu','ma','me','gi','ve','sa','do']
   window.label.set_text(time.strftime('%H:%M:%S')) # Set the label to the current time
   # Next we control if in five minutes start a new program.
   now = time.localtime()
   today = now.tm_wday
   hour = now.tm_hour
   minutes = now.tm_min

   timeNow = Timer(hour=hour,min=minutes)

   print(timeNow)
   print(window.schedule[day[today]])

   for index in range(0,5):
      timeNow.incMin()

   print(timeNow)

   if timeNow in window.schedule[day[today]] and not window.alarm.get_property('visible'):
      window.alarm.reset() # Reset the countdown of the window
      window.alarm.start() # start the countdown
      print('It worked!')
   return True


def updateCountdown(window):

   flashTime = Timer(min=1,sec=0) # Time when start to flashing
   finish = Timer() # Time is end

   window.countdown.dec() # Decrement the countdown
   window.label.set_text('- '+str(window.countdown))
   if window.countdown < flashTime:# If we are up to 1 minute to the alarm
      if window.label.get_visible(): # we toggle visible status of the label
         window.label.hide()
      else:
         window.label.show()
   if window.countdown == finish: # if countdown is zero, we stop cycling
      window.hide()               # and make the window disappear
#      window.__state__ = False    # put alarm in stopped mode
      return False
   else:
      return True # Otherwise we countinue to cycle
