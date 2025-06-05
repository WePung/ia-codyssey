import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iOS Style Calculator") # 제목
        self.setFixedSize(340, 520) # 화면 비율(375x812) 설정
        self.initUI()
        self.expression = "" # 현재 입력된 수식 저장

    def initUI(self):
        layout = QVBoxLayout() # 위젯을 위에서 아래로 쌓는 레이아웃
        layout.setContentsMargins(12, 12, 12, 12) # 바깥 여백 설정
        layout.setSpacing(8) # 위젯 간 간격 설정

        # 디스플레이
        self.display = QLineEdit() # 입력 텍스트 박스
        self.display.setReadOnly(True) # 직접 입력 방지 디스플레이 버튼으로만 입력
        self.display.setAlignment(Qt.AlignRight) # 오른쪽 정렬
        self.display.setFixedHeight(80) # 높이 고정
        self.display.setStyleSheet("""
            background: #222;
            color: white;
            border: none;
            font-size: 36px;
            padding: 12px;
            border-radius: 12px;
        """) # 배경, 글자색, 폰트, 패딩, 둥근 모서리 등 스타일 적용
        layout.addWidget(self.display) # 디스플레이를 레이아웃에 추가

        # 버튼 그리드
        buttons = [
            ['C', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        grid = QGridLayout() # 각 행별로 버튼의 텍스트를 2차원 리스트로 정의
        grid.setSpacing(10) # 버튼 사이 간격 10px

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

                btn = QPushButton(btn_text) # QPushButton 생성
                btn.setFixedSize(64, 64) # 크기 고정
                btn.setStyleSheet(style) # 스타일 적용

                # 0 버튼은 두 칸 차지
                if btn_text == '0':
                    btn.setFixedSize(144, 64) # 가로 2배 크기
                    grid.addWidget(btn, row_idx, col_idx, 1, 2) # 2열 병합
                    continue
                # 0 다음 버튼은 위치 조정
                if btn_text in '.=':
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

        layout.addLayout(grid) # 버튼 그리드 레이아웃을 전체 레이아웃에 추가
        self.setLayout(layout) # 전체 레이아웃을 위젯에 적용

    def num_clicked(self, num): 
        if self.expression == "" and num == '0': # 선행 0 입력 방지
            return
        self.expression += num
        self.update_display()

    def op_clicked(self, op): # 현재 수식을 계산하여 부호를 바꾼 뒤 다시 표시
        if self.expression and self.expression[-1] in '+-×÷%': # 연산자가 연속 입력되는 경우 마지막 연산자를 덮어씀
            self.expression = self.expression[:-1] # 연속 연산자 입력 방지
        self.expression += op
        self.update_display()

    def toggle_sign(self):
        try:
            value = eval(self.expression.replace('×', '*').replace('÷', '/'))
            value = -value
            self.expression = str(value)
            self.update_display()
        except:
            pass  # 무효한 입력 시 무시

    def clear(self): # 수식을 초기화하고 디스플레이도 비움
        self.expression = ""
        self.update_display()

    def calculate(self): # 계산 결과를 표시, 수식의 ×, "를 파이썬 연산자*, /로 바꾼 뒤 계산
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

    def delete_last(self): # 수식의 마지막 글자를 삭제하고 디스플레이를 갱신
        self.expression = self.expression[:-1]
        self.update_display()

if __name__ == "__main__":
    app = QApplication(sys.argv) # PyQt5 애플리케이션 객체 생성
    window = Calculator() # Calculator 창 생성 및 표시
    window.show()
    sys.exit(app.exec_()) # 이벤트 루프 시작
