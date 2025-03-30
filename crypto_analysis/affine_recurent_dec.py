import math
from itertools import product


def mod_inverse(a, m):
    '''
    Функция для вычисления мультипликативного обратного элемента в кольце Z_m
    '''
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None  # Если обратного элемента нет


def affine_recursive_decrypt(text, a1, a2, b1, b2, alphabet):
    '''
    Функция для расшифрования аффинного рекуррентного шифра
    Возвращает расшифрованный текст и последовательности ключей
    '''
    m = len(alphabet)
    n = len(text)
    a_sequence = [a1, a2]
    b_sequence = [b1, b2]
    
    # Генерируем последовательности ключей
    for i in range(2, n):
        a_next = (a_sequence[i-1] * a_sequence[i-2]) % m
        a_sequence.append(a_next)
        b_next = (b_sequence[i-1] + b_sequence[i-2]) % m
        b_sequence.append(b_next)
    
    decrypted_text = []
    for i, char in enumerate(text):
        if char in alphabet:
            y = alphabet.index(char)
            a_i = a_sequence[i]
            b_i = b_sequence[i]
            # x_i = a_i^{-1} * (y_i - b_i) mod n
            a_inv = mod_inverse(a_i, m)
            if a_inv is None:
                return None, None, None  # Невозможно расшифровать с этими ключами
            x = (a_inv * (y - b_i)) % m
            decrypted_text.append(alphabet[x])
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text), a_sequence, b_sequence


def brute_force_decrypt(ciphertext, alphabet, search_word=None, max_key_display=10):
    '''
    Функция для перебора всех возможных ключей и поиска заданного слова в результатах
    '''
    m = len(alphabet)
    possible_a = [a for a in range(1, m) if math.gcd(a, m) == 1]
    possible_b = range(m)
    
    # Генерируем все возможные комбинации начальных ключей
    keys = product(possible_a, possible_a, possible_b, possible_b)
    
    results = []
    total_combinations = len(possible_a)**2 * len(possible_b)**2
    processed = 0
    
    print(f"Всего комбинаций для перебора: {total_combinations}")
    
    for a1, a2, b1, b2 in keys:
        try:
            decrypted, a_seq, b_seq = affine_recursive_decrypt(ciphertext, a1, a2, b1, b2, alphabet)
            if decrypted is None:
                continue
                
            processed += 1
            if processed % 100000 == 0:
                print(f"Обработано {processed}/{total_combinations} комбинаций...")
            
            # Если задано слово для поиска, проверяем его наличие
            if search_word:
                if search_word.lower() in decrypted.lower():
                    results.append((decrypted, a_seq, b_seq))
            else:
                results.append((decrypted, a_seq, b_seq))
        except:
            continue
    
    return results


def format_key_sequence(seq, max_display):
    '''
    Форматирует последовательность ключей для вывода
    '''
    if len(seq) <= max_display:
        return ', '.join(map(str, seq))
    else:
        displayed = seq[:max_display]
        return ', '.join(map(str, displayed)) + f', ... (всего {len(seq)} ключей)'


def main_bruteforce():
    try:
        # Два алфавита для шифрования
        alphabet_options = {
            "Только заглавные буквы": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "Заглавные, строчные и пробел": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        }
        
        # Выбор алфавита пользователем
        print("Выберите алфавит:")
        for i, (name, alphabet) in enumerate(alphabet_options.items(), 1):
            print(f"{i}. {name}")
        choice = int(input("Ваш выбор: ")) - 1
        alphabet = list(alphabet_options.values())[choice]
        
        # Ввод зашифрованного текста
        ciphertext = input("Введите зашифрованный текст: ")
        
        # Выбор режима поиска
        search_mode = input("Хотите искать конкретное слово в результатах? (д/н): ").lower()
        search_word = None
        if search_mode == 'д':
            search_word = input("Введите слово для поиска: ")
        
        print("\nНачинаем перебор ключей...")
        results = brute_force_decrypt(ciphertext, alphabet, search_word, len(ciphertext))
        
        if not results:
            print("Ничего не найдено.")
        else:
            for i, (text, a_seq, b_seq) in enumerate(results, 1):
                print(f"\nРасшифрованный текст: {text}")
                print(f"Начальные ключи: a1={a_seq[0]}, a2={a_seq[1]}, b1={b_seq[0]}, b2={b_seq[1]}")
                print(f"Последовательность a1, а2: {format_key_sequence(a_seq, len(ciphertext))}")
                print(f"Последовательность b1, b2: {format_key_sequence(b_seq, len(ciphertext))}")
        
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    print("Перебор ключей")
    main_bruteforce()
