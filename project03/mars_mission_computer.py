import random
import datetime

class DummySensor:
    env_values = {
        'mars_base_internal_temperature': 0,
        'mars_base_external_temperature': 0,
        'mars_base_internal_humidity': 0,
        'mars_base_external_illuminance': 0,
        'mars_base_internal_co2': 0,
        'mars_base_internal_oxygen': 0
    }

    def set_env(self):
        DummySensor.env_values['mars_base_internal_temperature'] = random.randint(18, 30) # randint는 정수 uniform는 실수를 리턴
        DummySensor.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        DummySensor.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        DummySensor.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        DummySensor.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        DummySensor.env_values['mars_base_internal_oxygen'] = random.randint(4, 7)

    def get_env(self):
        current_time = datetime.datetime.now()
        log_message = (
            f"file create time : {current_time} \n"
            f"mars_base_internal_temperature : {DummySensor.env_values['mars_base_internal_temperature']}\n" # f는 문자열을 사용하겠다는 의미
            f"mars_base_external_temperature : {DummySensor.env_values['mars_base_external_temperature']}\n"
            f"mars_base_internal_humidity : {DummySensor.env_values['mars_base_internal_humidity']}\n"
            f"mars_base_external_illuminance : {DummySensor.env_values['mars_base_external_illuminance']}\n"
            f"mars_base_internal_co2 : {DummySensor.env_values['mars_base_internal_co2']:.2f}\n" # 소수점 표기
            f"mars_base_internal_oxygen : {DummySensor.env_values['mars_base_internal_oxygen']}\n"
        )
        
        with open('mars_base_log.txt', 'a') as log_file: # a는 추가모드로 파일을 열겠다는 의미
            log_file.write(log_message) # 파일의 무자열을 기록
        
        return DummySensor.env_values

# DummySensor 클래스의 인스턴스 생성
ds = DummySensor()

# set_env() 메소드 호출
ds.set_env()

# get_env() 메소드 호출 및 결과 출력
ds.get_env()