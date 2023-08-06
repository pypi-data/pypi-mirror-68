# clirail

Command line application for the iRail API

iRail provides an API for Belgian trains.

## Installation
```
pip install clirail
```

## Usage
Stations can be identified by name or by telegraphic code. You can learn telegraphic codes by
looking at a liveboard in clirail, or looking at stations' Wikipedia articles.

### Liveboard
A list of the trains departing shortly in a station.
* `./clirail STATION`: departing ASAP
* `./clirail STATION '' DEPARTURE_MOMENT`: departing at another moment

### Route planning
* `./clirail FROM_STATION TO_STATION`: departing ASAP
* `./clirail FROM_STATION TO_STATION DEPARTURE_MOMENT`: departing at another moment

### Disturbances
A list of all recent disturbances on the network.
* `./clirail`

## Licenses
* clirail code is released under GNU GPLv3+.
* xdg is released under ISC.

## Known issues
* Provided dates will be today, even though in some cases it makes more sense to consider it
  "tomorrow" (e.g. at 11 PM planning a route with departure at 7 AM)
* No help text yet

## Development
To create a virtualenv and install the dependencies in it:
```
tools/create_venv.py
```

If you introduce dependencies, list them in `setup.py` under `install_requires`, and run
`tools/update_requirements.sh`.
