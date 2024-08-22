import gi
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk, Gdk, Pango, PangoCairo
from Xlib.display import Display
from Xlib import X

class Banner:
    def __init__(self, fgcolor, bgcolor, font, font_size, font_weight, banner_height, monitor, voffset, message):
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.font = font
        self.font_size = font_size
        self.font_weight = font_weight
        self.banner_height = banner_height
        self.monitor = monitor
        self.voffset = voffset
        self.message = message
        self.window = None
        self.create_banner()

    def create_banner(self):
        self.window = Gtk.Window()
        self.window.set_decorated(False)
        self.window.set_app_paintable(True)
        self.window.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.window.set_keep_above(True)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_skip_pager_hint(True)
        self.window.set_default_size(self.monitor.get_geometry().width, self.banner_height)
        self.window.move(self.monitor.get_geometry().x,self.monitor.get_geometry().y + self.voffset)

        screen = self.window.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.window.set_visual(visual)

        self.window.connect("realize", self.on_realize)
        self.window.connect("draw", self.on_draw)
        self.window.show_all()

    def on_realize(self, widget):
        self.set_strut_properties()

    def set_strut_properties(self):
        display = Display()
        gdk_window = self.window.get_window()
        xid = gdk_window.get_xid()
        x11_window = display.create_resource_object('window', xid)

        geometry = self.monitor.get_geometry()
        x = geometry.x

        width = geometry.width

        # Reserve space (a "strut") for the bar
        strut_top = self.banner_height + self.voffset
        x11_window.change_property(display.intern_atom('_NET_WM_STRUT'),
                                   display.intern_atom('CARDINAL'), 32,
                                   [0, 0, strut_top, 0],
                                   X.PropModeReplace)
        x11_window.change_property(display.intern_atom('_NET_WM_STRUT_PARTIAL'),
                                   display.intern_atom('CARDINAL'), 32,
                                   [0, 0, strut_top, 0, 0, 0, 0, 0, x, x + width - 1, 0, 0],
                                   X.PropModeReplace)

    def on_draw(self, widget, cr):
        # Set background color
        bg_color = Gdk.RGBA()
        bg_color.parse(self.bgcolor)
        cr.set_source_rgba(bg_color.red, bg_color.green, bg_color.blue, bg_color.alpha)
        cr.paint()

        # Set text properties
        layout = widget.create_pango_layout(self.message)
        font_desc = Pango.FontDescription(f"{self.font} {self.font_size} {self.font_weight}")
        layout.set_font_description(font_desc)
        layout.set_alignment(Pango.Alignment.CENTER)

        # Set foreground color
        fg_color = Gdk.RGBA()
        fg_color.parse(self.fgcolor)
        cr.set_source_rgba(fg_color.red, fg_color.green, fg_color.blue, fg_color.alpha)

        # Calculate position to center the text vertically
        width, height = self.window.get_size()
        text_width, text_height = layout.get_size()
        text_width /= Pango.SCALE
        text_height /= Pango.SCALE
        x = (width - text_width) / 2
        y = (height - text_height) / 2

        # Move to the calculated position and draw text using PangoCairo
        cr.move_to(x, y)
        PangoCairo.update_layout(cr, layout)
        PangoCairo.show_layout(cr, layout)

    def auto_resize(self):
        self.window.set_default_size(self.monitor.get_geometry().width, self.banner_height)
        self.window.move(self.monitor.get_geometry().x, self.monitor.get_geometry().y + self.voffset)
        self.window.resize(self.monitor.get_geometry().width, self.banner_height)
        self.window.queue_draw()
        self.set_strut_properties()

class MultiWindowBanner:
    GNOME_MAIN_BAR_HEIGHT = 24
    def __init__(self, fgcolor, bgcolor, font, size, font_weight, banner_height, all_monitor_voffset, message):
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
        self.font = font
        self.size = size
        self.font_weight = font_weight
        self.banner_height = banner_height
        self.all_monitor_voffset = all_monitor_voffset
        self.message = message
        self.banners = {}
        self.lower_banner_boundary = 0

        screen = Gdk.Screen.get_default()
        screen.connect("monitors-changed", self.resize_banners)
        screen.connect("size-changed", self.resize_banners)

        self.create_banners()

    def create_banners(self):
        display = Gdk.Display.get_default()
        num_monitors = display.get_n_monitors()
        print(f"Creating banners for {num_monitors} monitors")

        for i in range(num_monitors):
            self.create_banner(display, i)

    def create_banner(self, display, monitor_index):
        monitor = display.get_monitor(monitor_index)
        is_primary = display.get_primary_monitor() == monitor
        voffset = self.all_monitor_voffset + (self.GNOME_MAIN_BAR_HEIGHT if is_primary else 0)
        self.lower_banner_boundary = voffset + self.banner_height
        banner = Banner(self.fgcolor, self.bgcolor, self.font, self.size, self.font_weight, self.banner_height, monitor, voffset, self.message)
        self.banners[monitor_index] = banner
        print(f"Created banner for monitor {monitor_index} with bgcolor={self.bgcolor}")

    def resize_banners(self, event=None):
        display = Gdk.Display.get_default()
        num_monitors = display.get_n_monitors()
        print(f"Resizing banners for {num_monitors} monitors")

        for i in range(num_monitors):
            if i not in self.banners or self.banners[i] is None:
                self.create_banner(display, i)
            else:
                self.banners[i].auto_resize()
                print(f"Resized banner for monitor {i} with bgcolor={self.banners[i].bgcolor}")

# Example usage
if __name__ == "__main__":
    display = Gdk.Display.get_default()
    monitor = display.get_monitor(0)
    banner = MultiWindowBanner('#FFFFFF', '#007A33', 'liberation-sans', 'medium', 'bold', 22, 0, 'UNCLASSIFIED//FOUO')
    Gtk.main()