import random
import datetime

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
        MissionComputer.env_values['mars_base_internal_temperature'] = random.randint(18, 30) # randint는 정수 uniform는 실수를 리턴
        MissionComputer.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        MissionComputer.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        MissionComputer.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        MissionComputer.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
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
        
        # 딕셔너리를 문자열로 변환
        log_message_str = str(log_message)
        
        with open('mars_base_log.txt', 'a') as log_file:
            log_file.write(log_message_str + "\n")  # 파일에 기록
            
        return MissionComputer.env_values

# MissionComputer 클래스의 인스턴스 생성
ds = MissionComputer()

# set_env() 메소드 호출
ds.set_env()

# get_env() 메소드 호출 및 결과 출력
ds.get_sensor_data()