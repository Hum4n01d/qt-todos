import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

import QtTodos 0.1

import 'pages'

ApplicationWindow {
  id: application

  width: 375
  height: 667

  visible: true
  flags: Qt.Window

  // Navigation View (Todos or Settings will be inside the StackView)
  Item {
    id: applicationContainer

    anchors.fill: parent

    StackView {
      id: stackView

      anchors.fill: parent

      initialItem: todosPage
    }
  }

  // Todos Page
  TodosViewModel {
    id: todosViewModel
  }

  Component {
    id: todosPage

    Todos {
      id: todos

      // When the openSettingsPage signal is triggered in Todos.qml, add a new card to the navigation stack
      onOpenSettingsPage: stackView.push(settingsPage)
      viewModel: todosViewModel
    }
  }

  // Settings Page
  SettingsViewModel {
    id: settingsViewModel

    // Send the todosViewModel Python class to the settingsViewModel through the Qt Property
    todosReference: todosViewModel
  }

  Component {
    id: settingsPage

    Settings {
      id: settings

      // Remove the settings page from the navigation stack when the dissmiss 
      onDismiss: stackView.pop()
      viewModel: settingsViewModel
    }
  }
}