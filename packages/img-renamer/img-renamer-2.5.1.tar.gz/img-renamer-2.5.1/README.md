# Image renamer

Production [![build status](https://gitlab.com/miicat/img-renamer/badges/production/pipeline.svg)](https://gitlab.com/miicat/img-renamer/commits/production)

Master [![build status](https://gitlab.com/miicat/img-renamer/badges/master/pipeline.svg)](https://gitlab.com/miicat/img-renamer/commits/master)

## Description

**img_renamer** is a Python script to rename images in numberic order.


## Usage

See [wiki](https://gitlab.com/miicat/img-renamer/-/wikis/) for full usage


### Basic usage

This will rename all images in `~/Pictures` folder like this: `0000001.png`, `0000002.png`, `0000003.png`...

`img_renamer ~/Pictures`  
Output:

```text
image.png -> 0000001.png
picture.jpg -> 0000002.jpg
img.jpeg -> 0000003.jpg
____________________
Renaming 3 of 3
Are you sure you want to rename (y/n): y
Do you want to save a log file(y/n): n
```


### Print help text

Simply run this `img_renamer --help`


## Author
[Miika Launiainen](https://gitlab.com/miicat)


## Donating

If you want to support me, feel free to use paypal
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/miicat)


## License

This library is licensed under GPLv3
