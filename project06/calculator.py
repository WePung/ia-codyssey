import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iOS Style Calculator")
        self.setFixedSize(340, 520)
        self.initUI()
        self.expression = ""

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # 디스플레이
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(80)
        self.display.setStyleSheet("""
            background: #222;
            color: white;
            border: none;
            font-size: 36px;
            padding: 12px;
            border-radius: 12px;
        """)
        layout.addWidget(self.display)

        # 버튼 그리드
        buttons = [
            ['C', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid = QGridLayout()
        grid.setSpacing(10)

        # 버튼 스타일
        btn_styles = {
            'num': """
                QPushButton {
                    background: #333;
                    color: white;
                    border-radius: 32px;
                    font-size: 26px;
                    font-weight: bold;
                }
                QPushButton:pressed {
                    background: #555;
                }
            """,
            'op': """
                QPushButton {
                    background: #FF9500;
                    color: white;
                    border-radius: 32px;
                    font-size: 26px;
                    font-weight: bold;
                }
                QPushButton:pressed {
                    background: #FFA733;
                }
            """,
            'func': """
                QPushButton {
                    background: #A5A5A5;
                    color: black;
                    border-radius: 32px;
                    font-size: 26px;
                    font-weight: bold;
                }
                QPushButton:pressed {
                    background: #C5C5C5;
                }
            """
        }

        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                if btn_text in ['+', '-', '×', '÷', '=']:
                    style = btn_styles['op']
                elif btn_text in ['C', '+/-', '%']:
                    style = btn_styles['func']
                else:
                    style = btn_styles['num']

                btn = QPushButton(btn_text)
                btn.setFixedSize(64, 64)
                btn.setStyleSheet(style)

                # 0 버튼은 두 칸 차지
                if btn_text == '0':
                    btn.setFixedSize(144, 64)
                    grid.addWidget(btn, row_idx, col_idx, 1, 2)
                    continue
                # 0 다음 버튼은 위치 조정
                if btn_text == '.':
                    grid.addWidget(btn, row_idx, col_idx+1)
                else:
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

    def delete_last(self):
        self.expression = self.expression[:-1]
        self.update_display()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
