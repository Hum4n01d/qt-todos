import os
import sys
import signal

from PySide2 import QtGui, QtQml

from TodosViewModel import TodosViewModel
from SettingsViewModel import SettingsViewModel
from TodosListModel import TodosListModel

# App constants
MODULE_NAME = 'QtTodos'
MAJOR_VERSION = 0
MINOR_VERSION = 1

# Enable Ctrl-C to kill
signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
  # Create QML components from a Python classes
  # major_version and minor_version represent major and minor version numbers for when we import it in QML
  QtQml.qmlRegisterType(TodosViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'TodosViewModel')
  QtQml.qmlRegisterType(SettingsViewModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'SettingsViewModel')
  QtQml.qmlRegisterType(TodosListModel, MODULE_NAME, MAJOR_VERSION, MINOR_VERSION, 'TodosListModel')

  # Use render loop that supports persistent 6major_versionfps
  os.environ['QSG_RENDER_LOOP'] = 'windows' 

  # Create system app
  app = QtGui.QGuiApplication(sys.argv)

  # Initialize QML rendering engine
  engine = QtQml.QQmlApplicationEngine(parent=app)
  engine.load('main.qml')

  # Use the app's status as an exit code
  sys.exit(app.exec_()) # exec_ to avoid collision with built in exec function