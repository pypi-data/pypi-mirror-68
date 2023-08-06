''' 
megabar is python module which can be used to create fun progress bar
objects by using only ASCII characters; coded by dAriush
'''


class MegaBar:
    ''' 
    MegaBar is suitable for consoles which doesn't support
    carriage return character "\r" such as IDLE. 
    '''

    def __init__(self,
                 iterable_object,
                 task_name='',
                 bar_width=60,
                 color=None):
        '''__init__ MegaBar class constructor

        Parameters
        ----------
        iterable_object : like list, tuple, strings
            this is the same iterable object that will be used in for loop
        task_name : str, optional
            progress title, by default ''
        bar_width : int, optional
            width of the bar, by default 40
        color : str, optional
        '''
        import os

        self.colors = {
            'BLACK': '\033[30m',
            'RED': '\033[31m',
            'GREEN': '\033[32m',
            'YELLOW': '\033[33m',
            'BLUE': '\033[34m',
            'MAGENTA': '\033[35m',
            'CYAN': '\033[36m',
            'WHITE': '\033[37m',
            'RESET': '\033[0m'
        }

        self.emojis = [
            '\m/_(>_<)_\m/',
            '\m/ (>.<) \m/',
            '\,,/(^_^)\,,/',
            '\(^-^)/',
            '( 0 _ 0 )',
            'd[-_-]b',
            '<(^_^)>',
            '¯\(°_o)/¯',
            '[¬º-°]¬',
        ]

        self.opening_character = '▌'
        self.closing_character = '▐'
        self.top_margin_character = '▄'
        self.bottom_margin_character = '▀'
        self.progress_character = '█'

        if color != None:
            if type(color) != str:
                raise TypeError('Pass color as str object')

            if color.upper() not in self.colors:
                raise ValueError('Invalid color name')

            os.system("")  # allows you to print ANSI codes in the Terminal
            self._color = color.upper()
            print(self.colors[self._color], end="", flush=True)

        else:
            self._color = None

        self.iterable_object = iterable_object
        self.iterations_number = len(iterable_object)
        self.task_name = (str(task_name)).strip()
        self.bar_width = int(bar_width)
        # number of printed characters in each step
        self.step = int(self.bar_width / self.steps_number)

        # MegaBar need a list of desired values in iterable_object to
        # excute a progress step; this list defined as progress_points
        self.progress_points = [
            int(j * (self.iterations_number / self.steps_number))
            for j in range(0, self.steps_number)
        ]

        # The elapsed_steps attribute is a counter for passed steps
        self.elapsed_steps = 0

        # Header and footer Construction
        #
        # Header of the MegaBar has two part, emoji and title
        # by default 0.4 of bar width allocated to emoji and remained
        # 0.6 of bar width allocated to title which is formated form
        # of task_name
        emoji_width = int(self.bar_width * 0.4) - 1  # -1 for opening character
        title_width = int(self.bar_width * 0.6) - 1  # -1 for ending character
        emoji = f'{self.get_random_emoji(): ^{emoji_width}s}'
        title = f'{self.task_name: ^{title_width}s}'
        top_box = self.top_margin_character * self.bar_width
        self.header = '{0}\n{1}{2}{3}{4}'.format(
            top_box, self.opening_character, emoji, title, self.closing_character)

    @property
    def steps_number(self):
        # In case of changing bar width steps number still will be valid
        return self.bar_width - 2

    def get_random_emoji(self):
        '''returning random emoji'''
        from random import randint
        random_emoji = self.emojis[randint(0, len(self.emojis) - 1)]
        return random_emoji

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, user_color_choice):
        import os
        if user_color_choice != None:
            if type(user_color_choice) != str:
                raise TypeError('Pass color as str object')

            if self._color != None:
                if user_color_choice.upper() not in self.colors:
                    raise ValueError('Invalid color name')

                self._color = user_color_choice.upper()
                print(self.colors[self._color], end="", flush=True)

            else:
                if user_color_choice.upper() not in self.colors:
                    raise ValueError('Invalid color name')

                os.system("")  # allows you to print ANSI codes in the Terminal
                self._color = user_color_choice.upper()
                print(self.colors[self._color], end="", flush=True)

        else:
            if self._color != None:
                self._color = None
                print(self.colors['RESET'], end="", flush=True)

    def start(self):
        import time
        self.start_time = time.perf_counter()
        print(f'{self.header}', flush=True)
        print(self.opening_character, end="", flush=True)

    def middle(self, i):
        # in folowing if block program determines when to pass one step
        if i in self.progress_points:
            print(self.progress_character * (self.step), end="", flush=True)
            self.elapsed_steps += 1

    def end(self):
        import time
        self.stop_time = time.perf_counter()
        self.elapsed_time = self.stop_time - self.start_time
        formated_elapsed_time = time.strftime("%M:%S",
                                              time.gmtime(self.elapsed_time))
        elapsed_time_string = f'Elapsed time: {formated_elapsed_time}'
        footer_time_section = '{0}{1: >{2}s}{3}'.format(self.opening_character,
                                                        elapsed_time_string, (
                                                            self.bar_width-2),
                                                        self.closing_character)
        bottom_box = self.bottom_margin_character * self.bar_width
        footer = footer_time_section + '\n' + bottom_box

        # It is possible that elapsed steps do not reach desired steps
        # number this is mostly because of integer conversion of
        # progress points
        # This problem can be solved by using elapsed_steps counter,
        # at the end of progress remaining characters will have calculated
        # and printed

        # -2 for opening and ending characters
        remained_character = self.bar_width - self.elapsed_steps * self.step - 2
        print(self.progress_character * remained_character +
              self.closing_character, flush=True)

        print(footer, flush=True)

        # Resetting color of terminal
        if self.color != None:
            print(self.colors['RESET'], end='', flush=True)

    def run(self):
        self.start()

        for counter, item in enumerate(self.iterable_object):
            yield item
            self.middle(counter)

        self.end()


def mega_bar(iterable_object, title='', bar_width=60, color=None):
    """just wrap for loop sequence with mega_bar

    Parameters
    ----------
    iterable_object : any iterable object
        this is what you want to pass to the for loop
    title : str, optional
        bar title, by default ''
    bar_width : int, optional
        by default 40
    color : str, optional
        by default None

    Returns
    -------
    items in iterable_objects
        a generator which returns items in iterable_objects
    """
    bar = MegaBar(iterable_object, task_name=title,
                  bar_width=bar_width, color=color)
    return bar.run()
