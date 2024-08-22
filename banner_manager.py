import json
from banner import MultiWindowBanner
from usg_classification_banner import USGClassificationBanner

class BannerManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.banners = {
            'classification': None,
            'custom': []
        }
        self.current_voffset = 0
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config = json.load(file)
            self.initialize_banners(config)

    def initialize_banners(self, config):
        self.banners = {
            'classification': None,
            'custom': []
        }
        for banner_def in config:
            print("banner_def: {}".format(banner_def))
            banner_type = banner_def['banner_type']
            if banner_type == 'classification':
                if self.banners['classification'] is None:
                    banner = USGClassificationBanner(banner_def['banner_subtype'])
                    print("Created classification banner with lower boundary: {}".format(banner.lower_banner_boundary))
                    self.banners['classification'] = banner
                    self.current_voffset += banner.lower_banner_boundary
                else:
                    print("Classification banner already exists. Skipping...")
            elif banner_type == 'custom':
                banner = MultiWindowBanner(
                    banner_def['fgcolor'],
                    banner_def['bgcolor'],
                    banner_def['font'],
                    banner_def['font_size'],
                    banner_def['font_weight'],
                    banner_def['banner_height'],
                    self.current_voffset,
                    banner_def['message']
                )
                self.banners['custom'].append(banner)
                print("Created custom banner with lower boundary: {}".format(banner.lower_banner_boundary))
                self.current_voffset += banner.banner_height  # Update only once
                print("Updated current_voffset to: {}".format(self.current_voffset))
            else:
                print("Unknown banner type: {}. Skipping...".format(banner_type))
            
        # After the loop, print the final state of the banners
        print("Final state of banners:")
        print("Classification banner: {}".format(vars(self.banners['classification']) if self.banners['classification'] else "None"))
        for custom_banner in self.banners['custom']:
            print("Custom banner: {}".format(vars(custom_banner)))

# Example usage
if __name__ == "__main__":
    manager = BannerManager('banner_conf.json')
    for banner_type, banners in manager.banners.items():
        if banner_type == 'classification':
            print(vars(banners))
        else:
            for banner in banners:
                print(vars(banner))