import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from Banner import Banner, USGClassificationBanner



def main():
    # Initialize the banner values
    classification = "U_FOUO"
    bar_size = 24
    vertical_offset = 26 # Offset from the top of the screen for GNOME main bar

    # Initialize the banner
    banner = USGClassificationBanner(classification, bar_size, vertical_offset)

    # Connect to the screen events
    screen = Gdk.Screen.get_default()
    screen.connect("monitors-changed", banner.auto_resize)
    screen.connect("size-changed", banner.auto_resize)

    # Run the Gtk main loop
    Gtk.main()

if __name__ == "__main__":
    main()