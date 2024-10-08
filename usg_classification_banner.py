from banner import MultiWindowBanner

class USGClassificationBanner(MultiWindowBanner):
    classification_colors = {
        # CLASSIFICATION: (MESSAGE, TEXT_COLOR, BANNER_COLOR)
        "U": ("UNCLASSIFIED", "#FFFFFF", "#007A33"),
        "U_FOUO": ("UNCLASSIFIED//FOUO", "#FFFFFF", "#007A33"),
        "C": ("CONFIDENTIAL", "#FFFFFF", "#0000FF"),
        "S": ("SECRET", "#FFFFFF", "#FF0000"),
        "TS": ("TOP SECRET", "#FFFFFF", "#FF8C00"),
        "TS_REL": ("TOP SECRET//REL TO USA, FVEY", "#000000", "#FFFF00"),
        "TS_NF": ("TOP SECRET//SI/TK//NOFORN", "#000000", "#FFFF00"),
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