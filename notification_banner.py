from banner import MultiWindowBanner

class NotificationBanner(MultiWindowBanner):
    notification_colors = {
        # NOTIFICATION TYPE: (MESSAGE, TEXT_COLOR, BANNER_COLOR)
        "SCHEDULED_EVENT": ("SCHEDULED EVENT", "#FFFFFF", "#00BFFF"),  # Deep Sky Blue
        "SYSTEM_OUTAGE": ("SYSTEM OUTAGE", "#FFFFFF", "#8B0000"),  # Dark Red
        "END_OF_LIFE": ("END OF LIFE NOTICE", "#FFFFFF", "#8B4513")  # Saddle Brown
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