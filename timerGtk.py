#! /usr/bin/python

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

import time

from timers.timer import Timer

from windows.windows import ClockWindow, AlarmWindow

# def alarmCreator(): # This callback has the only aim to set the alarms to give hours.

   # Idea da implementare ancora
   # alarmCreator dovrebbe prendere la lista dei programmi in onda oggi e verificare l'orario:
   # se quando giunge l'orario meno 5 minuti crea una alarmWindow ... to be continued

window = ClockWindow() # Create the window

provider = Gtk.CssProvider() # This object will serve to load the appearance property
display = Gdk.Display.get_default() 
screen = display.get_default_screen()

provider.load_from_data(b"""
GtkLabel {
font-size: 60;
padding: 0.5em;
}

#AlarmWindow {
background-color: black;
color: white;
}

#Alarm {
background-color: black;
color: white;
}
""")

# Next we tell the screen to use the appearance described in the provider
Gtk.StyleContext.add_provider_for_screen(screen,provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

Gtk.main() # Start the Gtk loop engine

