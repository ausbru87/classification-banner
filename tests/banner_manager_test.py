import unittest
from hypothesis import given, strategies as st
from banner_manager import BannerManager

class TestBannerManager(unittest.TestCase):

    def setUp(self):
        self.manager = BannerManager()

    def test_validate_payload_valid(self):
        payload = [
            {
                "banner_type": "system_classification",
                "banner_subtype": "U",
                "override_banner_height": 25,
                "override_fgcolor": "#FFFFFF",
                "override_bgcolor": "#000000",
                "override_font_size": "medium",
                "override_font_weight": "bold",
                "vertical_offset": 1000
            },
            {
                "banner_type": "environment",
                "banner_subtype": "prod",
                "override_banner_height": 25,
                "override_fgcolor": "#FFFFFF",
                "override_bgcolor": "#000000",
                "override_font_size": "medium",
                "override_font_weight": "bold",
                "vertical_offset": 1000
            },
            {
                "banner_type": "notification",
                "banner_subtype": "info",
                "override_banner_height": 25,
                "override_fgcolor": "#FFFFFF",
                "override_bgcolor": "#000000",
                "override_font_size": "medium",
                "override_font_weight": "bold",
                "vertical_offset": 1000
            }
        ]
        try:
            self.manager.validate_payload(payload)
        except ValueError:
            self.fail("validate_payload raised ValueError unexpectedly!")

    def test_validate_payload_invalid_banner_type(self):
        payload = [
            {
                "banner_type": "invalid_type",
                "banner_subtype": "U"
            }
        ]
        with self.assertRaises(ValueError):
            self.manager.validate_payload(payload)

    def test_validate_payload_invalid_banner_subtype(self):
        payload = [
            {
                "banner_type": "system_classification",
                "banner_subtype": "invalid_subtype"
            }
        ]
        with self.assertRaises(ValueError):
            self.manager.validate_payload(payload)

    def test_validate_payload_multiple_classification_banners(self):
        payload = [
            {
                "banner_type": "system_classification",
                "banner_subtype": "U"
            },
            {
                "banner_type": "system_classification",
                "banner_subtype": "C"
            }
        ]
        with self.assertRaises(ValueError):
            self.manager.validate_payload(payload)

    def test_validate_payload_multiple_environment_banners(self):
        payload = [
            {
                "banner_type": "environment",
                "banner_subtype": "prod"
            },
            {
                "banner_type": "environment",
                "banner_subtype": "dev"
            }
        ]
        with self.assertRaises(ValueError):
            self.manager.validate_payload(payload)

    def test_validate_payload_multiple_notification_banners(self):
        payload = [
            {
                "banner_type": "system_notification",
                "banner_subtype": "info"
            },
            {
                "banner_type": "system_notification",
                "banner_subtype": "warning"
            }
        ]
        try:
            self.manager.validate_payload(payload)
        except ValueError:
            self.fail("validate_payload raised ValueError unexpectedly!")

if __name__ == '__main__':
    unittest.main()