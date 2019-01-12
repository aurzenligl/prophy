from collections import deque
from contextlib import contextmanager
from functools import wraps

from prophyc import six

BREAKABLE_SPACE = " "


class BreakLinesByWidth(object):
    def __init__(
            self,
            max_line_width=100,
            indent_str="    ",
            block_start_token="",
            hard_indent_tail="",
            soft_indent_tail="",
            block_end_token="",
    ):
        self.max_line_width = max_line_width
        self.indent_str = indent_str
        self.hard_indent_tail = hard_indent_tail
        self.soft_indent_tail = soft_indent_tail
        self.block_start_token = block_start_token
        self.block_end_token = block_end_token

        self.indent_level = None
        self.line_abs_pos = None
        self.line_rel_pos = None
        self._markup_queue = None

    def _init(self, indent_level):
        self.indent_level = indent_level
        self.line_abs_pos = 0
        self.line_rel_pos = 0
        self._markup_queue = deque()

    def __call__(self, decorated_generator):
        @wraps(decorated_generator)
        def sub_generator(*p, **k):
            """ Is supposed to decorate a generator that:
            - yields paragraphs
            - and controls markup elements via the decorator class instance.
            """
            self._init(k.pop('indent_level', 0))

            if self.block_start_token:
                self.open_block()

            for paragraph in decorated_generator(*p, **k):
                while self._markup_queue:
                    yield self._markup_queue.popleft()

                if paragraph:
                    with self.being_a_paragraph():
                        soft_lines = paragraph.split("\n")
                        for is_not_last, soft_line in enumerate(soft_lines, 1 - len(soft_lines)):
                            for word in soft_line.split(BREAKABLE_SPACE):
                                if self.line_rel_pos > 0:
                                    if self.line_would_overflow(word):
                                        self.break_line()
                                        self.make_soft_line_indent()

                                if self.line_rel_pos > 0 or word == "":
                                    self._advance(BREAKABLE_SPACE)

                                self._advance(word)
                            if is_not_last:
                                self.break_line()
                                self.make_soft_line_indent()

            while self._markup_queue:
                yield self._markup_queue.popleft()

            if self.block_end_token:
                self.close_block()

            while self._markup_queue:
                yield self._markup_queue.popleft()

        return sub_generator

    def line_would_overflow(self, word):
        return self.line_abs_pos + len(word) >= self.max_line_width

    def make_a_bar(self, char_="=", title=""):
        assert isinstance(char_, six.string_types), "Bar character has to be a string."
        assert len(char_) == 1, "Bar character has to be a single character."
        line = "{} {} ".format(char_ * 4, title) if title else ""
        padding_width = self.max_line_width - len(line) - self._hard_indent_len
        bar = line + char_ * padding_width

        with self.being_a_paragraph():
            self._advance(bar)

    @contextmanager
    def being_a_paragraph(self):
        if not self.block_just_started:
            self.make_paragraph_indent()
        try:
            yield
        finally:
            self.break_line()

    @property
    def block_just_started(self):
        return self.line_abs_pos == self._hard_indent_len

    def break_line(self):
        self.line_abs_pos = 0
        self.line_rel_pos = 0
        self._markup_queue.append("\n")

    def _make_indent_w_tail(self, tail):
        self._advance(self._base_indent() + tail, False)

    def make_paragraph_indent(self):
        self._make_indent_w_tail(self.hard_indent_tail)

    def make_soft_line_indent(self):
        self._make_indent_w_tail(self.soft_indent_tail)

    def open_block(self):
        self._make_indent_w_tail(self.block_start_token)

    def close_block(self):
        if not self.block_just_started:
            self._make_indent_w_tail(self.block_end_token)
        else:
            self._advance(self.block_end_token, False)

    def _base_indent(self):
        return self.indent_str * self.indent_level

    @property
    def _hard_indent_len(self):
        return len(self._base_indent()) + len(self.hard_indent_tail)

    def _advance(self, text, increment_rel_pos=True):
        self.line_abs_pos += len(text)
        if increment_rel_pos:
            # intended to avoid counting indentation length
            self.line_rel_pos += len(text)
        self._markup_queue.append(text)


def split_long_string(long_string, max_line_width=80):
    lines = long_string.split("\n")
    if not any(len(line) > max_line_width for line in lines):
        for not_last, line in enumerate(lines, 1 - len(lines)):
            yield line + ("\n" if not_last else "")
    else:
        words = long_string.split(" ")
        if not any(len(word) > max_line_width for word in words):
            line, pos = "", 0
            for not_last, word in enumerate(words, 1 - len(words)):
                word += " " if not_last else ""
                line += word
                pos += len(word)
                if pos >= 80:
                    yield line
                    line, pos = "", 0
            if line:
                yield line
        else:
            pos = 0
            while pos < len(long_string):
                yield long_string[pos:pos + max_line_width]
                pos += max_line_width
