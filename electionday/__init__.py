from getpass import getpass
import os
import sys

from colorama import Back, Fore, Style

import electionday.config as config
import electionday.navigation as navigation
import electionday.voter as voter_model
import electionday.party as party_model
import electionday.database as db


def main():
    menu = config.MENU
    PASSWORD: str = config.PASSWORD
    error_msg: str = ''
    try:
        while True:
            clear()
            header('MAIN MENU')
            menu.view()
            if error_msg:
                print(Fore.RED, pad(error_msg),Style.RESET_ALL, sep='',
                      end='\n\n')
                error_msg = ''
            selected_option: str = get_option()
            if selected_option not in menu.selectors:
                error_msg = (f'Invalid selector ({selected_option}), please try'
                            ' again.')

            elif selected_option == '3':
                # Break out of loop to exit program.
                break

            elif selected_option == '1':
                # Prompt user for name and voter ID.
                user_name: str = prompt('Name: ')
                voter_id: str = getpass(pad('Voter ID: '))

                # Validate user.
                if not voter_model.is_valid(user_name, voter_id):
                    error_msg = 'Invalid credentials.'
                    continue

                valid_voter = voter_model.get_by_voter_id(voter_id)
                # Check if voter has voted.
                if valid_voter.has_voted:
                    error_msg = 'You have already voted.'
                    continue

                clear()
                # Display parties without votes.
                parties = party_model.select_all()
                header('CAST VOTE')
                for i, party in enumerate(parties):
                    COLOR = Fore.CYAN if i % 2 == 0 else Fore.GREEN
                    print(
                        COLOR, pad(f'{party.selector}  {party.name}'), sep='')
                print(Style.RESET_ALL)
                while True:
                    print(pad('Select a party to cast your vote.'))
                    print(pad('Enter C to cancel.'))
                    selector: str = prompt('').lower()
                    confirm_cancel: bool = False
                    if selector == 'c':
                        confirm_cancel = prompt('Return to menu? Y/n ').lower() == 'y'
                    if confirm_cancel:
                        break
                    selected_party = party_model.get_by_selector(parties, selector)
                    if selected_party is None:
                        print(pad('Invalid selection.'))
                        continue
                    print(pad(f'You have selected: {selected_party.name.upper()}'))
                    confirm_selection: bool = prompt('Confirm vote? Y/n ').lower()
                    if confirm_selection != 'y':
                        continue
                    break
                if confirm_cancel:
                    continue
                cast_vote(voter=valid_voter, party=selected_party)
                print(pad('Thank you for voting!'))
                print(pad(f'Use password "{config.PASSWORD}" to access current'
                        ' results.'))
                go_back()

            elif selected_option == '2':
                # Prompt voter for password.
                password = getpass(pad('Enter password to view results: '))
                if password != PASSWORD:
                    error_msg = 'Invalid password.'
                    continue
                clear()

                parties = party_model.select_results()
                header('CURRENT RESULTS')
                for i, party in enumerate(parties):
                    COLOR = Fore.CYAN if i % 2 == 0 else Fore.GREEN
                    print(
                        COLOR, pad(f'Votes: {party.votes}  {party.name}'),
                        sep='')
                print(Style.RESET_ALL)
                winning_parties = party_model.select_winners()
                if winning_parties[0].votes:
                    print(pad('Winning'
                            f" part{'y' if len(winning_parties) == 1 else 'ies'}:"
                            f" {', '.join(party.name for party in winning_parties)}"))
                else:
                   print(pad('No votes'))
                print()
                go_back()
        exit_program()
    except Exception as e:
        print(repr(e))
        raise e
    except KeyboardInterrupt:
        exit_program()


pad = navigation.add_padding(padding=2, direction='left')


def clear() -> None:
    """Wrapper for os.system to clear previous output.
    """
    os.system('clear')


def prompt(string: str) -> str:
    """Wrapper for padded input.

    Args:
        string (str): Input prompt string

    Returns:
        string (str): User input string
    """
    return input(pad(string))


def go_back() -> None:
    """Prompt user to return to main menu.

    Temporarily halts event loop to keep any previously output data
      visible until user chooses to return to menu.

    Returns:
        None: None
    """
    prompt('Back to main menu > ')


def get_option() -> str:
    """Prompt user to select a menu option.

    Returns:
        str: Selected option selector
    """
    return prompt('Select menu option: ')


def header(string: str) -> None:

    print('\n', pad(string), sep='', end='\n\n')


@db.connection_cursor
def cast_vote(cursor: db.sqlite3.Cursor,
              voter: voter_model.Voter,
              party: party_model.Party) -> None:
    try:
        voter_model.vote(cursor, voter)
        party_model.add_vote(cursor, party)
    except Exception as e:
        print(repr(e))
        raise e

def exit_program():
    print('\n\n', pad('Goodbye'), sep='', end='\n\n')
    db.CONNECTION.close()
    sys.exit()


if __name__ == '__main__':
    main()
