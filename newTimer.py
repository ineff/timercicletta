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

col = ["red","yellow","green"]

# The function that generates the text
# to put in the 'timer'
def get_timer():
    return time.strftime('%H:%M:%S')
    
# The class for the timer window    
class TimerWindow(Gtk.Window):

    # Constructor 
    def __init__(self):
        Gtk.Window.__init__(self, Gtk.WindowType.TOPLEVEL)
        self.set_title("Clock window")
        self.__frame__ = Gtk.Frame() # a gtk frame
        self.__drawing_area__ =  Gtk.DrawingArea() # The gtk object were we are going to draw
        self.__frame__.add(self.__drawing_area__) # we add the drawing area to the frame
        self.add(self.__frame__) # and the frame to the window
        self.connect("destroy", Gtk.main_quit) # when the window recieve a destroy event close the application
        self.__drawing_area__.connect("draw", self.draw_callback) # we set the callback for drawing the d.a.
        self.__color__ = colors["yellow"] # set a color for the d.a.
        self.index = 0
        GLib.timeout_add(1000, self.drawing) # set a counter that every 250 sec (almost) force redrawing
        self.show_all()

    def drawing(self):
        self.__drawing_area__.queue_draw()
        return True

    # The callback used by gtk for drawing the window
    def draw_callback (self, da, cr):
        # we get dimension 
        height = da.get_allocated_height() 
        width = da.get_allocated_width() 
        cr.rectangle(0, 0, width, height) 
        # get the color to use
        [red, green, blue, alpha] = self.get_color() 
        cr.set_source_rgba(red, green, blue, alpha) 
        # draw the window
        cr.fill() 
        # we add the timer
        timer = get_timer()
        cr.set_source_rgba(1, 1, 1, 1) 
        cr.set_font_size(min(height, width)/10.0) 
        text_width = (cr.text_extents(timer))[4]
        cr.move_to(width*0.5 - text_width/2, height*0.5) # we put the timer in the center of the window
        # aaaaaaaaand we print the timer
        cr.show_text(timer) 
        return True
                                              
    # This method get a 4-tuple for the color from the
    # RGBA object containing the color
    def get_color(self):
        self.index = (self.index + 1) % 3
        index = self.index
        red = colors[col[index]].red
        blue = colors[col[index]].blue
        green = colors[col[index]].green
        alpha = colors[col[index]].alpha
        # red = self.__color__.red 
        # blue = self.__color__.blue
        # green = self.__color__.green
        # alpha = self.__color__.alpha
        return [red, green, blue, alpha]

    # Set color to a given choice
    def set_color(self, choice):
        self.__color__ = colors[choice] 


Gtk.init()
clock = TimerWindow()

Gtk.main()

