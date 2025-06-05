import os
import csv

import speech_recognition as sr

def get_audio_files(directory):
    '''
    지정된 디렉토리에서 .wav, .mp3 확장자의 음성 파일 목록을 반환합니다.
    '''
    audio_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.wav') or file_name.endswith('.mp3'):
            audio_files.append(file_name)
    return audio_files

def speech_to_text(audio_path):
    '''
    음성 파일에서 텍스트를 추출합니다.
    반환값: (시작 시간, 인식된 텍스트) 리스트
    '''
    recognizer = sr.Recognizer()
    results = []
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language='ko-KR')
            # 시작 시간은 0.0으로 고정 (프레임 단위 인식은 별도 구현 필요)
            results.append((0.0, text))
        except sr.UnknownValueError:
            results.append((0.0, ''))
        except sr.RequestError:
            results.append((0.0, 'STT 서비스 오류'))
    return results

def save_text_to_csv(audio_file, text_data):
    '''
    (시간, 텍스트) 리스트를 CSV 파일로 저장합니다.
    '''
    base_name = os.path.splitext(audio_file)[0]
    csv_file = base_name + '.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'text'])
        for time, text in text_data:
            writer.writerow([time, text])
    print(f'CSV 파일 저장 완료: {csv_file}')

def process_all_audio_files(directory):
    '''
    디렉토리 내 모든 음성 파일에 대해 STT 및 CSV 저장을 수행합니다.
    '''
    audio_files = get_audio_files(directory)
    for audio_file in audio_files:
        print(f'처리 중: {audio_file}')
        audio_path = os.path.join(directory, audio_file)
        text_data = speech_to_text(audio_path)
        save_text_to_csv(audio_file, text_data)

def search_keyword_in_csv_files(directory, keyword):
    '''
    디렉토리 내 모든 CSV 파일에서 키워드가 포함된 행을 출력합니다.
    '''
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            with open(os.path.join(directory, file_name), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if keyword in row['text']:
                        print(f'파일: {file_name}, 시간: {row["time"]}, 내용: {row["text"]}')

if __name__ == '__main__':
    # 예시 사용법
    # 1. 음성 파일이 있는 디렉토리 지정
    audio_dir = 'audio'  # 예: 'audio' 폴더에 음성 파일 저장
    process_all_audio_files(audio_dir)

    # 2. 키워드 검색 (보너스)
    keyword = input('검색할 키워드를 입력하세요: ')
    search_keyword_in_csv_files(audio_dir, keyword)
