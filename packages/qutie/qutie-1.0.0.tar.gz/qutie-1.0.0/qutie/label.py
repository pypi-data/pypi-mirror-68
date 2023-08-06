from .qt import QtWidgets
from .qt import bind

from .frame import Frame

__all__ = ['Label']

@bind(QtWidgets.QLabel)
class Label(Frame):

    def __init__(self, text=None, *, word_wrap=None, **kwargs):
        super().__init__(**kwargs)
        if text is not None:
            self.text = text
        if word_wrap is not None:
            self.word_wrap = word_wrap

    @property
    def text(self):
        return self.qt.text()

    @text.setter
    def text(self, value):
        self.qt.setText(value)

    @property
    def word_wrap(self):
        return self.qt.wordWrap()

    @word_wrap.setter
    def word_wrap(self, value):
        self.qt.setWordWrap(value)

    @property
    def selected_text(self):
        return self.qt.selectedText()
