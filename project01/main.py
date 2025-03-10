print('Hello Mars')

current_file_path = __file__

# 경로에서 마지막 '/' 위치 찾기
last_slash_index = current_file_path.rfind('/')

# 폴더 경로만 추출
folder_path = current_file_path[:last_slash_index + 1]

# 경로에 파일 이름 추가
file_path = folder_path + 'mission_computer_main.log'

try:
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

        # 리스트 역순 정렬
        reversed_lines = lines[::-1]

        # Markdown 형식으로 변환
        markdown_lines = [f"- {line}" for line in reversed_lines]

        # Markdown 형식의 문자열 생성
        markdown_output = "\n".join(markdown_lines)

        # output.md 파일을 folder_path에 저장 (UTF-8 인코딩)
        output_file_path = folder_path + 'log_analysis.md'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(markdown_output)

        print(f"output.md 파일이 '{folder_path}'에 생성되었습니다.")

except FileNotFoundError:
    print(f"파일 '{file_path}'을 찾을 수 없습니다.")
