import platform
import os
import json
import time

class MissionComputer:
    def __init__(self):
        pass

    def get_mission_computer_info(self):
        try:
            system_info = {
                'Operating System': platform.system(),
                'OS Version': platform.version(),
                'CPU Type': platform.processor(),
                'CPU Cores': os.cpu_count(),
                'Memory Size': self._get_memory_size()
            }
            return json.dumps(system_info, indent=4)
        except Exception as e:
            return json.dumps({'Error': str(e)}, indent=4)

    def get_mission_computer_load(self):
        """시스템 부하 정보를 JSON 형식으로 반환"""
        try:
            load_info = {
                'CPU Usage (%)': self._get_cpu_usage(),
                'Memory Usage (%)': self._get_memory_usage()
            }
            return json.dumps(load_info, indent=4)
        except Exception as e:
            return json.dumps({'Error': str(e)}, indent=4)

    def _get_memory_size(self):
        """메모리 크기 계산 (플랫폼별 처리)"""
        if platform.system() == 'Windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            c_ulong = ctypes.c_ulong
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", c_ulong),
                    ("dwMemoryLoad", c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
                ]
            memory_status = MEMORYSTATUSEX()
            memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
            return round(memory_status.ullTotalPhys / (1024 ** 3), 2)
        else:
            return round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024 ** 3), 2)

    def _get_cpu_usage(self):
        """CPU 사용량 계산 (플랫폼별 처리)"""
        if platform.system() == 'Windows':
            import ctypes.wintypes
            GetSystemTimes = ctypes.windll.kernel32.GetSystemTimes
            class FILETIME(ctypes.Structure):
                _fields_ = [
                    ('dwLowDateTime', ctypes.wintypes.DWORD),
                    ('dwHighDateTime', ctypes.wintypes.DWORD)
                ]
            idle_time = FILETIME()
            kernel_time = FILETIME()
            user_time = FILETIME()
            
            GetSystemTimes(ctypes.byref(idle_time), ctypes.byref(kernel_time), ctypes.byref(user_time))
            idle1 = (idle_time.dwHighDateTime << 32) | idle_time.dwLowDateTime
            total1 = ((kernel_time.dwHighDateTime << 32) | kernel_time.dwLowDateTime) + \
                    ((user_time.dwHighDateTime << 32) | user_time.dwLowDateTime)
            
            time.sleep(1)
            
            GetSystemTimes(ctypes.byref(idle_time), ctypes.byref(kernel_time), ctypes.byref(user_time))
            idle2 = (idle_time.dwHighDateTime << 32) | idle_time.dwLowDateTime
            total2 = ((kernel_time.dwHighDateTime << 32) | kernel_time.dwLowDateTime) + \
                    ((user_time.dwHighDateTime << 32) | user_time.dwLowDateTime)
            
            return round((1 - (idle2 - idle1) / (total2 - total1)) * 100, 2)
        else:
            try:
                with open('/proc/stat', 'r') as f:
                    first_line = f.readline()
                    cpu_times = list(map(int, first_line.split()[1:]))
                idle1 = cpu_times[3]
                total1 = sum(cpu_times)
                time.sleep(1)
                with open('/proc/stat', 'r') as f:
                    second_line = f.readline()
                    cpu_times = list(map(int, second_line.split()[1:]))
                idle2 = cpu_times[3]
                total2 = sum(cpu_times)
                return round((1 - (idle2 - idle1) / (total2 - total1)) * 100, 2)
            except:
                return None

    def _get_memory_usage(self):
        """메모리 사용량 계산 (플랫폼별 처리)"""
        if platform.system() == 'Windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            c_ulong = ctypes.c_ulong
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", c_ulong),
                    ("dwMemoryLoad", c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
                ]
            memory_status = MEMORYSTATUSEX()
            memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status))
            return memory_status.dwMemoryLoad
        else:
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.readlines()
                mem_total = int(meminfo[0].split()[1])
                mem_free = int(meminfo[1].split()[1])
                return round(((mem_total - mem_free) / mem_total) * 100, 2)
            except:
                return None

# 클래스 인스턴스 생성 및 테스트
if __name__ == "__main__":
    runComputer = MissionComputer()
    
    print("Mission Computer Info:")
    print(runComputer.get_mission_computer_info())
    
    print("\nMission Computer Load:")
    print(runComputer.get_mission_computer_load())
