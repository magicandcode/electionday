from typing import Callable


def add_padding(padding: int, direction: str = 'both') -> Callable:
    """Add padding on both or either side of a string using blank
      spaces.

    Args:
        padding (int): Size of padding (number of blank spaces)
        direction (str, optional): Which side to pad. Defaults to 'both'.

    Returns:
        Callable: Wrapper function taking the string to pad
    """
    direction = direction.lower()

    def wrapper(string: str) -> str:
        """Wrapper function, takes the string to pad as argument.

        Args:
            string (str): String to pad

        Returns:
            str: Padded string
        """
        if direction == 'left':
            return ' '*padding  + string
        elif direction == 'right':
            return string + padding*' '
        else:
            return ' '*padding + string + ' '*padding
    return wrapper


class Menu:

    def __init__(self,
                 options = None,
                 selectors = None,
                 selector_padding: int = 2,
                 selector_punctuation: str = '.',
                 left_padding: int = 0,
    ):
        if options is None:
            options = []
        self.options = [str(option) for option in options]
        if selectors is None:
            selectors = []
        self.selectors = [str(selector) for selector in selectors]
        self.selector_padding: int = abs(selector_padding) or 2
        self.selector_punctuation: str = str(selector_punctuation)
        self._left_padding = int(left_padding)
        self.pad = add_padding(self.left_padding, 'left')

    def __str__(self) -> str:
        if self.selectors:
            return '\n'.join(
                self.pad(f"{selector}{self.selector_punctuation}"
                f"{' '*(self.selector_padding or 1)}{option}")
                for option, selector in zip(self.options, self.selectors))
        return '\n'.join(self.pad(option)
                         for option in self.options)

    @property
    def left_padding(self) -> int:
        return self._left_padding

    @left_padding.setter
    def left_padding(self, value: int) -> None:
        self._left_padding = int(value)
        self.pad = add_padding(self.left_padding, 'left')

    @property
    def layout(self) -> str:
        return str(self)

    def view(self) -> None:
        print('', self.layout, sep='', end='\n\n')


if __name__ == "__main__":
    menu = Menu(
        ['One', 'Two', 'Three'], [1, 2, 3, 4, 5, 6], selector_padding=0,
        selector_punctuation='.', left_margin=5)
    print(menu.options)
    menu.view()
