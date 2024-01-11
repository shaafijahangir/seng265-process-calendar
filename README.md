# Calendar Event Parser

## Overview

The Calendar Event Parser is a Python project that facilitates the extraction and presentation of calendar events from ICS (iCalendar) files. The core functionality is encapsulated in the `process_cal` class within the `process_cal4.py` file.

## Features

- **Constructor:**
  - Initializes the `process_cal` class with the name of the ICS file.

- **`get_events_for_day` Method:**
  - Takes a datetime object as input.
  - Checks for events on the specified date in the ICS file.
  - Returns a formatted string of the day's events or `None` if no events are found.

- **Modularity and Encapsulation:**
  - Encourages additional class and method implementation for a clean and organized structure.

- **Regular Expressions:**
  - Mandates the use of Python's `re` module for efficient data extraction.

- **Test-Driven Development:**
  - Seamlessly integrates with the provided `tester4.py` for rigorous testing.

- **Documentation:**
  - Requires comprehensive docstrings at all levels for clarity during code reviews.

## Instructions

1. Implement the program in `process_cal4.py`.
2. Utilize the provided `tester4.py` for testing purposes.
3. Maintain clean code practices, avoiding output to stdout within the `process_cal` class.
4. Submit a clean file with no residual commented lines or unintended artifacts.

## Usage

```bash
./tester4.py --start=2021/01/24 --end=2021/4/15 --file=<example>.ics
