from setuptools import setup

from electionday.config import APP_NAME, APP_SLUG
import electionday.database as db
from electionday.party import (
    create_table as party_table,
    populate_table as party_data
)
from electionday.voter import (
    create_table as voter_table,
    populate_table as voter_data
)


db.create_tables(party_table, voter_table)
try:
    data = db.load_data()
    parties, voters = data['parties'], data['voters']
except Exception as e:
    print(repr(e))
    raise e
else:
    db.populate_tables((party_data, parties), (voter_data, voters))
    print('Successfully created and populated database tables.')

with open('./requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [req.strip() for req in f]

setup(
    name=APP_NAME,
    py_modules=[APP_SLUG],

    install_requires=requirements,
    entry_points=f'''
        [console_scripts]
        {APP_SLUG}={APP_SLUG}:main
    ''',
)
