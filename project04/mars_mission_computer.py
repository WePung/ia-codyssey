import random
import time

env_values_list = []

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
        
        # 리스트에 사본 추가 (원본 보존성을 위함)
        env_values_list.append(env_values.copy())
        
        with open('mars_base_log.txt', 'a') as f:
            f.write(log_str + ",\n")
            print(f"Logged: {log_str}")
        return env_values

def main():
    ds = DummySensor()
    mc = MissionComputer()
    count = 0  # 카운트 초기화
    print("System started. Press 'q' to quit.")

    while True:
        # 센서 데이터 업데이트 및 로깅
        ds.set_env()
        mc.get_sensor_data()
        count += 1

        # 60번(300초) 마다 평균 계산
        if count % 60 == 0:
            # 내부/외부 온도 추출
            internal_temps = [entry['mars_base_internal_temperature'] for entry in env_values_list]
            external_temps = [entry['mars_base_external_temperature'] for entry in env_values_list]
            internal_humidity = [entry['mars_base_internal_humidity'] for entry in env_values_list]
            external_illuminance = [entry['mars_base_external_illuminance'] for entry in env_values_list]
            internal_co2 = [entry['mars_base_internal_co2'] for entry in env_values_list]
            internal_oxygen = [entry['mars_base_internal_oxygen'] for entry in env_values_list]
            
            # 평균 계산
            avg_internal = sum(internal_temps) / len(internal_temps)
            avg_external = sum(external_temps) / len(external_temps)
            avg_internal_humidity = sum(internal_humidity) / len(internal_humidity)
            avg_external_illuminance = sum(external_illuminance) / len(external_illuminance)
            avg_internal_co2 = sum(internal_co2) / len(internal_co2)
            avg_internal_oxygen = sum(internal_oxygen) / len(internal_oxygen)
            
            # 결과 출력
            print(f"\n[60회 데이터 평균]")
            print(f"내부 온도 평균: {avg_internal:.2f}°C")
            print(f"외부 온도 평균: {avg_external:.2f}°C")
            print(f"내부 내부 습도 평균: {avg_internal_humidity:.2f}%")
            print(f"외부 외부 광량 평균: {avg_external_illuminance:.2f}")
            print(f"내부 내부 이산화탄소 농도 평균: {avg_internal_co2:.2f}")
            print(f"외부 내부 산소 농도 평균: {avg_internal_oxygen:.2f}")

            # 리스트 초기화(초기화가 필요없을 시 주석 처리)
            env_values_list.clear()

        print("\n[5초 동안 입력 대기] 'q' 입력 시 종료:")
        for remaining_time in range(5, 0, -1):
            print(f"남은 시간: {remaining_time}초")
            time.sleep(1)

        user_input = input("입력: ")
        if user_input == "q":
            print("Terminating program...")
            break

if __name__ == "__main__":
    main()
