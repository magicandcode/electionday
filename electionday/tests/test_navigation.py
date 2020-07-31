import io
import sys

import pytest

import electionday.navigation as navigation


def test_can_create_menu():
    assert navigation.Menu()


def test_menu_has_default_empty_options():
    assert navigation.Menu().options == []


def test_menu_constructor_sets_options():
    options = ['One', 'Two', 'Three']
    got = navigation.Menu(options=options).options
    expected = options
    assert got == expected


def test_menu_has_show_method():
    assert navigation.Menu().show() is None


def test_menu_can_print_options(capsys):
    options = ['One', 'Two', 'Three']
    menu = navigation.Menu(options=options)
    menu.show()  # Print menu
    got = capsys.readouterr().out.strip()
    expected = all(option in got for option in options)
    assert expected


def test_menu_has_default_empty_selectors():
    assert navigation.Menu().selectors == []


def test_menu_constructor_sets_selectors():
    selectors= ['1.', '2.', '3.']
    got = navigation.Menu(selectors=selectors).selectors
    expected = selectors
    assert got == expected


def test_menu_can_print_options_with_selectors(capsys):
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    menu = navigation.Menu(options=options, selectors=selectors)
    menu.show()  # Print menu
    got = capsys.readouterr().out.strip()
    assert all(option in got for option in options)


@pytest.mark.parametrize('options, selectors, options_count', [
    (['One', 'Two', 'Three'], [1, 2, 3, 4], 3),
    (['One', 'Two', 'Three'], [1, 2, 3], 3),
    (['One', 'Two', 'Three'], [1, 2], 2),
    (['One', 'Two', 'Three'], [1], 1),
    (['One', 'Two', 'Three'], [], 3),
])
def test_menu_can_print_as_many_options_as_there_are_selectors(
        options, selectors, options_count, capsys):
    menu = navigation.Menu(options=options, selectors=selectors)
    menu.show()  # Print menu
    got = len(capsys.readouterr().out.rstrip().split('\n'))
    assert got == options_count


def test_menu_constructor_can_set_selector_punctuation(capsys):
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    punctuation = ':'
    menu = navigation.Menu(
        options=options, selectors=selectors, selector_punctuation=punctuation)
    menu.show()  # Print menu
    got = capsys.readouterr().out.count(punctuation)
    expected = len(options)
    assert got == expected


def test_menu_constructor_can_set_selector_padding(capsys):
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    padding = 5
    menu = navigation.Menu(
        options=options, selectors=selectors, selector_padding=padding)
    menu.show()  # Print menu
    got = capsys.readouterr().out
    expected = got.count(' '*padding) == len(options)
    assert expected


def test_menu_constructor_can_set_left_padding(capsys):
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    left_padding = 5
    menu = navigation.Menu(
        options=options, selectors=selectors, left_padding=left_padding)
    menu.show()  # Print menu
    got = capsys.readouterr().out.rstrip().split('\n')
    expected = all(row.startswith(' '*menu.left_padding) for row in got)
    assert expected
