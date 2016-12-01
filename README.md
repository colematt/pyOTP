# pyOTP
`pyOTP` is a Python 3 implementation of the following Internet Engineering Task Force One-Time Password (OTP) algorithms:

* HMAC-based One-Time Password (HOTP) proposed by [RFC 4226](https://tools.ietf.org/html/rfc4226).
* Time-based One-Time Password (TOTP) proposed by [RFC 6238](https://tools.ietf.org/html/rfc6238).

`pyOTP` uses [`zbarlight`](https://github.com/Polyconseil/zbarlight) to read qrcodes as a source for the shared key.

## Requirements

| Software | Version |
|----------|---------|
| [Python](https://www.python.org/downloads/)  | Tested with Python 3.5.0. Will not work with Python 2 |
| _Mac OS_: [Macports](https://www.macports.org/install.php)|  Tested with Macports for macOS Sierra v10.12 |
| [Zbar](http://zbar.sourceforge.net/download.html) | Tested with zbar v0.10 |

`pyOTP` has been tested on the following operating systems:

| OS | Version |
|----|---------|
| MacOS | Sierra v10.12.1 |
| Linux | Ubuntu v14.04 LTS |

## Installation
### MacOS
1. Install `ImageMagick` image processing libraries using MacPorts package manager:

        $ sudo port install ImageMagick

2. Download `zbar` source code. Uncompress the source code to the location of your choice (the location does not affect installation).

3. Navigate to the uncompressed zbar source code directory. Install `zbar` and its header files.

        $ ./configure --disable-video --without-python --without-gtk --without-qt
        $ sudo make && make install

4. Install `zbarlight` wrapper using pip:

        $ pip3 install zbarlight

### Linux
1. Install `zbar` and its header files using your package manager:

        $ apt-get install libzbar0 libzbar-dev

2. Install `zbarlight` wrapper using pip:

        $ pip3 install zbarlight
  
## Usage

    /usr/bin/env python3 demo.py [-h] [--displayuri] qrfile

    positional arguments:
      qrfile        path to the shared secret key QR Code .png file

    optional arguments:
      -h, --help    show this help message and exit
      --displayuri  Display the contents of the URI
