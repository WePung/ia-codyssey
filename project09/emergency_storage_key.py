def caesar_cipher_decode(target_text, shift):
    """
    카이사르 암호 해독 함수
    :param target_text: 해독할 문자열
    :param shift: 이동할 자리수(shift)
    :return: shift만큼 평행이동한 결과 문자열
    """
    result = []
    for char in target_text:
        if char.isupper():
            result_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        elif char.islower():
            result_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            result_char = char
        result.append(result_char)
    return ''.join(result)

def find_caesar_keyword_match(target_text, dictionary):
    """
    사전 단어가 해독된 문자열에 포함되는지 확인
    :param target_text: 해독할 문자열
    :param dictionary: 사전 단어 리스트
    :return: (shift, 해독된 문자열) 또는 None (일치 없음)
    """
    for shift in range(26):
        decoded = caesar_cipher_decode(target_text, shift)
        for word in dictionary:
            if word.lower() in decoded.lower():
                return (shift, decoded)
    return None

def main():
    # 사전 단어 리스트 (보너스 과제용)
    dictionary_words = ['open', 'door', 'password', 'key', 'success', 'enter', 'correct']
    
    # 파일 읽기
    try:
        with open('password.txt', 'r', encoding='utf-8') as f:
            encrypted_text = f.read().strip()
    except FileNotFoundError:
        print("Error: password.txt 파일을 찾을 수 없습니다.")
        return
    except Exception as e:
        print(f"Error: 파일을 읽는 중 오류가 발생했습니다. {e}")
        return

    # 보너스 과제: 사전 단어 매칭
    keyword_result = find_caesar_keyword_match(encrypted_text, dictionary_words)
    if keyword_result:
        shift, decoded_text = keyword_result
        print(f"사전 단어가 포함된 키 발견! shift={shift}, 결과: {decoded_text}")
        user_confirm = input(f"이 결과를 result.txt로 저장하시겠습니까? (y/n): ")
        if user_confirm.lower() == 'y':
            try:
                with open('result.txt', 'w', encoding='utf-8') as f:
                    f.write(decoded_text)
                print("result.txt에 저장되었습니다.")
            except Exception as e:
                print(f"Error: 파일을 쓰는 중 오류가 발생했습니다. {e}")
        return

    # 일반 출력: 각 shift별 결과
    print("각 shift별 결과:")
    for shift in range(26):
        decoded = caesar_cipher_decode(encrypted_text, shift)
        print(f"shift={shift:2d}: {decoded}")

    # 사용자 입력 받아서 저장
    user_shift = input("해독에 성공한 shift 번호를 입력하세요: ")
    try:
        user_shift = int(user_shift)
        decoded_text = caesar_cipher_decode(encrypted_text, user_shift)
        try:
            with open('result.txt', 'w', encoding='utf-8') as f:
                f.write(decoded_text)
            print("result.txt에 저장되었습니다.")
        except Exception as e:
            print(f"Error: 파일을 쓰는 중 오류가 발생했습니다. {e}")
    except ValueError:
        print("Error: 올바른 숫자를 입력해주세요.")

if __name__ == '__main__':
    main()
