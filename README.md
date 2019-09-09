# pyOTP
`pyOTP` is a Python 3 implementation of the following Internet Engineering Task Force One-Time Password (OTP) algorithms:

* HMAC counter-based One-Time Password (HOTP) proposed by [RFC 4226](https://tools.ietf.org/html/rfc4226).
* Time-based One-Time Password (TOTP) proposed by [RFC 6238](https://tools.ietf.org/html/rfc6238).

`pyOTP` uses [`zbarlight`](https://github.com/Polyconseil/zbarlight) to read QR codes as a source for the shared key, and [`dateutil`](https://dateutil.readthedocs.io/en/stable/parser.html#) to parse time strings for the HOTP counter value.

## Requirements

| Software                                    | Version       |
|---------------------------------------------|---------------|
| [Python](https://www.python.org/downloads/) | Python >= 3.2 |
| [Pip](https://pip.pypa.io/en/stable/)       |               |
| _Mac OS_: [Homebrew](https://brew.sh)       |               |

## Installation
### MacOS

```shell
brew update
brew install imagemagick zbar
pip3 install -U pip
pip3 install zbarlight python-dateutil
```

### Linux

```shell
sudo apt update
sudo apt install libzbar0 libzbar-dev python3-pip
pip3 install -U pip
pip3 install zbarlight python-dateutil
```

## Usage

To use the HOTP demo:

```
/usr/bin/env python3 pyotp_pkg/__main__.py [-h] [--displayuri] qrfile

positional arguments:
  qrfile        path to the shared secret key QR Code .png file

optional arguments:
  -h, --help    show this help message and exit
  --displayuri  Display the contents of the URI
```