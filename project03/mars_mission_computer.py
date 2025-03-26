import random
import datetime

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        # 내장 기능만 사용하여 간단한 "랜덤" 숫자 생성 (실제로는 랜덤이 아님)
        self.env_values['mars_base_internal_temperature'] = random.randint(18,30)
        self.env_values['mars_base_external_temperature'] = random.randint(0,21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50,60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500,715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02,0.1)
        self.env_values['mars_base_internal_oxygen'] = random.randint(4,7)
        
    # 고정된 시간 사용
    def get_current_time(self):
        return datetime.datetime.now()

    def get_env(self):
        current_time = self.get_current_time()
        log_message = (
            f"{current_time}, "
            f"{self.env_values['mars_base_internal_temperature']:.2f}, "
            f"{self.env_values['mars_base_external_temperature']:.2f}, "
            f"{self.env_values['mars_base_internal_humidity']:.2f}, "
            f"{self.env_values['mars_base_external_illuminance']:.2f}, "
            f"{self.env_values['mars_base_internal_co2']:.4f}, "
            f"{self.env_values['mars_base_internal_oxygen']:.2f}"
        )
        
        with open('mars_base_log.txt', 'a') as log_file:
            log_file.write(log_message + '\n')
        
        return self.env_values

# DummySensor 클래스의 인스턴스 생성
ds = DummySensor()

# set_env() 메소드 호출
ds.set_env()

# get_env() 메소드 호출 및 결과 출력
print(ds.get_env())
