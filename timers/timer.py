# A module exporting a class that implement a Timer 
# and some auxiliary functions

def fromTime2Str(num):   # Auxiliary function to transform integer in secons/minutes/hours

   sTime = ''
   if num < 10:
      sTime = '0'+str(num)
   else:
      sTime = str(num)
   return sTime

def fromArr2Time(arr): # Auxliary function that takes an array of two integer and return a Timer

   if (len(arr) != 2):
      return Timer()
   else:
      return Timer(hour=arr[0], min=arr[1])   
   

# The class for Timer

class Timer(object):

   def __init__(self,hour=0,min=0,sec=0):

       self.hour = hour
       self.min  = min
       self.sec  = sec

       return

   def __repr__(self):

       return "hour = %d, min = %d, sec = %d" % (self.hour,self.min,self.sec)

   def __str__(self):

       return ':'.join(map(fromTime2Str,[self.hour,self.min,self.sec]))

   def __cmp__(self,other): # Methods for comparing times

       if self.hour > other.hour: # if self's hour are greater than other's then self > other
           return 1
       if self.hour == other.hour:# if self and other have same hour 
           if self.min > other.min: # and self's min > other's min than self > other
               return 1
           if self.min == other.min: # and self and other have the same min
               if self.sec > other.sec: # ... well you got it, don't you?
                   return 1
               if self.sec == other.sec:
                   return 0
       # If any of the above if fails then other > self
       return -1

   def __lt__(self,other): # We define explicitly these methods too for compatibility with python3
      if self.hour < other.hour:
         return True
      if self.hour == other.hour and self.min < other.min:
         return True
      if self.hour == other.hour and self.min == self.min and self.sec < other.sec:
         return True
      return False

   def __eq__(self,other):
      return self.hour == other.hour and self.min == other.min and self.sec == other.sec
   
   def __gt__(self,other):
      return (not (self == other)) and not (self < other)

   def __ge__(self,other):
      return self > other or self == other

   def __le__(self,other):
      return self < other or self == other

   def inc(self): # method to increment the countdown
       if self.sec < 59: # If we can increment seconds we increment
           self.sec = self.sec +1
           return 
       self.sec = 0 # otherwise we restart seconds and increment minutes
       if self.min < 59: # if we can increment minute we do so
           self.min = self.min + 1 
           return
       self.min = 0 # otherwise we restart minutes and increments hours
       self.hour = self.hour + 1
       return 

   def dec(self): # method to decrement the countdown
       if self.sec == 0:
           if self.min == 0:
               if self.hour == 0:
                   return # If the countdown is set to 00:00:00 it cannot be decremented
               else:
                   self.hour = self.hour - 1
                   self.min = 59
                   self.sec = 59
           else: 
               self.min = self.min - 1
               self.sec = 59
       else:
           self.sec = self.sec - 1
       return


