import zipfile
import itertools
import time
import sys
import multiprocessing

def try_passwords(start_chars, chars, zip_path, result_queue):
    try:
        with zipfile.ZipFile(zip_path) as zip_file:
            for first in start_chars:
                for rest in itertools.product(chars, repeat=5):
                    password = first + ''.join(rest)
                    try:
                        zip_file.extractall(pwd=password.encode())
                        result_queue.put(password)
                        return
                    except RuntimeError:
                        continue
                    except Exception:
                        continue
    except Exception as e:
        print(f'프로세스 오류: {e}')

def unlock_zip_parallel():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    zip_path = 'emergency_storage_key.zip'
    start_time = time.time()
    cpu_count = multiprocessing.cpu_count()
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

    try:
        zipfile.ZipFile(zip_path)
    except FileNotFoundError:
        print('Error: emergency_storage_key.zip 파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'ZIP 파일 열기 오류: {e}')
        return

    print('🔓 암호 해독 시작:', time.strftime('%Y-%m-%d %H:%M:%S'))
    chunk_size = len(chars) // cpu_count
    processes = []

    for i in range(cpu_count):
        if i == cpu_count - 1:
            start_chars = chars[i * chunk_size :]
        else:
            start_chars = chars[i * chunk_size : (i + 1) * chunk_size]
        p = multiprocessing.Process(
            target=try_passwords,
            args=(start_chars, chars, zip_path, result_queue)
        )
        processes.append(p)
        p.start()

    found = None
    while True:
        if not result_queue.empty():
            found = result_queue.get()
            break
        if all(not p.is_alive() for p in processes):
            break
        time.sleep(0.5)

    for p in processes:
        p.terminate()

    if found:
        try:
            with open('password.txt', 'w') as f:
                f.write(found)
            print('\n✅ 성공! 암호:', found)
            print(f'소요 시간: {time.time() - start_time:.2f}초')
        except Exception as e:
            print(f'파일 저장 오류: {e}')
    else:
        print('\n❌ 모든 조합 시도 실패')

if __name__ == '__main__':
    # 기본(단일코어) 실행 : unlock_zip()
    # 병렬(멀티코어) 실행 : unlock_zip_parallel()
    unlock_zip_parallel()
