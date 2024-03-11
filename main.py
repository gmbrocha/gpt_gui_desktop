import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QTextOption, QPixmap
from dalle_req import make_dalle_req
from gpt_req import create_client_instance, make_request
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QTextEdit, QPushButton, QListWidget, \
    QListWidgetItem, QGridLayout, QFrame
import numpy
import cv2


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatGPT-DALLE GUI")
        self.setFixedHeight(1200)  # set a resizeable window
        self.setFixedWidth(1000)

        self.setGeometry(0, 0, 1200, 1000)

        # create central widget for the window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # set layout to box layout; add to central_widget as setLayout
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(40, 10, 40, 40)

        # add label for window
        self.title = QLabel("ChatGPT")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title, 0, 0, 1, 2)  # add label widget to the layout
        self.title.setStyleSheet("QLabel { font-size: 40px; padding: 6px; }")

        # add label for window
        self.query_title = QLabel("Query")
        self.layout.addWidget(self.query_title, 1, 0, 1, 1)  # add label widget to the layout
        self.query_title.setStyleSheet("QLabel { font-size: 27px; margin-left: 10px; }")

        # add label for window
        self.history_title = QLabel("History")
        self.history_title.setMaximumHeight(500)
        self.layout.addWidget(self.history_title, 1, 1, 1, 1)  # add label widget to the layout
        self.history_title.setStyleSheet("QLabel { font-size: 27px; margin-left: 10px; }")

        # create text widget for input and add to layout
        self.text_edit = QTextEdit()
        self.text_edit.setMaximumHeight(192)
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.layout.addWidget(self.text_edit, 2, 0, 1, 1)
        # self.text_edit.setStyleSheet("QTextEdit { margin-right: 15px; }")

        # add submit button widget to get the text and query the API
        self.submit = QPushButton("GENERATE RESPONSE")
        self.submit.setMaximumWidth(230)
        self.submit.clicked.connect(self.query_action)  # connect the button widget to the method/action
        self.layout.addWidget(self.submit, 3, 0, 1, 1, alignment=Qt.AlignCenter)

        # add output text box
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(220)
        self.result_text.setHidden(True)  # hide until output is generated
        self.result_text.setReadOnly(True)  # make read-only to avoid tampering
        self.layout.addWidget(self.result_text, 4, 0, 1, 1)
        self.result_text.setLineWrapMode(QTextEdit.WidgetWidth)
        self.result_text.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.result_text.setStyleSheet("QTextEdit { margin-bottom: 25px; }")

        # create and add a conversation history display
        self.conv_history_disp = QListWidget()
        self.layout.addWidget(self.conv_history_disp, 2, 1, 1, 1, alignment=Qt.AlignTop)
        self.conv_history_disp.setWordWrap(True)
        self.conv_history_disp.setMaximumWidth(460)

        # Adding horizontal line as a separator
        self.h_line = QFrame()
        self.h_line.setFrameShape(QFrame.HLine)
        self.h_line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.h_line, 5, 0, 1, -1)  # Spanning the line across all columns

        # # Adding a vertical spacer
        # self.spacer = QSpacerItem(20, 20)
        # self.layout.addItem(self.spacer, 6, 0, 1, 2)

        # Adding a new widget below the spacer
        self.dalle_title = QLabel('DALLE')
        self.layout.addWidget(self.dalle_title, 7, 0, 1, 2, alignment=Qt.AlignCenter)  # span new_label across 2 columns
        self.dalle_title.setStyleSheet("QLabel { font-size: 40px; padding: 8px; }")

        # add prompt label for DALLE
        self.dalle_subject = QLabel("Subject")
        self.layout.addWidget(self.dalle_subject, 8, 0, 1, 1)
        self.dalle_subject.setStyleSheet("QLabel { font-size: 27px; margin-left: 10px; }")

        # add style label for DALLE
        self.dalle_style = QLabel("Style")
        self.layout.addWidget(self.dalle_style, 8, 1, 1, 1)
        self.dalle_style.setStyleSheet("QLabel { font-size: 27px; margin-left: 10px; }")

        # create text widget for DALLE prompt and add to layout
        self.dalle_text_subject = QTextEdit()
        self.layout.addWidget(self.dalle_text_subject, 9, 0, 1, 1, alignment=Qt.AlignBottom)

        # create text widget for DALLE style and add to layout
        self.dalle_text_style = QTextEdit()
        self.layout.addWidget(self.dalle_text_style, 9, 1, 1, 1, alignment=Qt.AlignBottom)

        # add submit button widget to get the text and query the API
        self.submit_dalle = QPushButton("GENERATE IMAGE")
        self.submit_dalle.setMaximumWidth(200)
        self.submit_dalle.clicked.connect(self.dalle_action)  # connect the button widget to the method/action
        self.layout.addWidget(self.submit_dalle, 10, 0, 1, 2, alignment=Qt.AlignCenter)

        # create a list member to hold conversation history
        self.history = []

        self.image_label = QLabel('Image will be shown here', self)
        self.image_label.setHidden(True)  # Initially hide the label
        self.layout.addWidget(self.image_label, 11, 0, 1, 2, alignment=Qt.AlignCenter)

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
                padding: 0px;
                font-size: 14px;
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
        resp = make_request(client, model="gpt-4", messages=messages, temperature=temp)
        # resp = "Echo: " + query_text

        self.history.append((query_text, resp))

        self.result_text.setPlainText("GPT: " + resp)
        self.result_text.setHidden(False)

        self.update_conv_display()

        # clear user input
        self.text_edit.clear()

    def update_conv_display(self):
        """Docstring placeholder"""
        # clear display
        self.conv_history_disp.clear()

        # iterate and add items from history
        for el in self.history:
            list_item = QListWidgetItem("User: " + el[0])
            self.conv_history_disp.addItem(list_item)
            list_item2 = QListWidgetItem("GPT: " + el[1])
            self.conv_history_disp.addItem(list_item2)

    def dalle_action(self):
        """Docstring placeholder"""
        subject_text = self.dalle_text_subject.toPlainText()
        style_text = self.dalle_text_style.toPlainText()

        client = create_client_instance()

        img = make_dalle_req(client, subject_text, style_text, "dall-e-2")

        open_cv_image = numpy.array(img)
        # Convert RGB to BGR
        image = open_cv_image[:, :, ::-1].copy()

        h, w, ch = image.shape

        bytes_per_line = ch * w
        converted = QtGui.QImage(image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

        pic = QtGui.QPixmap.fromImage(converted)
        # pic is pixmap which can directly be set to QLabel

        self.image_label.setPixmap(pic)
        self.image_label.setScaledContents(True)
        self.image_label.setHidden(False)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
