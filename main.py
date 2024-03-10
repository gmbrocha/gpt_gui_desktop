import sys
from api import create_client_instance, make_request
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QTextEdit, QPushButton


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatGPT GUI")
        # self.resize(650, 450)  # set a resizeable window

        self.setGeometry(0, 0, 800, 600)

        # create central widget for the window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # set layout to box layout; add to central_widget as setLayout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(30, 10, 30, 30)

        # create a list object to hold conversation history
        self.history = []

        # add label for window
        self.title = QLabel("ChatGPT GUI. Query Below")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)  # add label widget to the layout

        # create text widget for input and add to layout
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        # horizontal layout for the query and back buttons

        # add submit button widget to get the text and query the API
        self.submit = QPushButton("GO")
        self.submit.setMaximumWidth(200)
        self.submit.clicked.connect(self.query_action)  # connect the button widget to the method/action
        self.layout.addWidget(self.submit, alignment=Qt.AlignCenter)

        # add output text box
        self.result_text = QTextEdit()
        self.result_text.setHidden(True)  # hide until output is generated
        self.result_text.setReadOnly(True)  # make read-only to avoid tampering
        self.layout.addWidget(self.result_text)

        # apply some style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2928;
            } 
            QLabel {
                color: #ffffff; /* set label text color */
                font-size: 18px;
                padding: 10px;
            }
            QTextEdit, QPushButton {
                background-color: #fff; /* text box + button background color */
                border: 1px solid #ccc; /* set border for text and push button */
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                margin-top: 10px;
                margin-bottom: 10px;
                background-color: #3e76d6;
                border: 1px solid #3e76d6;
                border-radius: 1px;
                color: #ffffff;
                padding: 5px;
                font-weight: bold;
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

        # client = create_client_instance()
        # messages = [
        #     {"role": "system", "content": "You are a helpful computer science assistant"},
        #     {"role": "user", "content": query_text},
        # ]
        # temp = 0
        # resp = make_request(client, model="gpt-3.5-turbo", messages=messages, temperature=temp)
        resp = "Echo: " + query_text

        self.history.append(resp)

        self.result_text.setPlainText(resp)
        self.result_text.setHidden(False)  # reset to false now shows the output on button push
        self.resize_window()

    def resize_window(self):
        """
        Docstring placeholder
        """
        self.resize(650, 300)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
