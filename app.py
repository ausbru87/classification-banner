import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Banner import Banner

def main():
    message = "UNCLASSIFIED // FOR OFFICIAL USE ONLY"
    fgcolor = "#FFFFFF"
    bgcolor = "#007A33"
    font = "liberation-sans"
    size = "large"
    weight = "bold"
    bar_size = 24

    banner = Banner(message, fgcolor, bgcolor, font, size, weight, bar_size)
    Gtk.main()

if __name__ == "__main__":
    main()