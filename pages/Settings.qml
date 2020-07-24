import QtQuick 2.15
import QtQuick.Controls 2.15

import QtTodos 0.1

Item {
  property SettingsViewModel viewModel

  signal dismiss

  Column {
    spacing: 4

    anchors {
      top: parent.top
      left: parent.left

      margins: 8
    }

    Label {
      // Update the label on the Settings Page with the number
      text: `Number of todos: ${viewModel && viewModel.todoCount}`
    }

    Button {
      text: 'Clear'

      onClicked: viewModel.clearTodos()
    }
    
    Button {
      text: 'Close'

      onClicked: dismiss()
    }
  }
}