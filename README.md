# Python Alarm Clock CLI

A simple command-line alarm clock application built with Python. It supports creating, listing, deleting, snoozing, and dismissing alarms. A background scheduler continuously checks alarm times and triggers alarms automatically.

## Features

- Create alarms using strict 24-hour `HH:MM` format.
- List all alarms and view their current status.
- Delete alarms using their unique ID.
- Automatically trigger alarms in the background.
- Snooze a ringing alarm for a configurable number of minutes (5 minutes by default).
- Dismiss ringing alarms.
- Handle snooze durations that cross midnight.
- Validate user input and handle invalid operations.
- Unit tests for alarm logic and scheduler behaviour.

## Tech Stack

- **Language:** Python 3.13
- **Standard Library:** `threading`, `datetime`, `dataclasses`, `unittest`, `uuid`, `re`
- **Dependencies:** No external packages required.

## Project Structure

```text
python-alarm-clock/
│
├── alarm_clock/
│   ├── __init__.py
│   ├── main.py
│   ├── alarm.py
│   ├── scheduler.py
│   └── cli.py
│
├── tests/
│   ├── __init__.py
│   ├── test_alarm.py
│   └── test_scheduler.py
│
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10 or later.
- A terminal or command prompt.

## Installation

Clone the repository:

```bash
git clone <your-github-repository-url>
cd python-alarm-clock
```

Create a virtual environment:

**Windows:**

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No additional packages are required.

## Run the Application

```bash
python -m alarm_clock.main
```

## Usage

After starting the application, the following menu is displayed:

```text
===== PYTHON ALARM CLOCK =====
1. Add Alarm
2. List Alarms
3. Delete Alarm
4. Snooze Alarm
5. Dismiss Alarm
6. Exit
```

### Create an Alarm

Select option `1` and enter a time in 24-hour format.

Example:

```text
Enter alarm time (HH:MM): 18:30
Alarm created successfully.
```

### List Alarms

Select option `2` to view all alarms, their IDs, scheduled times, and statuses.

### Delete an Alarm

Select option `3` and enter the alarm ID.

### Snooze an Alarm

When an alarm is ringing, select option `4`, enter its ID, and provide a snooze duration in minutes. Press Enter to use the default five-minute duration.

### Dismiss an Alarm

Select option `5` and enter the ID of the ringing alarm to stop and disable it.

## Running Tests

Run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- Alarm creation and time validation.
- Starting and stopping alarms.
- Snooze duration validation.
- Snooze across midnight.
- Adding and removing alarms.
- Triggering alarms at the correct time.
- Preventing duplicate triggers.
- Snoozed alarm scheduling.

## Design Overview

The application separates responsibilities into three main components:

**1. Alarm Model (`alarm.py`)**

Represents an individual alarm and manages its state, including whether it is enabled, ringing, or snoozed.

**2. Alarm Scheduler (`scheduler.py`)**

Maintains the collection of alarms and checks them periodically using a background thread. It handles both regular and snoozed alarm triggers.

**3. Command-Line Interface (`cli.py`)**

Handles user interaction, input validation, and alarm operations. It communicates with the alarm model and scheduler.

The entry point is `main.py`.

## Engineering Decisions

- **Separation of concerns:** Alarm logic, scheduling, and user interaction are kept in separate modules.
- **Standard library only:** Avoids unnecessary third-party dependencies.
- **Dataclasses:** Used to represent alarm state clearly.
- **Unique IDs:** Each alarm receives a unique identifier for management.
- **Background execution:** A separate thread allows the scheduler to check alarms while the CLI remains available.
- **Time-based testing:** Scheduler methods accept an optional current datetime, allowing deterministic tests without waiting for real-time alarms.
- **Input validation:** Alarm times follow strict 24-hour `HH:MM` formatting.

## Current Limitations

- Alarm data is stored in memory and is not persisted after the application exits.
- The application currently uses terminal notifications rather than audio playback.
- The scheduler checks alarms periodically, so triggering can have a small delay.
- The application is designed for a single local process.

## Future Improvements

- Add persistent alarm storage.
- Add configurable alarm sounds.
- Support recurring and one-time alarm settings.
- Add timezone support.
- Improve concurrent alarm-state management.

## License

This project is developed as a software engineering assessment and learning exercise.

## Author

**Rakesh Das**  
Senior Full Stack Developer

- **Email:** bcarakesh03@gmail.com
- **Phone:** +91 7076480257
- **LinkedIn:** https://www.linkedin.com/in/rakesh-das-a04a03229/