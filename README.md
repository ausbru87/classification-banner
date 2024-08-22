# Gnome Desktop Banner


## Installation

### Install System Dependencies


#### Debian Systems
```bash
sudo apt-get update
sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-xlib
```


#### Red Hat Systems
```bash
sudo dnf install -y python3-gobject python3-cairo gtk3 python3-xlib
```

## Known Issues

* Struts are not properly set on secondary monitors. This results in the banners overlapping the active windows on the desktop for those monitors.
* When the `BannerManager` is used in a single monitor configuration, the voffset for the second banner in the config file has an incorrect offset creating a gap between the classification banner and the first custom banner.
  * This is not the case when the `BannerManager` is used to deploy the banners in a dual+ monitor configuration. The banners are displayed with the correct voffsets
