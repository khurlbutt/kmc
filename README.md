# kmc
Kinetic Monte Carlo Simulation

## Setup
Parts of the data model are stored using protobufs
more info: https://github.com/google/protobuf/tree/master/python
There's some brew/pip installs for the proto comiler (aka protoc).
In essence, we want the kmc/proto/*.py files generally available for import.
* chmod 700 proto/setup.sh
* . proto/setup.sh

Requires python 3.5.2 and pip.
* pip install -r requirements.txt

Run the display server in the background.
* python display/server.py

Visit localhost:8888 in your browser.
* Going through the toy examples in order will give you a gist
* Start with localhost:8888/print-toy/1
* Move through the handful of dummy/toy examples (srsly)
* Try 'jumping' to a simulation step with ?stop_step=N (N < 1000 for now, tho actually running a sim!)

If developing, please use flake8 to help us adhere to PEP8 style guidelines.
* flake8 --install-hook git
* git config --bool flake8.strict true
* git config --bool flake8.lazy true


README Last Updated September 16, 2017
