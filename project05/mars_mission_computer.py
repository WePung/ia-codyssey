import platform
import os
import json
import psutil

class MissionComputer:
    # 시스템 정보 가져오기
    def get_mission_computer_info(self):
        try:
            system_info = {
                'Operating System': platform.system(),  # 운영체제 이름
                'OS Version': platform.version(),       # 운영체제 버전
                'CPU Type': platform.processor(),       # CPU 프로세서 정보
                'CPU Cores': os.cpu_count(),            # CPU 코어 개수
                'Memory Size': self._get_memory_size()  # 메모리 크기
            }
            return json.dumps(system_info, indent=4)  # JSON 형식으로 반환
        except Exception as e:
            return json.dumps({'Error': str(e)}, indent=4)
        
    # CPU 사용량 계산
    def _get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)  # 1초 동안 CPU 사용률 측정

    # 메모리 사용량 계산
    def _get_memory_usage(self):
        memory_info = psutil.virtual_memory()
        return memory_info.percent  # 메모리 사용률 반환

    # 시스템 부하 정보를 JSON 형식으로 반환
    def get_mission_computer_load(self):
        try:
            load_info = {
                'CPU Usage (%)': self._get_cpu_usage(),      # CPU 사용률 계산
                'Memory Usage (%)': self._get_memory_usage()  # 메모리 사용률 계산
            }
            return json.dumps(load_info, indent=4)  # JSON 형식으로 반환
        except Exception as e:
            return json.dumps({'Error': str(e)}, indent=4)

# 클래스 인스턴스 생성 및 테스트
if __name__ == "__main__":
    runComputer = MissionComputer()
    
    print("Mission Computer Info:")
    print(runComputer.get_mission_computer_info())  # 시스템 정보 출력
    
    print("\nMission Computer Load:")
    print(runComputer.get_mission_computer_load())  # 시스템 부하 정보 출력
