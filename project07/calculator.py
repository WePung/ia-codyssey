import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt

class Calculator:
    """계산기 핵심 기능 클래스"""
    def __init__(self):
        self.reset()
        
    def reset(self):
        """초기화 메소드"""
        self.current_value = '0'
        self.previous_value = None
        self.operation = None
        self.new_input = True
        self.has_decimal = False

    def add(self):
        """덧셈 연산 설정"""
        self._set_operation('+')

    def subtract(self):
        """뺄셈 연산 설정"""
        self._set_operation('-')

    def multiply(self):
        """곱셈 연산 설정"""
        self._set_operation('×')

    def divide(self):
        """나눗셈 연산 설정"""
        self._set_operation('÷')

    def _set_operation(self, op):
        """연산자 설정 헬퍼 메소드"""
        self.operation = op
        self.previous_value = self.current_value
        self.new_input = True
        self.has_decimal = False

    def negative_positive(self):
        """양수/음수 전환"""
        if self.current_value != '0':
            self.current_value = str(-float(self.current_value))
            self.has_decimal = '.' in self.current_value

    def percent(self):
        """퍼센트 계산"""
        try:
            value = float(self.current_value)
            self.current_value = str(value / 100)
            self.has_decimal = '.' in self.current_value
        except:
            self.reset()
            raise

    def equal(self):
        """결과 계산"""
        if self.operation and self.previous_value:
            try:
                a = float(self.previous_value)
                b = float(self.current_value)
                
                if self.operation == '+':
                    result = a + b
                elif self.operation == '-':
                    result = a - b
                elif self.operation == '×':
                    result = a * b
                elif self.operation == '÷':
                    if b == 0:
                        raise ZeroDivisionError
                    result = a / b
                
                self.current_value = self._format_result(result)
                self.operation = None
                self.previous_value = None
                self.new_input = True
                self.has_decimal = '.' in self.current_value
                
            except ZeroDivisionError:
                raise
            except:
                self.reset()
                raise

    def _format_result(self, value):
        """결과 포매팅"""
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        formatted = "{:.6f}".format(value).rstrip('0').rstrip('.')
        return formatted if formatted else '0'

class CalculatorUI(QWidget):
    """계산기 UI 클래스"""
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('Calculator')
        self.setFixedSize(340, 520)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # 디스플레이 설정
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFixedHeight(80)
        self._update_display_style()
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

        # 버튼 생성 및 연결
        for row, row_buttons in enumerate(buttons):
            for col, btn_text in enumerate(row_buttons):
                btn = self._create_button(btn_text)
                
                if btn_text == '0':
                    btn.setFixedSize(144, 64)
                    grid.addWidget(btn, row, col, 1, 2)
                elif btn_text in ['.', '=']:
                    grid.addWidget(btn, row, col+1)
                else:
                    grid.addWidget(btn, row, col)

                # 버튼 핸들러 연결
                if btn_text in {'+', '-', '×', '÷'}:
                    btn.clicked.connect(self._create_operator_handler(btn_text))
                elif btn_text == '=':
                    btn.clicked.connect(self._handle_equal)
                elif btn_text == 'C':
                    btn.clicked.connect(self._handle_clear)
                elif btn_text == '+/-':
                    btn.clicked.connect(self._handle_sign)
                elif btn_text == '%':
                    btn.clicked.connect(self._handle_percent)
                elif btn_text == '.':
                    btn.clicked.connect(self._handle_decimal)
                else:
                    btn.clicked.connect(self._create_number_handler(btn_text))

        layout.addLayout(grid)
        self.setLayout(layout)
        self._update_display()

    def _create_button(self, text):
        """버튼 생성 메소드"""
        btn = QPushButton(text)
        btn.setFixedSize(64, 64)
        style = self._get_button_style(text)
        btn.setStyleSheet(style)
        return btn

    def _get_button_style(self, text):
        """버튼 스타일 결정"""
        if text in {'+', '-', '×', '÷', '='}:
            return '''
                QPushButton {
                    background: #FF9500;
                    color: white;
                    border-radius: 32px;
                    font-size: 26px;
                    font-weight: bold;
                }
                QPushButton:pressed { background: #FFA733; }'''
        elif text in {'C', '+/-', '%'}:
            return '''
                QPushButton {
                    background: #A5A5A5;
                    color: black;
                    border-radius: 32px;
                    font-size: 26px;
                    font-weight: bold;
                }
                QPushButton:pressed { background: #C5C5C5; }'''
        else:
            return '''
                QPushButton {
                    background: #333;
                    color: white;
                    border-radius: 32px;
                    font-size: 26px;
                    font-weight: bold;
                }
                QPushButton:pressed { background: #555; }'''

    def _create_number_handler(self, num):
        """숫자 버튼 핸들러 생성"""
        def handler():
            if self.calculator.new_input:
                self.calculator.current_value = num
                self.calculator.new_input = False
            else:
                self.calculator.current_value += num
            self._update_display()
        return handler

    def _create_operator_handler(self, op):
        """연산자 버튼 핸들러 생성"""
        def handler():
            if op == '+': self.calculator.add()
            elif op == '-': self.calculator.subtract()
            elif op == '×': self.calculator.multiply()
            elif op == '÷': self.calculator.divide()
            self._update_display()
        return handler

    def _handle_equal(self):
        """등호 버튼 핸들러"""
        try:
            self.calculator.equal()
            self._update_display()
        except ZeroDivisionError:
            self.display.setText('Error')
            self.calculator.reset()

    def _handle_clear(self):
        """초기화 버튼 핸들러"""
        self.calculator.reset()
        self._update_display()

    def _handle_sign(self):
        """부호 변경 버튼 핸들러"""
        self.calculator.negative_positive()
        self._update_display()

    def _handle_percent(self):
        """퍼센트 버튼 핸들러"""
        self.calculator.percent()
        self._update_display()

    def _handle_decimal(self):
        """소수점 버튼 핸들러"""
        if not self.calculator.has_decimal:
            self.calculator.current_value += '.'
            self.calculator.has_decimal = True
            self.calculator.new_input = False
            self._update_display()

    def _update_display(self):
        """디스플레이 업데이트"""
        display_text = self.calculator.current_value
        if len(display_text) > 12:
            self.display.setStyleSheet('font-size: 24px;')
        else:
            self.display.setStyleSheet('font-size: 36px;')
        self.display.setText(display_text)

    def _update_display_style(self):
        """디스플레이 스타일 초기화"""
        self.display.setStyleSheet('''
            background: #222;
            color: white;
            border: none;
            font-size: 36px;
            padding: 12px;
            border-radius: 12px;
        ''')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalculatorUI()
    calc.show()
    sys.exit(app.exec_())
