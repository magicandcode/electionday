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
        self.left_padding = int(left_padding)

    def __str__(self) -> str:
        return self.get_output_string()

    def get_output_string(self) -> str:
        left_padding_string: str = ' ' * self.left_padding
        if self.selectors:
            return '\n'.join(
                f"{left_padding_string}{selector}{self.selector_punctuation}"
                f"{' '*(self.selector_padding or 1)}{option}"
                for option, selector in zip(self.options, self.selectors))
        return '\n'.join(f'{left_padding_string}{option}'
                         for option in self.options)

    def show(self):
        print(self.get_output_string())


if __name__ == "__main__":
    menu = Menu(
        ['One', 'Two', 'Three'], [1, 2, 3, 4, 5, 6], selector_padding=0,
        selector_punctuation='.', left_margin=5)
    print(menu.options)
    menu.show()
