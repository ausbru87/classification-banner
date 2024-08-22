from banner import MultiWindowBanner

class EnvironmentBanner(MultiWindowBanner):
    env_colors = {
        # ENVIRONMENT: (MESSAGE, TEXT_COLOR, BANNER_COLOR)
        "dev": ("DEVELOPMENT ENVIRONMENT", "#FFFFFF", "#66CDAA"),  # Medium Aquamarine (Lighter Teal)
        "test": ("TEST ENVIRONMENT", "#FFFFFF", "#800080"),  # Purple
        "stage": ("STAGING ENVIRONMENT", "#FFFFFF", "#4682B4"),  # Steel Blue
        "prod": ("PRODUCTION ENVIRONMENT", "#FFFFFF", "#D59890")  # Light Coral Pink
    }

    def __init__(self, classification, vertical_offset=0):
        if classification not in self.classification_colors:
            raise ValueError(f"Invalid classification: {classification}")
        self.classification = classification
        self.vertical_offset = vertical_offset
        message, fgcolor, bgcolor = self.classification_colors[self.classification]
        font = "liberation-sans"
        size = "medium"
        weight = "bold"
        banner_height = 22

        super().__init__(fgcolor, bgcolor, font, size, weight, banner_height, self.vertical_offset, message)