import csv
import os
import pickle

# 현재 파일 경로를 저장(__file__를 통해 현재 파일 경로 문자열 저장)
current_file_path = __file__

# 경로에서 폴더 경로만 추출(os.path.dirname() 사용)
folder_path = os.path.dirname(current_file_path)

# 경로에 파일 이름 추가(텍스트를 추출할 파일 지정)
file_path = os.path.join(folder_path, 'Mars_Base_Inventory_List.csv')

try:
    # 인코딩을 명시적으로 지정하여 파일을 읽음
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        # csv.reader() 함수로 CSV 파일을 읽기
        csvs = csv.reader(file)
        
        print("--------Mars_Base_Inventory_List 출력--------")
        
        # CSV 데이터를 리스트로 변환
        csvs_list = list(csvs)
        
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

        # Define the output binary file name and path
        output_bin_file = os.path.join(folder_path, 'Mars_Base_Inventory_List.bin')

        # Write the filtered list to the binary file
        with open(output_bin_file, 'wb') as bin_file:
            pickle.dump(filtered_list, bin_file)

        print(f"데이터가 '{output_bin_file}' 파일로 성공적으로 저장되었습니다.")

        # Read the binary file and print its contents
        with open(output_bin_file, 'rb') as bin_file:
            loaded_list = pickle.load(bin_file)

        print("\n--------이진 파일에서 읽은 데이터 출력--------")
        for item in loaded_list:
            print(item)

except FileNotFoundError:
    print(f"파일 '{file_path}'을 찾을 수 없습니다.")

except UnicodeDecodeError:
    print(f"파일 '{file_path}'의 인코딩이 올바르지 않습니다. 다른 인코딩을 시도해 보세요.")
