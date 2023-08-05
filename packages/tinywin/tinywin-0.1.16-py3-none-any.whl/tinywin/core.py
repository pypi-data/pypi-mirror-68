import curses

from tinywin import helpers

class PaneError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class Init(object):
    def __init__(self):
        pass

    def init(self):
        pass

class Processable(object):
    def __init__(self):    
        super(Processable, self).__init__()

    def process(self, time):
        pass

    def key_input(self, ie):
        return ie

class Drawable(Processable):
    def __init__(self, win=None):
        super(Drawable, self).__init__()
        self._win = win
        self._calc_win_coords()
        self._needs_drawing = True
        self.win_has_been_assigned = False

        self.awaiting_window_update = True

    def assign_win(self, win):
        self._win = win
        self._calc_win_coords()
        self.needs_drawing()
        self.win_has_been_assigned = True
        self.awaiting_window_update = False

    def window_size_update(self):
        pass

    def get_awaiting_window_update(self):
        return self.awaiting_window_update

    def _calc_win_coords(self):
        if self._win is not None:
            self._h, self._w = self._win.getmaxyx()
        else:
            self._h = None
            self._w = None

    def process(self, time):
        super(Drawable, self).process(time)

    def draw(self):
        if self._needs_drawing:
            self._refresh()

    def resize(self, nlines, ncols):
        if win is not None:
            win.resize(nlines, ncols)
        self.needs_drawing()

    def needs_drawing(self):
        self._needs_drawing = True

    def get_needs_drawing(self):
        return self._needs_drawing

    def _refresh(self):
        self._win.refresh()
        self._needs_drawing = False

    def key_input(self, ie):
        return ie

class Pane(Drawable):
    def __init__(self, stdscr, win=None, line_counter=0, title=''):
        super(Pane, self).__init__(win=win)
        self._stdscr = stdscr
        self._memory = {}
        self._focus = False
        self.line_counter = line_counter
        self.border_width_reduction = 4
        self.border_height_reduction = 2
        self._title = title

    def assign_win(self, win):
        super(Pane, self).assign_win(win)

    def window_size_update(self):
        super(Pane, self).window_size_update()

    def process(self, time):
        super(Pane, self).process(time)

    def draw(self):
        super(Pane, self).draw()

    def resize(self, nlines, ncols):
        super(Pane, self).resize(nlines, ncols)

    def add_focus_cursor_data(self, data):
        self.focus_cursor_data = data

    def needs_drawing(self):
        super(Pane, self).needs_drawing()

    def get_needs_drawing(self):
        return super(Pane, self).get_needs_drawing()


    def focus(self):
        self._focus = True
        self.needs_drawing()

    def unfocus(self):
        self._focus = False
        self.needs_drawing()

    def get_focus(self):
        return self._focus

    def set_title(self, title):
        self._title = title

    def get_title(self):
        return self._title

    def clear(self):
        if self._win is not None:
            self._win.clear()

    def _refresh(self):
        super(Pane, self)._refresh()

    def init_frame(self, title='', clear_interior=True, border_color=None, unfocused_line_color=None, single_line=False, omit_border=False, single_line_x=0, single_line_y=0):
        if not single_line:
            self.omit_border = omit_border
            self.draw_top_border(title, omit_side_borders=omit_border, border_color=border_color, unfocused_line_color=unfocused_line_color)
            if not self.omit_border:
                for i in range(1, self._h-2):
                    self.draw_line_border(focused_line_color=border_color, reset_line=clear_interior, unfocused_line_color=unfocused_line_color, line=i)
                self.draw_bottom_border(focused_line_color=border_color, unfocused_line_color=unfocused_line_color)
                self.line_counter = 1
        else:
            self.line_counter = 0
            self._win.move(single_line_y, single_line_x)
            self._win.clrtoeol()

    def draw_line_border(self, focused_line_color=None, unfocused_line_color=None, reset_line=True, line=None):
        if focused_line_color is None:
            focused_line_color = curses.color_pair(1)  # Default
        if unfocused_line_color is None:
            unfocused_line_color = focused_line_color
        if line is None:
            line = self.line_counter
        # if reset_line:
        #     self._win.move(line, 0)
        #     self._win.clrtoeol()
        if self._focus:
            self._win.addstr(line, 0, '│', focused_line_color)  # Default
            self._win.addstr(line, self._w-1, '│', focused_line_color)  # Default
        else:
            self._win.addstr(line, 0, '│', unfocused_line_color)
            self._win.addstr(line, self._w-1, '│', unfocused_line_color)

    def key_input(self, input_event):
        # if not self._focus:
        #     return input_event
        # if input_event.key == curses.KEY_MOUSE:
        #     try:
        #         _, self._mx, self._my, _, _ = input_event.getmouse()
        #         # if self._win.enclose(self._my, self._mx):
        #         #     self.focus()
        #         # else:
        #         #     self.unfocus()
        #     except curses.error as e:
        #         pass
        #     input_event.absorb()
        return input_event

    def draw_top_border(self, _title, focused_title_color=None, omit_side_borders=False, border_color=None, unfocused_line_color=None):
        self._win.move(0, 0)
        self._win.clrtoeol()
        if omit_side_borders:
            helpers.title(self._win, 0, _title, self._focus, unfocused_line_color=unfocused_line_color, focused_line_color=border_color, focused_title_color=focused_title_color, omit_side_borders=True)
        else:
            helpers.title(self._win, 0, _title, self._focus, focused_title_color=focused_title_color, focused_line_color=border_color, unfocused_line_color=unfocused_line_color, omit_side_borders=False)

    def draw_bottom_border(self, focused_line_color=None, unfocused_line_color=None):
        if focused_line_color is None:
            focused_line_color = curses.color_pair(1)  # Default
        if unfocused_line_color is None:
            unfocused_line_color = focused_line_color
        self._win.move(self._h - 2, 0)
        self._win.clrtoeol()
        if self._focus:
            self._win.addstr(self._h - 2, 0, '└' + ''.center(self._w-2, '─') + '┘', focused_line_color)
        else:
            self._win.addstr(self._h - 2, 0, '└' + ''.center(self._w-2, '─') + '┘', unfocused_line_color)

    def _addstr_text_line(self, y, x, text_line):
        text_line.output_to_window(self._win, y, x)

    def addstr_auto(self, x, string, color=None, inc=True):
        if isinstance(string, Text_Line):
            self._addstr_text_line(self.line_counter, x, string)
        else:
            if color is None:
                color = curses.color_pair(1)
            self._win.addstr(self.line_counter, x + 2, string, color)  # Move over one place to make space for the border
        if inc:
            self.line_counter = self.line_counter + 1

    def addstr(self, y, x, string, color=None):
        if isinstance(string, Text_Line):
            self._addstr_text_line(y, x, string)
        else:
            if color is None:
                color = curses.color_pair(1)
            self._win.addstr(y, x + 2, string, color)  # Move over one place to make space for the border

    def inc(self):
        self.line_counter = self.line_counter + 1

    def reset_line_counter(self):
        self.line_counter = 0

class Pane_Holder(Processable):
    def __init__(self, pane, start_x, start_y, width, height, can_be_focused=True, focus_key=None, one_line=False, fixed_to=None, unfocus_callback=None):
        self._pane = pane
        self._start_x = start_x
        self._start_y = start_y
        self._width = width
        self._height = height
        self._can_be_focused = can_be_focused
        self._focus_key = ord(focus_key) if focus_key is not None else None
        self._one_line = one_line
        self._unfocus_callback = unfocus_callback
        self._fixed_to = fixed_to


    def get_coords(self):
        return (self._start_x, self._start_y, self._width, self._height)

    def get_is_one_line(self):
        return self._one_line

    def get_is_fixed_to(self):
        return self._fixed_to

    def link_win(self, win):
        self._pane.assign_win(win)
        self._win = win

    def move_win(self, begin_y, begin_x):
        self._win.mvwin(begin_y, begin_x)

    def resize_win(self, nlines, ncols):
        self._win.resize(nlines, ncols)

    def refresh_assign_win(self):
        self._pane.assign_win(self._win)

    def get_pane(self):
        return self._pane

    def can_be_focused(self):
        return self._can_be_focused

    def key_input(self, ie):
        if ie is not None and self._focus_key is not None and ie.key == self._focus_key:
            if self._unfocus_callback is not None:
                self._unfocus_callback()
            self._pane.focus()
            ie.absorb()
        return ie

class Text_Wrapper(object):
    def __init__(self, text, color):
        self.text = text
        self.color = color

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text

    def copy(self):
        return Text_Wrapper(self.text, self.color)

class Text_Line(object):
    """Text_Line

    This class is a wrapper for strings that allows color information to be associated. They can be used in
    most cases a regular string can be used, and with regards to this library, are interchangable with
    strings.

    Each Text_Line should represent a single line of data to be printed to the screen. Many blocks of colored
    strings can be contained in a single Text_Line, and Text_Lines can be added together to merge their data.

    On initialization, strings and colors should be passed in as arguments:
        tl = Text_Line('This is color 1,', curses.color_pair(1), ' but this part is color 2.', curses.color_pair(2))

    Named Arguments:
        data:           Data to be associated with this line of data. Useful for lists of data. [None]
        ellipsis_color: Color of the ellipsis at the end of a shortened Text_Line. [None (default color)]
        ellipsis_text:  Text to serve ellipsis purpose at the end of a shortened Text_Line. ['...']
        allowed_width:  Width allocated for this Text_Line. A value will force the Text_Line to shorten to the 
                        specified value. [None (no shortening)]

    User Functions:
        get_data():                  Gets the data dictionary associated with this Text_Line
        set_data(data):              Sets the data to be associated with this Text_Line
        output_to_window(win, y, x): Requests the Text_Line to draw to the specified window at the coords specified.
        uniform_color(color):        Sets all text in the Text_Line to the same, specified color.
        get_has_been_shortened():    Gets whether or not this text has been shortened.
        shorten_to_length(length):   Requests the Text_Line to shorten its contents to fit the specified length.

    Operators:
        __len__: len(text_line): Length of a Text_Line is the length of characters of the text stored within. Color 
                                 has no effect on the returned length.
        __str__: str(text_line): Text_Lines can be converted to string, which will strip color info and output the raw
                                 text stored within.
        __add__: text_line1 + text_line2  || 'string' + text_line || text_line + 'string': Text_Lines can be added to
                                 eachother, and to other objects. If both objects are Text_Lines, a new Text_Line will
                                 be returned. If the first object is a Text_Line, a new Text_Line will be returned. If
                                 the first object is not a Text_Line, the Text_Line object will be treated as a string
                                 with regards to the add.
    """
    def __init__(self, *args, data=None, ellipsis_color=None, ellipsis_text='...', allowed_width=None):
        self.data = data
        self._has_been_shortened = False
        if self.data is None:
            self.data = dict()
        if ellipsis_color is None:
            try:
                self._ellipsis_color = curses.color_pair(2)
            except curses.error:
                self._ellipsis_color = None
        else:
            self._ellipsis_color = ellipsis_color
        self._ellipsis_text = ellipsis_text
        texts = []
        colors = []
        current_arg_is_text = True
        for arg in args:
            if current_arg_is_text:
                if isinstance(arg, Text_Line):
                    texts.append(str(arg))
                else:
                    texts.append(arg)
            else:
                colors.append(arg)
            current_arg_is_text = not current_arg_is_text

        # if len(texts) != len(colors):


        self._text_objects = []
        self._shortened_text_objects = []

        for i in range(0, len(texts)):
            self._text_objects.append(Text_Wrapper(texts[i], colors[i]))

        if allowed_width is None:
            self._allowed_width = 0
            for t in self._text_objects:
                self._allowed_width = self._allowed_width + len(t)
        else:
            self._allowed_width = allowed_width

        self._shortened_text_objects = self._text_objects

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data.copy()
        return self

    def set_allowed_width(self, width):
        self._allowed_width = width
        return self

    def get_text_component(self, index):
        return self._text_objects[index]

    def output_to_window(self, win, line_counter, x_offset, highlight=0):
        try:
            len_counter = 0
            for t in self._shortened_text_objects:
                if t.color is None:
                    win.addstr(line_counter, len_counter + x_offset, t.text)
                else:
                    if not highlight:
                        win.addstr(line_counter, len_counter + x_offset, t.text, t.color)
                    else:
                        win.addstr(line_counter, len_counter + x_offset, t.text, t.color | highlight)
                len_counter = len_counter + len(t)
            if highlight:
                win.addstr(line_counter, len_counter + x_offset, ' '*(self._allowed_width - len_counter - x_offset - 3), highlight)
            return len_counter
        except curses.error:
            pass

    def uniform_color(self, color):
        for t in self._text_objects:
            t.color = color

        for t in self._shortened_text_objects:
            t.color = color

        return self

    def get_has_been_shortened(self):
        return self._has_been_shortened

    def shorten_to_length(self, length):
        self._allowed_width = length
        self._has_been_shortened = True
        tmp_shortened_text_objects = []
        for t in self._text_objects:
            tmp_shortened_text_objects.append(t.copy())
        total_len = 0
        for t in tmp_shortened_text_objects:
            total_len = total_len + len(t)
        if total_len > length:
            self._shortened_text_objects = []
            # print(total_len, length)
            index = len(tmp_shortened_text_objects) - 1  # Start at the end of the colored string
            character_index = len(tmp_shortened_text_objects[index])-1  # Start at the last character in the last string
            removing = True

            while removing is True:
                total_len = total_len - 1
                character_index = character_index - 1
                if character_index < 0:
                    index = index - 1
                    if index < 0:
                        raise TerminalTooSmallError(f'Cannot shorten text "{self.__str__(use_unshortened_text=True)}" to length "{length}"')
                    character_index = len(tmp_shortened_text_objects[index])-1
                if total_len + len(self._ellipsis_text) <= length:
                    removing = False

            # We can use all text up to index, and the last piece of text can be used up to the character_index

            tmp_shortened_text_objects[index].text = tmp_shortened_text_objects[index].text[0:character_index+1]  # Shorten last index text
            if tmp_shortened_text_objects[index].text[len(tmp_shortened_text_objects[index].text)-1] == ' ':  # Trim a space if one exists
                tmp_shortened_text_objects[index].text = tmp_shortened_text_objects[index].text[:-1]

            for i in range(0, index+1):
                self._shortened_text_objects.append(tmp_shortened_text_objects[i])
            self._shortened_text_objects.append(Text_Wrapper(self._ellipsis_text, self._ellipsis_color))
        return self

    def __len__(self, use_unshortened_text=False):
        counter = 0
        if use_unshortened_text is True:
            for t in self._text_objects:
                counter = counter + len(t)
        else:
            for t in self._shortened_text_objects:
                counter = counter + len(t)
        return counter

    def __add__(self, o):
        if isinstance(o, Text_Line):
            left_side = self
            right_side = o

            l_objs = left_side._text_objects
            r_objs = right_side._text_objects

            total_args = []

            for l in l_objs:
                total_args.append(l.text)
                total_args.append(l.color)
            for l in r_objs:
                total_args.append(l.text)
                total_args.append(l.color)

            return Text_Line(*total_args, data=left_side.data, ellipsis_color=left_side._ellipsis_color)
        else:
            left_side = self
            right_side = o

            l_objs = left_side._text_objects

            total_args = []

            for l in l_objs:
                total_args.append(l.text)
                total_args.append(l.color)

            total_args.append(right_side)
            total_args.append(None)

            return Text_Line(*total_args, data=left_side.data, ellipsis_color=left_side._ellipsis_color)

    def __radd__(self, o):
        if isinstance(o, Text_Line):
            left_side = o
            right_side = self

            l_objs = left_side._text_objects
            r_objs = right_side._text_objects

            total_args = []

            for l in l_objs:
                total_args.append(l.text)
                total_args.append(l.color)
            for l in r_objs:
                total_args.append(l.text)
                total_args.append(l.color)

            return Text_Line(*total_args, data=left_side.data, ellipsis_color=left_side._ellipsis_color)
        else:
            return o + self.__str__()

    def __str__(self, use_unshortened_text=False):
        string = ''
        if use_unshortened_text is True:
            for t in self._text_objects:
                string = string + t.text
        else:
            for t in self._shortened_text_objects:
                string = string + t.text
        return string

class TerminalTooSmallError(PaneError):
    def __init__(self, msg='Terminal too small for application'):
        super(TerminalTooSmallError, self).__init__(msg)

class Menu_Item(object):
    def __init__(self, text, callback, hotkey=None, underline_char=-1, disabled=False):
        self.text = text
        self.callback = callback
        self._x = 0
        self._y = 0
        self._selected = False
        self._hotkey = hotkey
        self._hotkey_ord = ord(hotkey) if hotkey is not None else None
        self._underline_char = underline_char
        self._disabled = disabled

        if underline_char != -1:
            self._underline_char_before = self.text[0:self._underline_char]
            self._underline_char_underline = self.text[self._underline_char:self._underline_char+1]
            self._underline_char_after = self.text[self._underline_char+1:]
            if self._hotkey is not None:
                self._underline_char_after = self._underline_char_after + f' ({self._hotkey})'

        if self._hotkey is not None:
            self.text = self.text + f' ({self._hotkey})'

    def set_center(self, x, y):
        self._x = x
        self._y = y

    def set_disabled(self, val):
        self._disabled = val

    def get_disabled(self):
        return self._disabled

    def key_input(self, input_event):
        if self._hotkey_ord is not None and input_event.key == self._hotkey_ord:
            if self.click():
                input_event.absorb()

        return input_event

    def click(self):
        if self.callback is not None and not self._disabled:
            self.callback()
            return True
        return False

    def select(self, val=True):
        self._selected = val

    def get_center(self):
        return (self._x, self._y)

    def get_left_corner(self):
        return (self._x - math.ceil(len(self.text)), self._y)

    def draw(self, win):
        (x, y) = self.get_left_corner()
        color = curses.color_pair(1)  # Default
        if self._disabled:
            color = curses.color_pair(2)  # Dim default
        if self._selected:
            win.addstr(y, x, self.text, color | curses.A_UNDERLINE)
        else:
            if self._underline_char != -1:
                win.addstr(y, x, self._underline_char_before, color)
                win.addstr(y, x + len(self._underline_char_before), self._underline_char_underline, color | curses.A_UNDERLINE)
                win.addstr(y, x + len(self._underline_char_before) + len(self._underline_char_underline), self._underline_char_after, color)
            else:
                win.addstr(y, x, self.text, color)

class Loading_Bar(object):
    def __init__(self, base_message, width, allocate_message_width=None):
        if not isinstance(base_message, Text_Line):
            base_message = Text_Line(base_message, curses.color_pair(1))
        self._base_message = base_message
        if allocate_message_width is None:
            self._base_message_length = len(self._base_message)
        else:
            self._base_message_length = allocate_message_width
            self._base_message.shorten_to_length(self._base_message_length)
        self._message = self._base_message
        self._w = width
        self._fraction_done = 0

    def set(self, fraction_done, new_message=None):
        self._fraction_done = fraction_done
        if self._fraction_done > 1:
            self._fraction_done = 1
        elif self._fraction_done < 0:
            self._fraction_done = 0

        if new_message is not None:
            if not isinstance(new_message, Text_Line):
                new_message = Text_Line(new_message, curses.color_pair(1))
            self._message = new_message
            self._message.shorten_to_length(self._base_message_length)

    def get_text(self):
        bar_len = self._w - self._base_message_length - 8
        if bar_len < 2:
            return Text_Line(
                self._message, curses.color_pair(1),
                ('{:.0%}'.format(self._fraction_done)).ljust(4, ' '), curses.color_pair(1)
            )
        else:
            msg = self._message
            num_filled = math.floor(bar_len * self._fraction_done)
            num_not_filled = bar_len - num_filled
            # bar = '[' + ('━' * num_filled) + (' ' * num_not_filled) + ']'
            # return ('{:.0%}'.format(self._fraction_done)).rjust(4, ' ') + bar + ' ' + msg
            if self._fraction_done == 1:
                precent_color = curses.color_pair(9)
            else:
                precent_color = curses.color_pair(5)
            return Text_Line(
                ('{:.0%}'.format(self._fraction_done)).rjust(4, ' '), precent_color,
                '[', curses.color_pair(1),
                ('━' * num_filled), curses.color_pair(1),
                ('━' * num_not_filled), curses.color_pair(2),
                '] ', curses.color_pair(1),
                msg, curses.color_pair(1)
            )
