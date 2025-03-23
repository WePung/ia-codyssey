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
        self.env_values['mars_base_internal_temperature'] = 20 + (id(self) % 12)
        self.env_values['mars_base_external_temperature'] = 10 + (id(self) % 11)
        self.env_values['mars_base_internal_humidity'] = 55 + (id(self) % 5)
        self.env_values['mars_base_external_illuminance'] = 600 + (id(self) % 115)
        self.env_values['mars_base_internal_co2'] = 0.05 + (id(self) % 8) / 1000
        self.env_values['mars_base_internal_oxygen'] = 5 + (id(self) % 2)

    def get_current_time(self):
        # 고정된 시간 사용
        return "2024-03-23 14:30:00"

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
