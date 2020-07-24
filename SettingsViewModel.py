from PySide2 import QtCore

from TodosViewModel import TodosViewModel

class SettingsViewModel(QtCore.QObject):
  todos_reference_changed = QtCore.Signal()
  todo_count_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)

    self.__todos_reference = None
  
  def get_todo_count(self):
    if self.__todos_reference:
      return len(self.__todos_reference.todos)
    
    return 0

  def get_todos_reference(self):
    return self.__todos_reference

  def set_todos_reference(self, value):
    # Only change the view model if there is a new one (don't reload when closing the app)
    if value:
      self.__todos_reference = value
      self.todos_reference_changed.emit()

      # Connect signal in TodosViewModel
      self.__todos_reference.todo_count_changed.connect(lambda: self.todo_count_changed.emit())

  @QtCore.Slot()
  def clearTodos(self):
    self.__todos_reference.clear_todos()

  todosReference = QtCore.Property(TodosViewModel, get_todos_reference, set_todos_reference, notify=todos_reference_changed)
  todoCount = QtCore.Property(int, get_todo_count, notify=todo_count_changed)