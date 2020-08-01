import environs
import pathlib

import electionday.navigation as navigation


# Read environment variables.
env: environs.Env = environs.Env()
env.read_env()


APP_NAME: str = 'ElectionDay'
APP_SLUG: str = APP_NAME.replace(' ', '_').lower()
APP_BASE_PATH: pathlib.Path = pathlib.Path(__file__).parent
BASE_PATH: pathlib.Path = APP_BASE_PATH.parent
DATA_DIR_PATH: pathlib.Path = BASE_PATH.joinpath('data')
DATA_PATH: pathlib.Path = DATA_DIR_PATH.joinpath('data.json')
DB_PATH: pathlib.Path = DATA_DIR_PATH.joinpath(f'{APP_SLUG}.db')

options = ['Login & Vote', 'View Results', 'Quit']
selectors = [1, 2, 3]
MENU: navigation.Menu = navigation.Menu(
    options, selectors, selector_padding=2, selector_punctuation='.',
    left_padding=2,
)
PASSWORD: str = env.str('PASSWORD')
