import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from Xlib.display import Display
from Xlib import X

def on_configure_event(window, event, data):
    # Adjust the window properties when resized or moved
    screen = window.get_screen()
    monitors = []
    nmons = screen.get_n_monitors()
    for m in range(nmons):
        mg = screen.get_monitor_geometry(m)
        monitors.append(mg)

    display = Display()
    topw = display.create_resource_object('window',
                                          window.get_toplevel().get_window().get_xid())

    main_monitor = screen.get_primary_monitor()

    for i, monitor in enumerate(monitors):
        x = monitor.x
        y = monitor.y
        width = monitor.width
        height = monitor.height

        # Adjust y position to be below the status bar only for the main monitor
        status_bar_height = 24  # Adjust this value as needed
        if i == main_monitor:
            y += status_bar_height

        # Move and resize the window
        window.move(x, y)
        window.resize(width, data['bar_size'])

        # Reserve space (a "strut") for the bar
        strut_top = data['bar_size'] + (status_bar_height if i == main_monitor else 0)
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
    window.connect("delete-event", Gtk.main_quit)

    # (b) Style it
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(b"""
    #bar {
        background-color: #007A33;
    }
    """)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # (b) Add a label to the center of the bar
    center_label = Gtk.Label(
        "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" % (
            font, weight, fgcolor, size, message))
    center_label.set_use_markup(True)
    center_label.set_justify(Gtk.Justification.CENTER)
    center_label.set_yalign(0.5)
    center_label.set_xalign(0.5)
    center_label.set_hexpand(True)
    center_label.set_vexpand(True)
    window.add(center_label)
    window.show_all()

    # Connect to the configure-event signal
    window.connect("configure-event", on_configure_event, {'bar_size': bar_size})

    Gtk.main()

if __name__ == "__main__":
    main()