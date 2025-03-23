# 현재 파일 경로를 저장(__file__를 통해 현재 파일 경로 문자열 저장)
current_file_path = __file__

# 경로에서 마지막 '/' 위치 찾기(rfind()를 통해 /가 사용된 마지막 문자열 위치확인)
last_slash_index = current_file_path.rfind('/')

# 폴더 경로만 추출(문자열을 통해 마지막 /가 사용된 문자열까지 저장)
folder_path = current_file_path[:last_slash_index + 1]

# 경로에 파일 이름 추가(텍스트를 추출할 파일 지정)
file_path = folder_path + 'Mars_Base_Inventory_List.csv'

try:
    # 인코딩을 명시적으로 지정하여 파일을 읽음
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        # CSV 파일을 읽기
        lines = file.readlines()
        
        print("--------Mars_Base_Inventory_List 출력--------")
        
        # CSV 데이터를 리스트로 변환
        csvs_list = [line.strip().split(',') for line in lines]
        
        # CSV 데이터를 줄 단위로 출력
        for item in csvs_list:
            print(item)
        
        # 0번째 요소 제외하고 나열
        arr = csvs_list[1:]

        # 4번째 요소(Rank)에 따라 내림차순 정렬
        sorted_arr = sorted(arr, key=lambda x: float(x[4]), reverse=True)

        print("--------정렬 출력--------")
        for item in sorted_arr:
            print(item)

        # 4번째 요소가 0.7 이상인 것들만 따로 리스트로 만들기
        filtered_list = [item for item in sorted_arr if float(item[4]) >= 0.7]

        print("\n--------0.7 이상인 요소들 출력--------")
        for item in filtered_list:
            print(item)

        # 이진법 파일을 내보낼 파일 위치 및 이름 선정
        output_bin_file = 'Mars_Base_Inventory_List.bin'

        # 이진법 파일로 내보내기
        with open(output_bin_file, 'wb') as bin_file:
            # CSV 데이터를 바이트로 변환하여 저장
            for item in filtered_list:
                bin_file.write(','.join(item).encode('utf-8') + b'\n')

        print(f"데이터가 '{output_bin_file}' 파일로 성공적으로 저장되었습니다.")

        # 내보낸 이진법 파일을 다시 읽기
        with open(output_bin_file, 'rb') as bin_file:
            loaded_lines = bin_file.readlines()

        loaded_list = [line.decode('utf-8').strip().split(',') for line in loaded_lines]

        print("\n--------이진 파일에서 읽은 데이터 출력--------")
        for item in loaded_list:
            print(item)

except FileNotFoundError:
    print(f"파일 '{file_path}'을 찾을 수 없습니다.")

except UnicodeDecodeError:
    print(f"파일 '{file_path}'의 인코딩이 올바르지 않습니다. 다른 인코딩을 시도해 보세요.")
