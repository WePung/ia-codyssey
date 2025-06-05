import os
import time
import wave
import pyaudio  # 외부 라이브러리 사용 가능(음성 녹음 부분)

def get_current_datetime():
    """현재 날짜와 시간을 '년월일-시분초' 형식으로 반환"""
    return time.strftime('%Y%m%d-%H%M%S', time.localtime())

def ensure_records_dir():
    """records 폴더가 없으면 생성"""
    if not os.path.exists('records'):
        os.makedirs('records')

def record_voice(duration=5, sample_rate=44100, channels=1, chunk=1024):
    """
    마이크로부터 음성을 녹음하여 파일로 저장
    :param duration: 녹음할 시간(초)
    :param sample_rate: 샘플링 레이트
    :param channels: 채널 수(모노)
    :param chunk: 버퍼 크기
    :return: 저장된 파일 경로
    """
    ensure_records_dir()
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)
    print('녹음 중...')
    frames = []
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print('녹음 완료')
    stream.stop_stream()
    stream.close()
    audio.terminate()

    filename = f"records/{get_current_datetime()}.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
    return filename

def list_recordings(start_date=None, end_date=None):
    """
    특정 날짜 범위의 녹음 파일 리스트 반환(보너스 과제)
    :param start_date: 시작 날짜(YYYYMMDD, 없으면 전체)
    :param end_date: 종료 날짜(YYYYMMDD, 없으면 전체)
    :return: 해당 날짜 범위의 파일 경로 리스트
    """
    if not os.path.exists('records'):
        return []
    files = os.listdir('records')
    result = []
    for f in files:
        if not f.endswith('.wav'):
            continue
        date_part = f.split('.')[0].split('-')[0]
        try:
            file_date = int(date_part)
        except ValueError:
            continue
        if start_date is not None:
            try:
                start = int(start_date)
                if file_date < start:
                    continue
            except ValueError:
                pass
        if end_date is not None:
            try:
                end = int(end_date)
                if file_date > end:
                    continue
            except ValueError:
                pass
        result.append(os.path.join('records', f))
    return result

def main():
    print('화성 음성 기록 시스템 Javis')
    print('1. 음성 녹음')
    print('2. 특정 날짜 범위의 녹음 파일 보기(보너스 과제)')
    choice = input('메뉴를 선택하세요(1 또는 2): ')
    if choice == '1':
        filename = record_voice()
        print(f'녹음 파일이 저장되었습니다: {filename}')
    elif choice == '2':
        start = input('시작 날짜(YYYYMMDD, 생략 가능): ')
        end = input('종료 날짜(YYYYMMDD, 생략 가능): ')
        files = list_recordings(start if start else None, end if end else None)
        print(f'해당 범위의 녹음 파일 목록:')
        for f in files:
            print(f)
    else:
        print('잘못된 입력입니다.')

if __name__ == '__main__':
    main()
