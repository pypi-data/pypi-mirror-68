# bbbmon

A small python based CLI utility to monitor BigBlueButton-Usage. 

## Installation

The easiest way to install bbbmon is to install it from the Python Package Index (PyPi). This project uses [python poetry](https://python-poetry.org/) for dependency management, so you could also run it without installing the package system wide, see instructions below.

## Install with pip3

```bash
sudo pip3 install bbbmon --upgrade
```

Then run with:

```bash
bbbmon
```

## Run with poetry (without pip)

Clone the repo:

```bash
git clone https://code.hfbk.net/bbb/bbbmon.git
```

Make sure you have poetry installed. Install instruction for poetry can be [found here](https://python-poetry.org/docs/#installation).
From inside the project directory run:

```bash
poetry install
```

Run bbbmon with:

```bash
poetry run bbbmon
```



# Configuration

Run `bbbmon config --new` to create a new default configuration file. bbbmon will always ask you before it creates or overwrites anything.

Within the config you can define one or more endpoints with running bbb instances – each with it's secret and bigbluebutton-URL. You can find the secret on your server in it's config-file via 

```bash
cat /usr/share/bbb-web/WEB-INF/classes/bigbluebutton.properties | grep securitySalt=
```

A example configuration file could look like this:
```toml
[bbb.example.com]
securitySalt=MY_SUPER_SECRET_SECRET
bigbluebutton.web.serverURL=https://bbb.example.com/

[Föö]
securitySalt=MY_SUPER_SECRET_SECRET2
bigbluebutton.web.serverURL=https://bbb.foo.com/
```
The section names in the square brackets can be chosen arbitrarily (as long as they are unique) and will be used as display names (they support utf-8). It makes sense to keep them short as they can be  used for filtering and/or ordering:

```bash
bbbmon meetings -e Föö
```



# Usage

For help run:

```bash
bbbmon -h
```

bbbmon supports command abbreviations – these commands produce the same result:

```bash
bbbmon meetings
bbbmon meeting
bbbmon mee
bbbmon m
```

This works as long as there is no other command starting with the same letters.