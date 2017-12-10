# Open Board - A RasperryPi Realtime Train Information Board


Built using a RasperryPi and a [Pimoroni DisplayoTrin HAT](https://github.com/pimoroni/displayotron).

## Installation

```
# Install software dependencies using Pimoroni script
curl -sS get.pimoroni.com/displayotron | bash

# Install python dependencies
pip install -r requirements.txt
```

## Development

```
# Setup a virtual environment
python3 -m venv pyenv

# Install development dependencies
pip install -r requirements-dev.txt
```

## Tests

Run the tests using pytest

```
PYTHONPATH=. py.test
```
