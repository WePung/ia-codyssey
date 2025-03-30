import random
import time

json_data = []

class MissionComputer:
    env_values = {
        'mars_base_internal_temperature': 0,
        'mars_base_external_temperature': 0,
        'mars_base_internal_humidity': 0,
        'mars_base_external_illuminance': 0,
        'mars_base_internal_co2': 0,
        'mars_base_internal_oxygen': 0
    }

    def set_env(self):
        MissionComputer.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        MissionComputer.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        MissionComputer.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        MissionComputer.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        MissionComputer.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 2)
        MissionComputer.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    def get_sensor_data(self):
        log_message = {
            'mars_base_internal_temperature': MissionComputer.env_values['mars_base_internal_temperature'],
            'mars_base_external_temperature': MissionComputer.env_values['mars_base_external_temperature'],
            'mars_base_internal_humidity': MissionComputer.env_values['mars_base_internal_humidity'],
            'mars_base_external_illuminance': MissionComputer.env_values['mars_base_external_illuminance'],
            'mars_base_internal_co2': MissionComputer.env_values['mars_base_internal_co2'],
            'mars_base_internal_oxygen': MissionComputer.env_values['mars_base_internal_oxygen']
        }
        
        log_message_str = str(log_message)
        with open('mars_base_log.txt', 'a') as log_file:
            log_file.write(log_message_str + ",\n")
            
        return MissionComputer.env_values

# 메인 로직 실행
ds = MissionComputer()
print("system start (if you want to stop 'q' input)")

while True:
    print("\n5 second watting... (if you want to stop 'q' input)")
    
    # 입력 대기 (5초 동안 입력이 없으면 자동으로 데이터 수집)
    start_time = time.time()
    user_input = None
    
    while time.time() - start_time < 5:
        if user_input is None:
            user_input = input("input: ").strip().lower()
        
        if user_input == "q":
            print("\nSystem stopped...")
            exit()  # 프로그램 종료
    
    # 환경 데이터 설정 및 로그 기록
    ds.set_env()
    ds.get_sensor_data()
