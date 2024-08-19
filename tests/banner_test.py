from unittest import TestCase
from unittest.mock import MagicMock, patch
from banner import Banner, MultiWindowBanner

class TestBanner(TestCase):

    @patch('banner.Gtk.Window')
    @patch('banner.Gtk.CssProvider')
    @patch('banner.Gdk.Screen')
    @patch('banner.Gdk.Display')
    @patch('banner.Display')
    def test_banner_initialization(self, mock_display, mock_gdk_display, mock_gdk_screen, mock_css_provider, mock_gtk_window):
        # Mocking Gdk and Gtk components
        mock_window = mock_gtk_window.return_value
        mock_screen = mock_gdk_screen.return_value
        mock_gdk_display.get_default.return_value.get_default_screen.return_value = mock_screen
        mock_css_provider_instance = mock_css_provider.return_value
        mock_display_instance = mock_display.return_value
        
        monitor_mock = MagicMock()
        banner = Banner("white", "black", "Arial", "medium", "bold", 30, monitor_mock)

        # Assertions for window initialization
        mock_gtk_window.assert_called_once()
        mock_window.set_name.assert_called_once_with("bar")
        mock_window.set_type_hint.assert_called_once_with(mock_gdk_display().get_default().WindowTypeHint.DOCK)
        mock_window.set_decorated.assert_called_once_with(False)
        mock_window.set_keep_above.assert_called_once_with(True)
        mock_window.stick.assert_called_once()

        # Assertions for style application
        mock_css_provider.load_from_data.assert_called_once()
        mock_screen.add_provider_for_screen.assert_called_once_with(
            mock_screen, mock_css_provider_instance, mock_gtk_window.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Assertions for label addition
        mock_window.add.assert_called_once()
        mock_window.show_all.assert_called_once()

        # Assertions for display initialization
        mock_display.assert_called_once()
        mock_display_instance.create_resource_object.assert_called_once()