import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Calculator")
        self.setFixedSize(300, 400)
        self.initUI()

        self.expression = ""

    def initUI(self):
        layout = QVBoxLayout()

        # 디스플레이
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(50)
        self.display.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.display)

        # 버튼 그리드
        buttons = [
            ['C', 'DEL', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]

        grid = QGridLayout()

        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                btn = QPushButton(btn_text)
                btn.setFixedSize(60, 60)
                btn.setStyleSheet("font-size: 18px;")
                grid.addWidget(btn, row_idx, col_idx)
                # 연결
                if btn_text.isdigit() or btn_text == '.':
                    btn.clicked.connect(lambda checked, t=btn_text: self.num_clicked(t))
                elif btn_text in ['+', '-', '×', '÷', '%']:
                    btn.clicked.connect(lambda checked, t=btn_text: self.op_clicked(t))
                elif btn_text == '=':
                    btn.clicked.connect(self.calculate)
                elif btn_text == 'C':
                    btn.clicked.connect(self.clear)
                elif btn_text == 'DEL':
                    btn.clicked.connect(self.delete_last)
                elif btn_text == '+/-':
                    btn.clicked.connect(self.toggle_sign)

        layout.addLayout(grid)
        self.setLayout(layout)

    def num_clicked(self, num):
        if self.expression == "" and num == '0':
            return
        self.expression += num
        self.update_display()

    def op_clicked(self, op):
        if self.expression and self.expression[-1] in '+-×÷%':
            self.expression = self.expression[:-1]
        self.expression += op
        self.update_display()

    def toggle_sign(self):
        try:
            value = eval(self.expression.replace('×', '*').replace('÷', '/'))
            value = -value
            self.expression = str(value)
            self.update_display()
        except:
            pass

    def delete_last(self):
        self.expression = self.expression[:-1]
        self.update_display()

    def clear(self):
        self.expression = ""
        self.update_display()

    def calculate(self):
        try:
            expr = self.expression.replace('×', '*').replace('÷', '/')
            result = eval(expr)
            self.expression = str(result)
            self.update_display()
        except:
            self.display.setText("Error")
            self.expression = ""

    def update_display(self):
        self.display.setText(self.expression)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
