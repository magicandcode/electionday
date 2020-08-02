# ElectionDay
### Simple (and insecure!) Python voting system prototype application.

Final project submission.

Login to vote on a party and view current results. To vote you must be a registered voter and enter your name and voter ID.


## Installation
First you need to rename `data/sample-data.json` to `data.json` (or change the path in `electionday/config.py`).

Also rename `.sample-env` to `.env` and set `PASSWORD` required to view results.

It is strongly recommended that you run the application in its own virtual environment.


### Virtual Environment - Unix (MacOS/Linux)
You may have to use `python3` instead of `python`, check your Python version with `python -V` and `python3 -V` and use the latest version (see Requirements).
```
python3 -m venv venv
```
This creates a virtual environment in a new dir `venv/` inside the project repo. It will not be tracked by Git.
Activate the environment:
```
. venv/bin/activate
```
You should now see `(venv)` in the prompt.
Once you've activated your virtual environemnt you install the application and its
dependencies using Pip:
```
pip install -e .
```
Note that you need to be inside the project repo root dir.
This will create the database and populate it with your data.


### Virtual Environment - Windows
Create virtual environment:
```
python -m venv venv
```
> If you get an error saying you don't have permission, make sure there is no `venv` dir already. This error may occur even if you've removed a previous virtual environemnt directory so update the Explorer window or run `dir` to make sure `venv` doesn't exist before you start searching for another solution.

Once you've created your virtual environment you need to activate it. Depending on which shell you're using the command differs slightly.

#### Cmd
```
venv\Scripts\activate.bat
```

#### Powershell
```
venv\Scripts\activate.ps1
```
You should now see `(venv)` in the prompt.
Once you've activated your virtual environment you install the application and its
dependencies using Pip:
```
pip install -e .
```
Note that you need to be inside the project repo root dir.
This will create the database and populate it with your data.

> If you encounter an error with `null character` or `encoding` in the message you may need to change the value of `ENCODING` in `electionday/config.py`.

> If there are any import issues, try running pip or a Python script as a Python module:
> ```
> python -m pip <options>
> ```
> ```
> python -m module_name_without_dot_py
> ```


## Usage
To run the application as a Python script you need to install dependencies and create the database manually.
Start by installing dependencies in `requirements.txt`:
```
pip install -r requirements.txt
```

Then create and populate the database:
```
python -m setup_db
```

Finally run the application as a script (cannot be run as a module since it has the same name as the package):
```
python electionday.py
```

While it's possible to run the application as a script, the preferred way is to install it with Pip and run as a commandline application.

You can run the application with or without any options. Any command line option values will be reset inside the program loop after the first iteration.

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
