## ElectionDay
### Simple (and insecure!) Python voting system prototype application.

Final project submission.

Login to vote on a party and view current results. To vote you must be a registered voter and enter your name and voter ID.

## Installation
First you need to rename `data/sample-data.json` to `data.json` (or change the path in `setup.py`).

Also rename `.sample-env` to `.env` and set `PASSWORD` required to view results.

Install with Pip when in project folder (`ElectionDay`):
```
pip install -e .
```
This will create the database and populate it with your data.

## Usage
You can run the application with or without any options. Any option values will be reset inside the program loop after first iteration.

```
Usage: electionday [OPTIONS]

  Python prototype voting system

  Login to vote on a party and view current results. To vote you must be a
  registered voter and enter your name and voter ID.

  You can run the application with or without any options. Any option values
  will be reset inside the program loop after first iteration.

Options:
  -o, --option TEXT  Menu option selector (1, 2, 3)
  -n, --name TEXT    Name of voter
  --help             Show this message and exit.
```

### Menu Screen
```
  MAIN MENU

  1.  Login & Vote
  2.  View Results
  3.  Quit

  Select menu option:
```

### Voting Screen
```
  CAST VOTE

  1  Azorius Senate
  2  Boros Legion
  3  Dimir House
  4  Golgari Swarm
  5  Gruul Clans
  6  Izzet Leauge
  7  Orzhov Syndicate
  8  Rakdos Cult
  9  Selesnya Conclave
  10  Simic Combine

  Select a party to cast your vote.
  Enter C to cancel.
  5
  You have selected: GRUUL CLANS
  Confirm vote? Y/n y
  Thank you for voting!
  Use password "ivoted" to access current results.
  Back to main menu > 
  ```

### Results Screen
```
  CURRENT RESULTS

  Votes: 8  Azorius Senate
  Votes: 8  Boros Legion
  Votes: 6  Rakdos Cult
  Votes: 5  Golgari Swarm
  Votes: 4  Gruul Clans
  Votes: 3  Dimir House
  Votes: 3  Izzet Leauge
  Votes: 3  Orzhov Syndicate
  Votes: 2  Selesnya Conclave
  Votes: 2  Simic Combine

  Winning parties: Azorius Senate, Boros Legion

  Back to main menu >
```

## Requirements
* Python (Only tested with 3.8, may work with higher or lower versions but uses f-strings so at least 3.6)
* click
* colorama
* environs
