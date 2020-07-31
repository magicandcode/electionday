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


def test_menu_has_get_output_string_method():
    assert isinstance(navigation.Menu().layout, str)


def test_menu_can_get_output_string_with_options():
    options = ['One', 'Two', 'Three']
    menu = navigation.Menu(options=options)
    got = menu.layout
    expected = all(option in got for option in options)
    assert expected


def test_menu_has_default_empty_selectors():
    assert navigation.Menu().selectors == []


def test_menu_constructor_sets_selectors():
    selectors= ['1.', '2.', '3.']
    got = navigation.Menu(selectors=selectors).selectors
    expected = selectors
    assert got == expected


def test_menu_can_get_output_string_with_options_and_selectors():
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    menu = navigation.Menu(options=options, selectors=selectors)
    got = menu.layout
    assert all(option in got for option in options)


@pytest.mark.parametrize('options, selectors, options_count', [
    (['One', 'Two', 'Three'], [1, 2, 3, 4], 3),
    (['One', 'Two', 'Three'], [1, 2, 3], 3),
    (['One', 'Two', 'Three'], [1, 2], 2),
    (['One', 'Two', 'Three'], [1], 1),
    (['One', 'Two', 'Three'], [], 3),
])
def test_menu_can_print_as_many_options_as_there_are_selectors(
        options, selectors, options_count):
    menu = navigation.Menu(options=options, selectors=selectors)
    got = len(menu.layout.split('\n'))
    assert got == options_count


def test_menu_constructor_can_set_selector_punctuation():
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    punctuation = ':'
    menu = navigation.Menu(
        options=options, selectors=selectors, selector_punctuation=punctuation)
    got = menu.layout.count(punctuation)
    expected = len(options)
    assert got == expected


def test_menu_constructor_can_set_selector_padding():
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    padding = 5
    menu = navigation.Menu(
        options=options, selectors=selectors, selector_padding=padding)
    got = menu.layout.count(' '*padding)
    expected = len(options)
    assert got == expected


def test_menu_constructor_can_set_left_padding():
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    left_padding = 5
    menu = navigation.Menu(
        options=options, selectors=selectors, left_padding=left_padding)
    got = all(row.startswith(' '*menu.left_padding)
              for row in menu.layout.split('\n'))
    expected = True
    assert got == expected


def test_menu_has_view_method():
    assert navigation.Menu().view() is None


@pytest.mark.parametrize('options, selectors', [
    (['One', 'Two', 'Three'], [1, 2, 3, 4]),
    (['One', 'Two', 'Three'], [1, 2, 3]),
    (['One', 'Two', 'Three'], [1, 2]),
    (['One', 'Two', 'Three'], [1]),
    (['One', 'Two', 'Three'], []),
])
def test_str_of_menu_is_layout_string(options, selectors):
    menu = navigation.Menu(options=options, selectors=selectors)
    got = str(menu)
    expected = menu.layout
    assert got == expected


@pytest.mark.parametrize('options, selectors, options_count', [
    (['One', 'Two', 'Three'], [1, 2, 3, 4], 3),
    (['One', 'Two', 'Three'], [1, 2, 3], 3),
    (['One', 'Two', 'Three'], [1, 2], 2),
    (['One', 'Two', 'Three'], [1], 1),
    (['One', 'Two', 'Three'], [], 3),
])
def test_menu_can_print_as_string_with_view_method(
        options, selectors, options_count, capsys):
    menu = navigation.Menu(options=options, selectors=selectors)
    menu.view()
    got = capsys.readouterr().out.rstrip()
    expected = str(menu)
    assert got == expected


def test_menu_layout_property_returns_menu_as_string():
    options, selectors = ['One', 'Two', 'Three'], [1, 2, 3]
    menu = navigation.Menu(options=options, selectors=selectors)
    got = menu.layout
    expected = str(menu)
    assert got == expected


def test_navigation_has_add_padding_closure():
    pad = navigation.add_padding(4)
    assert pad('hello') == '    hello    '


def test_add_padding_left():
    pad = navigation.add_padding(4, 'LEFT')
    assert pad('hello') == '    hello'


def test_add_padding_right():
    pad = navigation.add_padding(4, 'RIGHT')
    assert pad('hello') == 'hello    '
