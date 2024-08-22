from cerberus import Validator
import re

class ValidationError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

class BannerValidator:
    HEX_COLOR_PATTERN = re.compile(r'^#[0-9A-Fa-f]{6}$')
    VALID_FONT_SIZES = ("small", "medium", "large")
    VALID_FONT_WEIGHTS = ("bold", "normal", "light")
    VALID_TYPES = ("classification", "environment", "notification")
    VALID_SUBTYPES = {
        "classification": ("u", "u_fouo", "c", "s", "ts", "ts_rel", "ts_nf"),
        "environment": ("dev", "test", "stage", "prod"),
        "notification": ("eol", "sched_event", "sys_out")
    }
    OPTIONAL_FIELDS = ["append_message", "override_message", "override_fgcolor", "override_bgcolor", "override_banner_height", "override_font_size", "override_font_weight", "vertical_offset"]
    VALID_FIELDS = ["banner_type", "banner_subtype"] + OPTIONAL_FIELDS

    schema = {
        'banner_type': {'type': 'string', 'allowed': VALID_TYPES},
        'banner_subtype': {'type': 'string', 'allowed': sum(VALID_SUBTYPES.values(), ())},
        'append_message': {'type': 'string', 'nullable': True},
        'override_message': {'type': 'string', 'nullable': True},
        'override_fgcolor': {'type': 'string', 'regex': HEX_COLOR_PATTERN.pattern, 'nullable': True},
        'override_bgcolor': {'type': 'string', 'regex': HEX_COLOR_PATTERN.pattern, 'nullable': True},
        'override_banner_height': {'type': 'integer', 'nullable': True},
        'override_font_size': {'type': 'string', 'allowed': VALID_FONT_SIZES, 'nullable': True},
        'override_font_weight': {'type': 'string', 'allowed': VALID_FONT_WEIGHTS, 'nullable': True},
        'vertical_offset': {'type': 'integer', 'nullable': True}
    }

    def is_valid_payload(self, payload):
        v = Validator(self.schema)
        classification_count = 0
        environment_count = 0

        for banner_info in payload:
            if not v.validate(banner_info):
                raise ValidationError(f"Payload is invalid: {v.errors}", v.errors)

            banner_type = banner_info.get("banner_type")
            if banner_type == "classification":
                classification_count += 1
                if classification_count > 1:
                    raise ValidationError("Payload is invalid: Only one classification banner is allowed.")
            elif banner_type == "environment":
                environment_count += 1
                if environment_count > 1:
                    raise ValidationError("Payload is invalid: Only one environment banner is allowed.")

        return True

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