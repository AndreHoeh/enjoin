# enjoin

This tool sends commands via serial connection and waits for a expected response. The command will fail if the expected pattern does not appear within a set timeout.

___

## Features

- send serial commands
- search the response for a pattern
- regex support
- timeout support (seconds as float)
- early return if the pattern appears before the time is up
- optional verbosity levels
- shows usage (--help)
- options can be abbreviated
- support for environment variables to set port and baud rate

## Example Command

The following three commands will connect via serial port "COM5" and send the command "ls -la". The enjoin command will fail if the expected pattern "root" will not appear as a response within the set timeout.

    python .\enjoin.py "ls -la" --port COM5 --expect "root" --timeout 1 --verbose
    python .\enjoin.py "ls -la" --po COM5 --e "root" --tim 1 --verb
    python .\enjoin.py "ls -la" -p COM5 -e "root" -t 1 -v

you can set the port name and the baud rate as an environment variable and omit the parameters

    export ENJOIN_PORT="/dev/ttyUSB0"
    export ENJOIN_BAUD="115200"
    python .\enjoin.py "ls -la" -e "root"

The following command uses a regular expression pattern and will also find the word "root"

    python .\enjoin.py "ls -la" -e "r.*t" -v

Expecting a pattern is optional. You can just use the tool to send a command. This command will fail if the serial port could not be used. 
In this example, the program will wait for 1 second after the command was sent.

    python .\enjoin.py ls -t 1

If you just want to send a command and read the output, you have to expect something, that will most likely not be found.

    python .\enjoin.py ls -e "answer to my problems"

Use the autocheck option to handle commands that don't write any output when they fail.

    python .\enjoin.py rm file_that_does_not_exist -a

## Usage

    usage: enjoin [-h] [-e EXPECT] [-p PORT] [-b BAUDRATE] [-v] [-a] [-t TIMEOUT] command

    A small tool to enjoin serial commands.

    positional arguments:
    command               the command to enjoin

    options:
    -h, --help            show this help message and exit
    -e EXPECT, --expect EXPECT
                            what to expect; will just send the command if argument is not set
    -p PORT, --port PORT  serial port name
    -b BAUDRATE, --baud BAUDRATE
                            baud rate, default: 115200
    -v, --verbose
    -a, --autocheck       command will fail if the enjoined command has failed, even if there was no output. Results in <command> || echo FAILPATTERN
    -t TIMEOUT, --timeout TIMEOUT
                            time to wait for a response, default 200ms

## Dependencies

- python
  - python package: pyserial

### Install python requirements

    python -m pip install pyserial