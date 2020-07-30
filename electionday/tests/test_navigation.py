import pytest

import electionday.navigation as navigation


def test_can_create_menu():
    assert navigation.Menu()


def test_menu_has_default_empty_options():
    assert navigation.Menu().options == []


def test_menu_init_sets_options():
    options = ['One', 'Two', 'Three']
    got = navigation.Menu(options=options).options
    expected = options
    assert got == expected


def test_menu_has_show_method():
    assert navigation.Menu().show() is None
