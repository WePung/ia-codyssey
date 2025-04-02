import random
import time

# 환경 변수 초기화
env_values = {
    'mars_base_internal_temperature': 0,
    'mars_base_external_temperature': 0,
    'mars_base_internal_humidity': 0,
    'mars_base_external_illuminance': 0,
    'mars_base_internal_co2': 0,
    'mars_base_internal_oxygen': 0
}

# 센서 클래스 정의
class DummySensor:
    def set_env(self):
        # 환경 변수에 랜덤 값 설정
        env_values.update({
            'mars_base_internal_temperature': random.randint(18, 30),
            'mars_base_external_temperature': random.randint(0, 21),
            'mars_base_internal_humidity': random.randint(50, 60),
            'mars_base_external_illuminance': random.randint(500, 715),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 2),
            'mars_base_internal_oxygen': random.randint(4, 7)
        })

# 미션 컴퓨터 클래스 정의
class MissionComputer:
    def get_sensor_data(self):
        # 환경 데이터를 로그로 기록
        log_message = {k: v for k, v in env_values.items()}
        log_str = str(log_message)
        
        with open('mars_base_log.txt', 'a') as f:
            f.write(log_str + ",\n")
            print(f"Logged: {log_str}")
        return env_values

# 메인 실행 로직
def main():
    ds = DummySensor()
    mc = MissionComputer()
    print("System started. Press 'q' to quit.")

    while True:
        # 센서 데이터 업데이트 및 로깅
        ds.set_env()
        mc.get_sensor_data()

        # 사용자 입력 대기 (5초 제한)
        print("\n[5초 동안 입력 대기] 'q' 입력 시 종료:")
        
        user_input = None
        start_time = time.time()

        for remaining_time in range(5, 0, -1):  # 카운트다운 (5초 -> 1초)
            print(f"남은 시간: {remaining_time}초")
            time.sleep(1)  # 초마다 대기
            
            if time.time() - start_time >= remaining_time:  # 남은 시간이 지나면 입력 대기 시작
                user_input = input("입력: ")
                if user_input:
                    break

        # 입력 처리 (시간 초과 시 공백으로 간주)
        if not user_input:
            print("⚠️ 입력 없음: 공백으로 간주합니다.")
            user_input = " "  # 공백으로 처리
        
        if user_input == "q":
            print("Terminating program...")
            break
        else:
            print(f"입력된 값: '{user_input}' (종료하려면 'q' 입력)")

if __name__ == "__main__":
    main()
