import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from Xlib.display import Display
from Xlib import X

class Banner:

    def __init__(self, fgcolor, bgcolor, font, size, font_weight, banner_height, vertical_offset=0, message=""):
        self.vertical_offset = vertical_offset
        self.bgcolor = bgcolor
        self.font = font
        self.font_weight = font_weight
        self.fgcolor = fgcolor
        self.size = size
        self.message = message
        self.banner_height = banner_height

        self.initialize_window()
        self.apply_styles()
        self.add_label()
        self.initialize_display()

    def initialize_window(self):
        self.window = Gtk.Window()
        self.window.set_name("bar")
        self.window.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.window.stick()
        self.window.connect("delete-event", Gtk.main_quit)

    def apply_styles(self):
        style_provider = Gtk.CssProvider()
        css_data = b"""
        #bar {
            background-color: %s;
        }
        """ % self.bgcolor.encode('utf-8')
        style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Display.get_default().get_default_screen(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def add_label(self):
        center_label = Gtk.Label()
        center_label.set_markup(
            "<span font_family='%s' font_weight='%s' foreground='%s' size='%s'>%s</span>" % (
                self.font, self.font_weight, self.fgcolor, self.size, self.message))
        center_label.set_justify(Gtk.Justification.CENTER)
        center_label.set_yalign(0.5)
        center_label.set_xalign(0.5)
        center_label.set_hexpand(True)
        center_label.set_vexpand(True)
        self.window.add(center_label)
        self.window.show_all()

    def initialize_display(self):
        self.display = Display()
        self.topw = self.display.create_resource_object('window',
                                                        self.window.get_toplevel().get_window().get_xid())
        self.auto_resize()

    def auto_resize(self, event=None):
        monitor = Gdk.Display.get_default().get_primary_monitor()
        geometry = monitor.get_geometry()

        x = geometry.x
        y = geometry.y
        width = geometry.width

        # Adjust y position to be below the status bar only for the primary monitor
        y += self.vertical_offset

        # Move and resize the window
        self.window.move(x, y)
        self.window.resize(width, self.banner_height)

        # Reserve space (a "strut") for the bar
        strut_top = self.banner_height + self.vertical_offset
        self.topw.change_property(self.display.intern_atom('_NET_WM_STRUT'),
                                  self.display.intern_atom('CARDINAL'), 32,
                                  [0, 0, strut_top, 0],
                                  X.PropModeReplace)
        self.topw.change_property(self.display.intern_atom('_NET_WM_STRUT_PARTIAL'),
                                  self.display.intern_atom('CARDINAL'), 32,
                                  [0, 0, strut_top, 0, 0, 0, 0, 0, x, x + width - 1, 0, 0],
                                  X.PropModeReplace)

class MultiWindowBanner(Banner):
    GNOME_MAIN_BAR_HEIGHT = 26

    def __init__(self, fgcolor, bgcolor, font, size, font_weight, banner_height, all_monitor_voffset=0, message=""):
        self.all_monitor_voffset = all_monitor_voffset
        super().__init__(fgcolor, bgcolor, font, size, font_weight, banner_height, message)
        self.banners = []
        self.create_banners()

    def create_banners(self):
        display = Gdk.Display.get_default()
        num_monitors = display.get_n_monitors()

        for i in range(num_monitors):
            monitor = display.get_monitor(i)
            is_primary = display.get_primary_monitor() == monitor
            voffset = self.all_monitor_voffset + (self.GNOME_MAIN_BAR_HEIGHT if is_primary else 0)
            banner = Banner(self.fgcolor, self.bgcolor, self.font, self.size, self.font_weight, self.banner_height, voffset, self.message)
            self.banners.append(banner)
