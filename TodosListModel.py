from PySide2 import QtCore

from TodosViewModel import TodosViewModel

class TodosListModel(QtCore.QAbstractListModel):
  NAME_ROLE = QtCore.Qt.UserRole # UserRole means custom role which means custom object key in JS
  IS_CHECKED_ROLE = QtCore.Qt.UserRole + 1 # Add one because it needs a unique enum value

  def __init__(self, parent=None):
    QtCore.QAbstractListModel.__init__(self, parent)

    self.__todos_reference = None
  
  def get_todo_count(self):
    if self.__todos_reference:
      return len(self.__todos_reference.todos)
    
    return 0

  def get_todos_reference(self):
    return self.__todos_reference

  def todo_is_checked_changed_callback(self, row):
    # Create a QModelIndex from the row number
    # createIndex is a ListModel class method
    index = self.createIndex(row, 0) # Column is zero

    # Use the ListModel dataChanged signal to indicate that the UI needs to be updated at this index
    self.dataChanged.emit(index, index, [self.IS_CHECKED_ROLE]) # Tell the ListModel which row range and roles are being updated

  def set_todos_reference(self, value):
    # Only change the view model if there is a new one (don't reload when closing the app)
    if value:
      # Tell the list model that we are going to replace the entirety of the list (not just change one item)
      # beginResetModel and endResetModel are class methods from the parent
      self.beginResetModel()
      self.__todos_reference = value
      self.endResetModel()

      # Connect signals in TodosViewModel
      # QtCore.QModelIndex() is because we don't have a parent list for the ListModel and we have index twice because we have a start and end index for insertion
      self.__todos_reference.pre_insert_todo.connect(lambda index: self.beginInsertRows(QtCore.QModelIndex(), index, index)) 
      self.__todos_reference.post_insert_todo.connect(lambda: self.endInsertRows())
      
      # QtCore.QModelIndex() is because we don't have a parent list for the ListModel
      self.__todos_reference.pre_clear_todos.connect(lambda: self.beginRemoveRows(QtCore.QModelIndex(), 0, len(self.__todos_reference.todos) - 1)) # Remove all todos from 0 to end
      self.__todos_reference.post_clear_todos.connect(lambda: self.endRemoveRows())

      # Tell the ListModel which row range and roles are being updated
      self.__todos_reference.todo_is_checked_changed.connect(self.todo_is_checked_changed_callback)
  
  # Override the required roleNames method from the parent ListModel class
  # Camel cased because it's a wrapper for a C++ function
  def roleNames(self):
    # Create a mapping of our enum ints to their JS object key names
    # In QML we can use them as model.name or model.isChecked where model is the ListModel
    return {
      self.NAME_ROLE: b'name',
      self.IS_CHECKED_ROLE: b'isChecked'
    }

  # Override the required rowCount method from the parent ListModel class
  def rowCount(self, parent=QtCore.QModelIndex()):
    if self.__todos_reference:
      # Prevents value from being returned if the list has a parent (is inside another list)
      if not parent.isValid():
        return len(self.__todos_reference.todos)

  # Override the required data method from the parent ListModel class
  def data(self, index, role=QtCore.Qt.DisplayRole): # DisplayRole is a default role (object key in QML) that returns the fallback value for the data function
    # Make sure the view model is connected (don't load in data before the UI loads)
    if self.__todos_reference:
      # Make sure the index is within the range of the row count (in the list)
      if index.isValid():
        # Get the data at the index for the ListModel to display
        todo = self.__todos_reference.todos[index.row()] # index is an object with row and column methods

        # Return the type of data that was requested based on the role enum values
        if role == self.NAME_ROLE:
          return todo.name
        elif role == self.IS_CHECKED_ROLE:
          return todo.is_checked

    # This is for DisplayRole or if the todos reference doesn't exist
    return None 

  # Override the required setData method from the parent ListModel class
  def setData(self, index, value, role):
    # Make sure there is a reference to the TodosViewModel
    # Only allow changes to the checked value, we can't rename todos from within the todo item UI
    if self.__todos_reference and role == self.IS_CHECKED_ROLE:
      todo = self.__todos_reference.todos[index.row()] # index is an object with row and column methods
      todo.is_checked = value

      # Use the ListModel dataChanged signal to indicate that the UI needs to be updated at this index 
      # dataChanged requires two QModelIndex arguments and because we are overriding a default class method, they are already in the right format
      self.dataChanged.emit(index, index, [self.IS_CHECKED_ROLE]) # Tell the ListModel which row range and roles are being updated
      
      return True

    return False

  # A slot is a function we can use in JS in QML
  @QtCore.Slot()
  def clearTodos(self):
    # Run the clear_todos function from the TodosViewModel in Python
    self.__todos_reference.clear_todos()

  todosReference = QtCore.Property(TodosViewModel, get_todos_reference, set_todos_reference)