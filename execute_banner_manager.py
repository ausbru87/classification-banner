import sys
import argparse
import gi
from banner_manager import BannerManager

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

def main(config_file):
    # Initialize GTK
    # Gtk.init(sys.argv)

    # # Get screen and display information
    # display = Gdk.Display.get_default()
    # screen = display.get_default_screen()

    # Initialize BannerManager
    BannerManager(config_file)

    # Print banner details for verification

    # Run the Gtk main loop
    Gtk.main()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute Banner Manager with a configuration file.')
    parser.add_argument('config_file', type=str, help='Path to the banner configuration file')
    args = parser.parse_args()

    main(args.config_file)