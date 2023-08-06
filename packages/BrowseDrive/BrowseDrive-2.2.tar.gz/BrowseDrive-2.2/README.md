BrowseDrive is a package that allows for one to download the browser driver files used during browser automation with selenium. This package covers downloads for geckodriver and chromedriver. This package also has a module for the automation of browser drivers. 

## Installation
```python
pip3 install BrowseDrive==2.1

```

## Usage
```python 
import BrowseDrive
from BrowseDrive.driverdownloader import DriverDownloader

```

## Downloading drivers 
```python
downloader = DriverDownloader() 
downloader.set_savepath("") # Save path goes inside here
downloader.download() # Starts the download process

```

