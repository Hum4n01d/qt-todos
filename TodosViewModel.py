from PySide2 import QtCore

from models import Todo

class TodosViewModel(QtCore.QObject):
  is_valid_changed = QtCore.Signal()
  new_todo_name_changed = QtCore.Signal()
  todo_count_changed = QtCore.Signal()
  pre_insert_todo = QtCore.Signal(int)
  post_insert_todo = QtCore.Signal()
  pre_clear_todos = QtCore.Signal()
  post_clear_todos = QtCore.Signal()
  todo_is_checked_changed = QtCore.Signal(int)

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
    # Tell the ListView that we are going to clear all todos
    self.pre_clear_todos.emit()

    self.todos = []
    self.todo_count_changed.emit()

    # Tell the ListView that we are finished clearing all todos
    self.post_clear_todos.emit()

  # A slot is a function we can use in JS in QML
  @QtCore.Slot()
  def toggleFirstTodo(self): # Camel case because it will be used as a js function
    # Make sure there is a first todo
    if len(self.todos) > 0:
      todo = self.todos[0]
      todo.is_checked = not todo.is_checked # Toggle the is_checked property
      self.todo_is_checked_changed.emit(0) # 0 is the index of the changed todo

  @QtCore.Slot()
  def addTodo(self):
    # Only add a todo if the field validation passes
    if self.get_is_valid():
      # Tell the ListView that we are going to add a todo
      self.pre_insert_todo.emit(len(self.todos)) # Index of new todo is the current length of the list

      # Create a Todo instance with the current value of the input field
      todo = Todo(self.__new_todo_name)
      self.todos.append(todo)
      self.todo_count_changed.emit()

      # Clear the input field
      self.set_new_todo_name('')
      
      # Tell the ListView that we finished adding a todo
      self.post_insert_todo.emit()
  
  # Provide an interface through the Qt Property to communicate with the QML components
  newTodoName = QtCore.Property(str, get_new_todo_name, set_new_todo_name, notify=new_todo_name_changed)
  isValid = QtCore.Property(bool, get_is_valid, notify=is_valid_changed)