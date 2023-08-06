import os

from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget

__all__ = ['TextArea']

@bind(QtWidgets.QTextEdit)
class TextArea(BaseWidget):

    def __init__(self, value=None, *, readonly=False, richtext=False, **kwargs):
        super().__init__(**kwargs)
        self.readonly = readonly
        self.richtext = richtext
        if value is not None:
            self.value = value

    @property
    def value(self):
        return self.qt.toPlainText()

    @value.setter
    def value(self, value):
        self.qt.setPlainText(value)

    @property
    def readoly(self):
        return self.qt.readOnly()

    @readoly.setter
    def readoly(self, value):
        self.qt.setReadOnly(value)

    @property
    def richtext(self):
        return self.qt.acceptRichText()

    @richtext.setter
    def richtext(self, value):
        self.qt.setAcceptRichText(value)

    def append(self, text):
        self.text = os.linesep.join((self.text, text))

    def insert(self, text):
        self.qt.insertPlainText(text)

    def clear(self):
        self.qt.clear()

    def select_all(self):
        self.qt.selectAll()

    def redo(self):
        self.qt.redo()

    def undo(self):
        self.qt.undo()
