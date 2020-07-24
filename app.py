import os
import sys
import signal

from PySide2 import QtGui, QtQml

from TodosViewModel import TodosViewModel
from SettingsViewModel import SettingsViewModel

# Enable Ctrl-C to kill
signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
  # Create QML components from a Python classes
  # 0 and 1 represent major and minor version numbers for when we import it in QML
  QtQml.qmlRegisterType(TodosViewModel, 'QtTodos', 0, 1, 'TodosViewModel')
  QtQml.qmlRegisterType(SettingsViewModel, 'QtTodos', 0, 1, 'SettingsViewModel')

  # Use render loop that supports persistent 60fps
  os.environ['QSG_RENDER_LOOP'] = 'windows' 

  # Create system app
  app = QtGui.QGuiApplication(sys.argv)

  # Initialize QML rendering engine
  engine = QtQml.QQmlApplicationEngine(parent=app)
  engine.load('main.qml')

  # Use the app's status as an exit code
  sys.exit(app.exec_()) # exec_ to avoid collision with built in exec function