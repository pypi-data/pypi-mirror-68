from .qt import QtCore
from .qt import QtWidgets
from .qt import bind

from .widget import BaseWidget

__all__ = ['Text']

@bind(QtWidgets.QLineEdit)
class Text(BaseWidget):

    def __init__(self, value=None, *, readonly=False, clearable=False,
                 changed=None, editing_finished=None, **kwargs):
        super().__init__(**kwargs)
        self.readonly = readonly
        self.clearable = clearable
        if value is not None:
            self.value = value
        self.changed = changed
        self.editing_finished = editing_finished
        # Connect signals
        self.qt.textChanged.connect(self.__handle_changed)
        self.qt.editingFinished.connect(self.__handle_editing_finished)

    @property
    def value(self):
        return self.qt.text()

    @value.setter
    def value(self, value):
        self.qt.setText(value)

    @property
    def readonly(self):
        return self.qt.isReadOnly()

    @value.setter
    def readonly(self, value):
        self.qt.setReadOnly(value)

    @property
    def clearable(self):
        return self.qt.clearButtonEnabled()

    @clearable.setter
    def clearable(self, value):
        self.qt.setClearButtonEnabled(value)

    @property
    def changed(self):
        return self.__changed

    @changed.setter
    def changed(self, value):
        self.__changed = value

    def __handle_changed(self, text):
        if callable(self.changed):
            self.changed(text)

    @property
    def editing_finished(self):
        return self.__editing_finished

    @editing_finished.setter
    def editing_finished(self, value):
        self.__editing_finished = value

    def __handle_editing_finished(self):
        if callable(self.editing_finished):
            self.editing_finished()

    def clear(self):
        self.qt.clear()
