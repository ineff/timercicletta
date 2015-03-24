#! /usr/bin/python

from gi.repository import GLib, Gdk, Gtk # Library for using gtk+ window system
import cairo # Needed to draw in gtk
import time # Needed to operate with deltas

# The list of the colors
colors = {
    "red": Gdk.RGBA (red = 1.0, green = 0.0, blue = 0.0, alpha = 1.0),
    "yellow": Gdk.RGBA (red = 1, green = 1, blue = 0.25, alpha = 1.0),
    "green": Gdk.RGBA (red = 0.0, green = 1.0, blue = 0.0, alpha = 1.0)
}

def get_timer():
    # The function that generates the text
    # to put in the 'timer'
    return "-13:00:00"
    
    
class TimerWindow(Gtk.Window):
# The class for the timer window
    def __init__(self):
        # Constructor 
        Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL)
        self.set_title("Clock window")
        self.__frame__ = Gtk.Frame()
        self.__drawing_area__ =  Gtk.DrawingArea()
        self.__frame__.add(self.__drawing_area__)
        self.add(self.__frame__)
        self.connect("destroy", Gtk.main_quit)
        self.__drawing_area__.connect("draw", self.draw_callback)
        self.__color__ = colors["yellow"]
        GLib.timeout_add(250, self.drawing)
        self.show_all()

    def drawing (widget):
        # Loop function called to make redraw the window
        widget.__drawing_area__.queue_draw()
        return True # continue to loop

    def draw_callback (self, da, cr):
        # The callback used by gtk for drawing the window
        height = da.get_allocated_height() # we get dimensine 
        width = da.get_allocated_width() # of the drawing area
        [red, green, blue, alpha] = self.get_color() # get the color to use
        cr.set_source_rgba(red, green, blue, alpha) 
        cr.rectangle(0, 0, width, height) 
        cr.fill() # and color the window
        cr.set_source_rgba(1, 1, 1, 1) # hence we add the timer
        cr.set_font_size(min(height, width)/10.0) 
        timer = get_timer()
        text_width = (cr.text_extents(timer))[4]
        cr.move_to(width*0.5 - text_width/2, height*0.5) # we put the timer in the center of the window
        cr.show_text(timer) # aaaaaaaaand we print the timer
        return True

    def get_color(self):
        # This method get a 4-tuple for the color from the
        # RGBA object containing the color
        red = self.__color__.red 
        blue = self.__color__.blue
        green = self.__color__.green
        alpha = self.__color__.alpha
        return [red, green, blue, alpha]

    def set_color(self, choice):
        # Set color to a given choice
        self.__color__ = colors[choice] 


Gtk.init()
clock = TimerWindow()

Gtk.main()

