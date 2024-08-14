import gi
import argparse
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from usg_classification_banner import USGClassificationBanner



def main(classification):

    # Initialize the banner
    banner = USGClassificationBanner(classification)

    # Connect to the screen events
    screen = Gdk.Screen.get_default()
    screen.connect("monitors-changed", banner.resize_banners)
    screen.connect("size-changed", banner.resize_banners)

    # Run the Gtk main loop
    Gtk.main()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GNOME Desktop Banner")
    parser.add_argument("classification", type=str, help="The classification level for the banner")
    args = parser.parse_args()

    main(args.classification)