print('Hello Mars')

# 현재 파일 경로를 저장(__file__를 통해 현재 파일 경로 문자열 저장)
current_file_path = __file__

# 경로에서 마지막 '/' 위치 찾기(rfind()를 통해 /가 사용된 마지막 문자열 위치확인)
last_slash_index = current_file_path.rfind('/')

# 폴더 경로만 추출(문자열을 통해 마지막 /가 사용된 문자열까지 저장)
folder_path = current_file_path[:last_slash_index + 1]

# 경로에 파일 이름 추가(텍스트를 추출할 파일 지정)
file_path = folder_path + 'mission_computer_main.log'

try:
    # open(경로, 'r')로 파일에 접속
    # with는 함수의 자동닫기를 나타내며 블록이 자동으로 닫혀 따로 돌아다니는 데이터 방지
    # as file은 객체의 타입을 지정
    with open(file_path, 'r') as file:
        # read() 함수로 접속한 파일을 텍스트 형태로 읽음
        # splitlines() 함수로 읽어온 파일을 줄넘김 단위로 list에 추가
        lines = file.read().splitlines()

        # 리스트 역순 정렬
        reversed_lines = lines[::-1]

        # Markdown 형식으로 변환
        markdown_lines = [f"- {line}" for line in reversed_lines]

        # Markdown 형식의 문자열 생성(join()함수를 통해 여러줄의 데이터를 하나로 통합)
        markdown_output = "\n".join(markdown_lines)

        # output.md 파일을 folder_path에 저장 (UTF-8 인코딩)
        output_file_path = folder_path + 'log_analysis.md'
        # open()함수로 w작성 모드를 통해 인코딩을 utf-8로 설정 후 현재 폴더로 생성 위치 지정 후 생성
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(markdown_output)

        print(f"output.md 파일이 '{folder_path}'에 생성되었습니다.")

        # ERROR 메시지가 포함된 줄 추출
        error_lines = [line for line in lines if 'ERROR' in line]

        # Markdown 형식으로 변환
        error_markdown_lines = [f"- {line}" for line in error_lines]

        # Markdown 형식의 문자열 생성
        error_markdown_output = "\n".join(error_markdown_lines)

        # ERROR.md 파일을 folder_path에 저장 (UTF-8 인코딩)
        error_file_path = folder_path + 'err_log_analysis.md'
        with open(error_file_path, 'w', encoding='utf-8') as error_file:
            error_file.write(error_markdown_output)

        print(f"ERROR.md 파일이 '{folder_path}'에 생성되었습니다.")

        # ERROR 메시지가 포함되지 않은 줄 추출
        non_error_lines = [line for line in lines if 'ERROR' not in line]

        # Markdown 형식으로 변환
        non_error_markdown_lines = [f"- {line}" for line in non_error_lines]

        # Markdown 형식의 문자열 생성
        non_error_markdown_output = "\n".join(non_error_markdown_lines)

        # NON_ERROR.md 파일을 folder_path에 저장 (UTF-8 인코딩)
        non_error_file_path = folder_path + 'log_analysis.md'
        with open(non_error_file_path, 'w', encoding='utf-8') as non_error_file:
            non_error_file.write(non_error_markdown_output)

        print(f"NON_ERROR.md 파일이 '{folder_path}'에 생성되었습니다.")

except FileNotFoundError:
    print(f"파일 '{file_path}'을 찾을 수 없습니다.")
