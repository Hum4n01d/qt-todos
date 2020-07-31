import QtQuick 2.15
import QtQuick.Controls 2.15

import QtTodos 0.1

Item {
  // Create a way to connect the view model to the view
  property TodosViewModel viewModel

  signal openSettingsPage

  // Initialize the python TodosListModel class
  TodosListModel {
    id: listModel

    // viewModel is a property of the Todos component which is passed to it in main.qml as TodosViewModel
    todosReference: viewModel
  }

  ScrollView {
    anchors {
      top: parent.top
      right: parent.right
      bottom: buttons.top
      left: parent.left

      bottomMargin: 8
    }

    ListView {
      id: listView

      clip: true
      spacing: 1

      // model is an attribute for the data source and connects the ListModel to the ListView QML component
      model: listModel

      delegate: Item {
        width: listView.width
        height: 44

        Label {
          text: model.name

          anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
            
            leftMargin: 8
          }
        }

        CheckBox {
          checked: model.isChecked

          onClicked: model.isChecked = checked // checked is the CheckBox's checked property
          
          anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
            
            rightMargin: 8
          }
        }
      }
    }
  }

  Column {
    id: buttons
    
    spacing: 8

    anchors {
      bottom: parent.bottom
      left: parent.left
      margins: 8
    }

    Row {
      spacing: 4

      Button {
        text: 'Open Settings'

        // Trigger the openSettingsPage signal to run code in the main.qml file
        onClicked: openSettingsPage()
      }

      Button {
        text: 'Toggle First Todo'

        // Trigger the toggleFirstTodo slot in TodosViewModel
        onClicked: viewModel.toggleFirstTodo()
      }
    }

    Row {
      spacing: 4
      
      TextField {
        id: todoNameField

        // Use the newTodoName Qt Property that we wrote in the TodosViewModel
        // Only use this property if the viewModel exists
        text: viewModel && viewModel.newTodoName

        // Built in TextField signal that is triggered when the user types something
        onTextEdited: {
          viewModel.newTodoName = text
        }

        // Enter key pressed
        onAccepted: {
          if (viewModel.isValid) {
            viewModel.addTodo()
          }
        }
      }

      Button {
        text: 'Add Todo'

        // When the button is clicked, call the addTodo function in the TodosViewModel
        onClicked: viewModel.addTodo()

        // Use the isValid Qt Property that we wrote in the TodosViewModel
        // Only use this property if the viewModel exists
        enabled: viewModel && viewModel.isValid 
      }
    }
  }
}