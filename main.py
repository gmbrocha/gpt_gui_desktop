import sys
from api import create_client_instance, make_request
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QTextEdit, QPushButton, \
    QHBoxLayout, QListWidget, QListWidgetItem, QGridLayout


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatGPT GUI")
        self.setFixedHeight(600)  # set a resizeable window
        self.setFixedWidth(900)

        self.setGeometry(0, 0, 900, 600)

        # create central widget for the window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # set layout to box layout; add to central_widget as setLayout
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(40, 10, 40, 40)

        # add label for window
        self.title = QLabel("ChatGPT GUI")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title, 0, 0, 1, 2)  # add label widget to the layout
        self.title.setStyleSheet("QLabel { font-size: 23px; padding: 10px; }")

        # add label for window
        self.history_title = QLabel("Query")
        self.layout.addWidget(self.history_title, 1, 1, 1, 1)  # add label widget to the layout
        self.history_title.setStyleSheet("QLabel { margin-left: 10px; }")

        # add label for window
        self.history_title = QLabel("History")
        self.layout.addWidget(self.history_title, 1, 0, 1, 1)  # add label widget to the layout

        # create text widget for input and add to layout
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit, 2, 1, 1, 1)

        # add submit button widget to get the text and query the API
        self.submit = QPushButton("GO")
        self.submit.setMaximumWidth(75)
        self.submit.clicked.connect(self.query_action)  # connect the button widget to the method/action
        self.layout.addWidget(self.submit, 3, 1, 1, 1, alignment=Qt.AlignCenter)

        # add output text box
        self.result_text = QTextEdit()
        self.result_text.setHidden(True)  # hide until output is generated
        self.result_text.setReadOnly(True)  # make read-only to avoid tampering
        self.layout.addWidget(self.result_text, 4, 1, 1, 1)

        # create and add a conversation history display
        self.conv_history_disp = QListWidget()
        self.conv_history_disp.setMaximumHeight(500)
        self.layout.addWidget(self.conv_history_disp, 2, 0, 3, 1)
        self.conv_history_disp.setWordWrap(True)

        # create a list member to hold conversation history
        self.history = []

        # apply some style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2928;
            } 
            QLabel {
                color: #ffffff; /* set label text color */
                font-size: 18px;
                padding: 0px;
            }
            QTextEdit, QPushButton {
                background-color: #fff; /* text box + button background color */
                border: 1px solid #ccc; /* set border for text and push button */
                padding: 6px;
                font-size: 14px;
            }
            QTextEdit {
                margin-left: 10px;
            }
            QPushButton {
                margin-top: 10px;
                margin-bottom: 10px;
                background-color: #3e76d6;
                border: 1px solid #3e76d6;
                border-radius: 1px;
                color: #ffffff;
                padding: 8px;
                padding-left: 14px;
                padding-right: 14px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ddd; /* set push button hover color */
            }
        """)

    def query_action(self):
        """
        Docstring placeholder
        """
        query_text = self.text_edit.toPlainText()  # get plaintext from the text widget

        client = create_client_instance()
        messages = [
            {"role": "system", "content": "You are a helpful computer science assistant"},
            {"role": "user", "content": query_text},
        ]
        temp = 0
        resp = make_request(client, model="gpt-3.5-turbo", messages=messages, temperature=temp)
        # resp = "Echo: " + query_text

        self.history.append((query_text, resp))

        self.result_text.setPlainText("GPT: " + resp)
        self.result_text.setHidden(False)

        self.update_conv_display()

        # clear user input
        self.text_edit.clear()

    def update_conv_display(self):
        # clear display
        self.conv_history_disp.clear()

        # iterate and add items from history
        for el in self.history:
            list_item = QListWidgetItem("User: " + el[0])
            self.conv_history_disp.addItem(list_item)
            list_item2 = QListWidgetItem("GPT: " + el[1])
            self.conv_history_disp.addItem(list_item2)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
