#!/usr/bin/env python3
import serial
import argparse
import time
import sys
import re
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="enjoin",
        description="A small tool to enjoin serial commands.",
    )
    parser.add_argument(
        "command",
        type=str,
        help="the command to enjoin",
    )
    parser.add_argument(
        "-e",
        "--expect",
        type=str,
        help="what to expect; will just send the command if argument is not set",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=str,
        default="",
        help="serial port name",
    )
    parser.add_argument(
        "-b",
        "--baud",
        metavar="BAUDRATE",
        type=int,
        default=0,
        help="baud rate, default: 115200",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
    )
    parser.add_argument(
        "-a",
        "--autocheck",
        action="store_true",
        help="command will fail if the enjoined command has failed, even if there was no output. Results in <command> || echo FAILPATTERN",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0.2,
        help="time to wait for a response, default 200ms",
    )
    return parser.parse_args()


def send_and_read_lines(ser: serial.Serial, args):
    if args.autocheck:
        args.command += " || echo 12b342b71"
        args.expect = "12b342b71"
    bytes_send = f"{args.command}\r".encode("utf-8")
    len_send = len(bytes_send)
    ser.write(bytes_send)
    if not args.expect:
        time.sleep(args.timeout)
        return True
    buffer = ""
    byte_count = 0
    t_send = time.time()
    while time.time() - t_send < args.timeout:
        if ser.inWaiting() < 1:
            time.sleep(0.001)
            continue
        new_char = ser.read().decode("utf-8")
        if not new_char == "\n":
            byte_count += 1
            if byte_count > len_send:  # ignore echo output
                buffer += new_char
        else:
            if args.verbose > 0:
                print(buffer)
            if find_text(args.expect, buffer):
                return True
            buffer = ""
    if find_text(args.expect, buffer):
        return True
    return False


def find_text(pattern: str, text: str):
    findings = re.search(pattern, text)
    if not findings:
        return False
    return True


def main():
    args = parse_arguments()

    port = os.getenv("ENJOIN_PORT", "")
    baud = int(os.getenv("ENJOIN_BAUD", "115200"))
    if args.port:
        port = args.port
    if args.baud:
        baud = args.baud

    ser = serial.Serial(port, baud, timeout=1)
    if args.verbose > 1:
        print(f"connected to: {ser.name} with {ser.baudrate}")

    if not send_and_read_lines(ser, args):
        if args.verbose > 0:
            print(f"\033[91mERROR:\033[0m could not find expected pattern '{args.expect}'")
        ser.close()
        sys.exit(1)
    ser.close()


if __name__ == "__main__":
    main()
