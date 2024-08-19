import re

class BannerManager:
    def __init__(self):
        self.hex_color_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        self.valid_font_sizes = {"small", "medium", "large"}
        self.valid_font_weights = {"bold", "normal", "light"}
        self.valid_subtypes = {
            "system_classification": {"U", "U_FOUO", "C", "S", "TS", "TS_REL", "TS_NF"},
            "system_environment": {"DEV", "TEST", "STAGE", "PROD"},
            "system_notification": {"EOL", "SCHED_EVENT", "SYS_OUT"}
        }

    def validate_payload(self, payload):
        classification_count = 0
        environment_count = 0

        for banner_info in payload:
            if not isinstance(banner_info, dict):
                raise ValueError("Invalid banner info format")

            banner_type = banner_info.get("banner_type")
            self.validate_banner_type(banner_type)
            self.validate_banner_subtype(banner_type, banner_info.get("banner_subtype"))

            if banner_type == "system_classification":
                classification_count += 1
                if classification_count > 1:
                    raise ValueError("Only one classification banner is allowed.")
            elif banner_type == "environment":
                environment_count += 1
                if environment_count > 1:
                    raise ValueError("Only one environment banner is allowed.")
            elif banner_type == "notification":
                continue  # Any number of notification banners are allowed
            else:
                raise ValueError(f"Invalid banner type: {banner_type}")

            optional_fields = ["append_message", "override_message", "override_fgcolor", "override_bgcolor",
                               "override_font", "override_font_weight", "override_font_size", "override_banner_height",
                               "vertical_offset"]

            for field in optional_fields:
                if field in banner_info:
                    self.validate_field(field, banner_info[field])

    def validate_banner_type(self, banner_type):
        if banner_type not in self.valid_subtypes:
            raise ValueError(f"Invalid banner type: {banner_type}")

    def validate_banner_subtype(self, banner_type, banner_subtype):
        if banner_subtype not in self.valid_subtypes.get(banner_type, set()):
            raise ValueError(f"Invalid banner subtype: {banner_subtype} for banner type: {banner_type}")

    def validate_field(self, field, value):
        if field == "override_banner_height":
            self.validate_override_banner_height(value)
        elif field in ["override_fgcolor", "override_bgcolor"]:
            self.validate_hex_color(value, field)
        elif field == "override_font_size":
            self.validate_font_size(value)
        elif field == "override_font_weight":
            self.validate_font_weight(value)
        elif field == "vertical_offset":
            self.validate_vertical_offset(value)
        else:
            self.validate_string_field(value, field)

    def validate_override_banner_height(self, value):
        if not isinstance(value, int) or not (20 <= value <= 30):
            raise ValueError(f"Invalid value for override_banner_height: {value}. It must be an integer between 20 and 30.")

    def validate_hex_color(self, value, field):
        if not isinstance(value, str) or not self.hex_color_pattern.match(value):
            raise ValueError(f"Invalid value for {field}: {value}. It must be a hex color code in the format #FFFFFF.")

    def validate_font_size(self, value):
        if value not in self.valid_font_sizes:
            raise ValueError(f"Invalid value for override_font_size: {value}. It must be one of {self.valid_font_sizes}.")

    def validate_font_weight(self, value):
        if value not in self.valid_font_weights:
            raise ValueError(f"Invalid value for override_font_weight: {value}. It must be one of {self.valid_font_weights}.")

    def validate_vertical_offset(self, value):
        if not isinstance(value, int) or not (0 <= value <= 5000):
            raise ValueError(f"Invalid value for vertical_offset: {value}. It must be an integer between 0 and 5000.")

    def validate_string_field(self, value, field):
        if not isinstance(value, str):
            raise ValueError(f"Invalid value for {field}: {value}")

    def sanitize_payload(self, payload):
        sanitized_payload = []
        for banner_info in payload:
            sanitized_info = {}
            for key, value in banner_info.items():
                if isinstance(value, str):
                    sanitized_info[key] = value.strip()
                else:
                    sanitized_info[key] = value
            sanitized_payload.append(sanitized_info)
        return sanitized_payload