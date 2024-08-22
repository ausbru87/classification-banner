import unittest
from hypothesis import given, strategies as st
from banner_validator import BannerValidator, ValidationError

class TestBannerValidator(unittest.TestCase):

    def setUp(self):
        self.validator = BannerValidator()

    def test_validate_payload_valid(self):
        payload = [
            {
                "banner_type": "classification",
                "banner_subtype": "u",
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
                "banner_subtype": "eol",
                "override_banner_height": 25,
                "override_fgcolor": "#FFFFFF",
                "override_bgcolor": "#000000",
                "override_font_size": "medium",
                "override_font_weight": "bold",
                "vertical_offset": 1000
            }
        ]
        try:
            self.validator.is_valid_payload(payload)
        except ValidationError:
            self.fail("is_valid_payload raised ValidationError unexpectedly!")

    def test_validate_payload_invalid_banner_type(self):
        payload = [
            {
                "banner_type": "invalid_type",
                "banner_subtype": "u"
            }
        ]
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

    def test_validate_payload_invalid_banner_subtype(self):
        payload = [
            {
                "banner_type": "classification",
                "banner_subtype": "invalid_subtype"
            }
        ]
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

    def test_validate_payload_multiple_classification_banners(self):
        payload = [
            {
                "banner_type": "classification",
                "banner_subtype": "u"
            },
            {
                "banner_type": "classification",
                "banner_subtype": "c"
            }
        ]
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

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
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

    def test_validate_payload_multiple_notification_banners(self):
        payload = [
            {
                "banner_type": "notification",
                "banner_subtype": "eol"
            },
            {
                "banner_type": "notification",
                "banner_subtype": "sys_out"
            }
        ]
        try:
            self.validator.is_valid_payload(payload)
        except ValidationError:
            self.fail("is_valid_payload raised ValidationError unexpectedly!")

    # Define a strategy that includes potential malicious strings
    malicious_strings = st.text() | st.sampled_from([
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "<script>alert('XSS')</script>",
        "../../etc/passwd"
    ])

    @given(malicious_strings)
    def test_fuzzing_banner_type(self, fuzzed_string):
        payload = [
            {
                "banner_type": fuzzed_string,
                "banner_subtype": "u"
            }
        ]
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

    @given(malicious_strings)
    def test_fuzzing_override_fgcolor(self, fuzzed_string):
        payload = [
            {
                "banner_type": "classification",
                "banner_subtype": "u",
                "override_banner_height": 25,
                "override_fgcolor": fuzzed_string,
                "override_bgcolor": "#000000",
                "override_font_size": "medium",
                "override_font_weight": "bold",
                "vertical_offset": 1000
            }
        ]
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

    @given(malicious_strings)
    def test_fuzzing_override_bgcolor(self, fuzzed_string):
        payload = [
            {
                "banner_type": "classification",
                "banner_subtype": "u",
                "override_banner_height": 25,
                "override_fgcolor": "#FFFFFF",
                "override_bgcolor": fuzzed_string,
                "override_font_size": "medium",
                "override_font_weight": "bold",
                "vertical_offset": 1000
            }
        ]
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

    @given(malicious_strings)
    def test_fuzzing_override_font_size(self, fuzzed_string):
        payload = [
            {
                "banner_type": "classification",
                "banner_subtype": "u",
                "override_banner_height": 25,
                "override_fgcolor": "#FFFFFF",
                "override_bgcolor": "#000000",
                "override_font_size": fuzzed_string,
                "override_font_weight": "bold",
                "vertical_offset": 1000
            }
        ]
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

    @given(malicious_strings)
    def test_fuzzing_override_font_weight(self, fuzzed_string):
        payload = [
            {
                "banner_type": "classification",
                "banner_subtype": "u",
                "override_banner_height": 25,
                "override_fgcolor": "#FFFFFF",
                "override_bgcolor": "#000000",
                "override_font_size": "medium",
                "override_font_weight": fuzzed_string,
                "vertical_offset": 1000
            }
        ]
        with self.assertRaises(ValidationError):
            self.validator.is_valid_payload(payload)

if __name__ == '__main__':
    unittest.main()