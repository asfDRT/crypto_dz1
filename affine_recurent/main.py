import math


def mod_inverse(a, m):
    '''
    Функция для вычисления мультипликативного обратного элемента в кольце Z_m
    '''
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None  # Если обратного элемента нет


def affine_recursive_encrypt(text, a1, a2, b1, b2, alphabet):
    '''
    Функция для шифрования аффинным рекуррентным шифром
    '''
    m = len(alphabet)
    if math.gcd(a1, m) != 1 or math.gcd(a2, m) != 1:
        raise ValueError("Числа 'a1' и 'a2' должны быть взаимно простыми с длиной алфавита")
    
    n = len(text)
    # Генерация последовательностей ключей
    a_sequence = [a1, a2] # Начальные a1, a2
    b_sequence = [b1, b2] # Начальные b1, b2
    
    # Рекуррентное вычисление ключей для каждого символа
    for i in range(2, n):
        # a_i = (a_{i-1} * a_{i-2}) mod n
        a_next = (a_sequence[i-1] * a_sequence[i-2]) % m
        a_sequence.append(a_next)

        # b_i = (b_{i-1} + b_{i-2}) mod n
        b_next = (b_sequence[i-1] + b_sequence[i-2]) % m
        b_sequence.append(b_next)
    
    encrypted_text = []
    for i, char in enumerate(text):
        if char in alphabet:
            x = alphabet.index(char)
            a_i = a_sequence[i] 
            b_i = b_sequence[i]
            # y_i = (a_i * x_i + b_i) mod n
            y = (a_i * x + b_i) % m
            encrypted_text.append(alphabet[y])
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)


def affine_recursive_decrypt(text, a1, a2, b1, b2, alphabet):
    '''
    Функция для расшифрования аффинного рекуррентного шифра
    '''
    m = len(alphabet)
    if math.gcd(a1, m) != 1 or math.gcd(a2, m) != 1:
        raise ValueError("Числа 'a1' и 'a2' должны быть взаимно простыми с длиной алфавита")
    
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
                raise ValueError(f"Обратный элемент для a_{i} = {a_i} не существует в Z_{m}")
            x = (a_inv * (y - b_i)) % m
            decrypted_text.append(alphabet[x])
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)


def get_choice(prompt, choices):
    '''
    Функция для взаимодействия с пользователем
    '''
    while True:
        print(prompt)
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        try:
            selection = int(input("Выберите номер: ").strip())
            if 1 <= selection <= len(choices):
                return choices[selection - 1]
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")


def main():
    try:
        # Два алфавита для шифрования
        alphabet_options = {
            "Только заглавные буквы": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "Заглавные, строчные и пробел": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        }
        
        # Выбор алфавита пользователем
        alphabet_choice = get_choice("Выберите алфавит:", list(alphabet_options.keys()))
        alphabet = alphabet_options[alphabet_choice]
        m = len(alphabet)
        
        # Ввод текста и выбор режима
        text = input("Введите последовательность символов: ")
        mode = get_choice("Выберите режим:", ["Зашифровка", "Расшифровка"]).lower()
        
        if mode == "зашифровка":
            while True:
                try:
                    a1 = int(input("Введите первый коэффициент 'a1' (взаимно простой с длиной алфавита): "))
                    a2 = int(input("Введите второй коэффициент 'a2' (взаимно простой с длиной алфавита): "))
                    if math.gcd(a1, m) != 1 or math.gcd(a2, m) != 1:
                        print("Числа 'a1' и 'a2' должны быть взаимно простыми с длиной алфавита.")
                        continue
                    b1 = int(input("Введите первый коэффициент 'b1': "))
                    b2 = int(input("Введите второй коэффициент 'b2': "))
                    break
                except ValueError:
                    print("Некорректный ввод. Введите целые числа.")
            
            encrypted_text = affine_recursive_encrypt(text, a1, a2, b1, b2, alphabet)
            print(f"Исходный текст: {text}")
            print(f"Зашифрованный текст: {encrypted_text}")
            print(f"Начальные ключи: a1={a1}, a2={a2}, b1={b1}, b2={b2}")
        
        elif mode == "расшифровка":
            while True:
                try:
                    a1 = int(input("Введите первый коэффициент 'a1' (взаимно простой с длиной алфавита): "))
                    a2 = int(input("Введите второй коэффициент 'a2' (взаимно простой с длиной алфавита): "))
                    if math.gcd(a1, m) != 1 or math.gcd(a2, m) != 1:
                        print("Числа 'a1' и 'a2' должны быть взаимно простыми с длиной алфавита.")
                        continue
                    b1 = int(input("Введите первый коэффициент 'b1': "))
                    b2 = int(input("Введите второй коэффициент 'b2': "))
                    break
                except ValueError:
                    print("Некорректный ввод. Введите целые числа.")
            
            decrypted_text = affine_recursive_decrypt(text, a1, a2, b1, b2, alphabet)
            print(f"Исходный текст: {text}")
            print(f"Расшифрованный текст: {decrypted_text}")
            print(f"Начальные ключи: a1={a1}, a2={a2}, b1={b1}, b2={b2}")
        else:
            print("Некорректный режим.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()