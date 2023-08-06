# clirail

Command line application for the iRail API

iRail provides an API for Belgian trains.

## Installation
```
pip install --user --upgrade clirail
```

Then make sure the installed executable will be found. On UNIX-like systems, this means checking that `~/.local/bin/` is [in your PATH](https://opensource.com/article/17/6/set-path-linux).

## Usage
|Command                                       |Function                                       |
|----------------------------------------------|-----------------------------------------------|
|clirail <station> ['' <moment>]               |Liveboard (list of trains departing in station)|
|clirail <from_station> <to_station> [<moment>]|Route planning                                 |
|clirail                                       |Analyse current timeliness in a few stations   |

Omit the `<moment>` for ASAP departures.

Give either the name or the telegraphic code. Names are matched fuzzily and intuitively. You can
learn telegraphic codes by looking at a liveboard in clirail.

## Licenses
* clirail code is released under GNU GPLv3+.
* xdg is released under ISC.

## Known issues
* If `<moment>` is just a time, it will be considered as today, even though in some cases it would
  make more sense to consider it as tomorrow (e.g. at 11 PM planning a route with departure at 7 AM).

## Development
To create a virtualenv and install the dependencies in it:
```
tools/create_venv.py
```

Activate the virtualenv with `source venv/bin/activate`. Then run `bin/clirail` to run the program.

Important: make sure the virtualenv is activated each time you run, otherwise your global `clirail`
installation may be used.

If you introduce dependencies, list them in `setup.py` under `install_requires`, and run
`tools/update_requirements.sh`.
