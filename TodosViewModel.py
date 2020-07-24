from PySide2 import QtCore

from models import Todo

class TodosViewModel(QtCore.QObject):
  is_valid_changed = QtCore.Signal()
  new_todo_name_changed = QtCore.Signal()
  todo_count_changed = QtCore.Signal()

  def __init__(self):
    QtCore.QObject.__init__(self)
  
    self.__new_todo_name = ''
    self.todos = []

  def get_new_todo_name(self):
    return self.__new_todo_name
  
  def set_new_todo_name(self, value):
    self.__new_todo_name = value
    self.is_valid_changed.emit()
    self.new_todo_name_changed.emit()

  def get_is_valid(self):
    return len(self.__new_todo_name) > 0

  def clear_todos(self):
    self.todos = []
    self.todo_count_changed.emit()

  @QtCore.Slot()
  def addTodo(self): # Camel case because it will be used as a js function
    # Only add a todo if the field validation passes
    if self.get_is_valid():
      # Create a Todo instance with the current value of the input field
      todo = Todo(self.__new_todo_name)
      self.todos.append(todo)
      self.todo_count_changed.emit()

      # Clear the input field
      self.set_new_todo_name('')
      
      print([todo.name for todo in self.todos])
  
  # Provide an interface through the Qt Property to communicate with the QML components
  newTodoName = QtCore.Property(str, get_new_todo_name, set_new_todo_name, notify=new_todo_name_changed)
  isValid = QtCore.Property(bool, get_is_valid, notify=is_valid_changed)