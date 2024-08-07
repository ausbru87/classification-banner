import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from Banner import Banner

def main():
    # Initialize the banner values
    message = "UNCLASSIFIED // FOR OFFICIAL USE ONLY"
    fgcolor = "#FFFFFF"
    bgcolor = "#007A33"
    font = "liberation-sans"
    size = "large"
    weight = "bold"
    bar_size = 24

    # Initialize the banner
    banner = Banner(message, fgcolor, bgcolor, font, size, weight, bar_size)

    # Connect to the screen events
    screen = Gdk.Screen.get_default()
    screen.connect("monitors-changed", banner.auto_resize)
    screen.connect("size-changed", banner.auto_resize)

    # Run the Gtk main loop
    Gtk.main()

if __name__ == "__main__":
    main()