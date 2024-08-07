import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from Xlib.display import Display
from Xlib import X

def on_size_allocate(window, allocation, data):
    # Adjust the window properties when resized or moved
    display = Display()
    topw = display.create_resource_object('window',
                                          window.get_toplevel().get_window().get_xid())

    monitor = Gdk.Display.get_default().get_primary_monitor()
    geometry = monitor.get_geometry()

    x = geometry.x
    y = geometry.y
    width = geometry.width
    height = geometry.height

    # Adjust y position to be below the status bar only for the primary monitor
    status_bar_height = 24  # Adjust this value as needed
    y += status_bar_height

    # Move and resize the window
    window.move(x, y)
    window.resize(width, data['bar_size'])

    # Reserve space (a "strut") for the bar
    strut_top = data['bar_size'] + status_bar_height
    topw.change_property(display.intern_atom('_NET_WM_STRUT'),
                         display.intern_atom('CARDINAL'), 32,
                         [0, 0, strut_top, 0],
                         X.PropModeReplace)
    topw.change_property(display.intern_atom('_NET_WM_STRUT_PARTIAL'),
                         display.intern_atom('CARDINAL'), 32,
                         [0, 0, strut_top, 0, 0, 0, 0, 0, x, x + width - 1, 0, 0],
                         X.PropModeReplace)

def main():
    print("Gtk %d.%d.%d" % (Gtk.get_major_version(),
                            Gtk.get_minor_version(),
                            Gtk.get_micro_version()))

    message = "UNCLASSIFIED // FOUO"
    fgcolor = "#FFFFFF"
    bgcolor = "#007A33"
    font = "liberation-sans"
    size = "large"
    weight = "bold"
    bar_size = 30  # Height of the bar

    # (a) Create an undecorated dock
    window = Gtk.Window()
    window.set_name("bar")
    window.set_type_hint(Gdk.WindowTypeHint.DOCK)
    window.set_decorated(False)
    window.set_keep_above(True)  # Keep the window always on top
    window.stick()  # Make the window visible on all workspaces

    # Style the window
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(f"""
    #bar {{
        background-color: {bgcolor};
    }}
    """)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    # Add a label to the center of the bar
    label = Gtk.Label()
    label.set_markup(f"<span font_family='{font}' weight='{weight}' foreground='{fgcolor}' size='{size}'>{message}</span>")
    label.set_justify(Gtk.Justification.CENTER)
    label.set_yalign(0.5)
    label.set_xalign(0.5)
    label.set_hexpand(True)
    label.set_vexpand(True)
    window.add(label)
    window.show_all()

    # Connect the size allocate signal
    window.connect("size-allocate", on_size_allocate, {'bar_size': bar_size})

    Gtk.main()

if __name__ == "__main__":
    main()