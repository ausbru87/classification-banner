from gi.repository import Gtk
from banner import Banner

def main():
    message = "Hello, World!"
    fgcolor = "#FFFFFF"
    bgcolor = "#007A33"
    font = "Sans"
    size = "large"
    weight = "bold"
    bar_size = 24

    banner = Banner(message, fgcolor, bgcolor, font, size, weight, bar_size)
    Gtk.main()

if __name__ == "__main__":
    main()