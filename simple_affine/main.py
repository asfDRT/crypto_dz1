import math


def mod_inverse(a, m):
    '''
    Функция для вычисления мультипликативного обратного элемента в кольце Z_m
    '''
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None  # Если обратного элемента нет


def affine_encrypt(text, a, b, alphabet):
    '''
    Функция для шифрования аффинным шифром
    '''
    if math.gcd(a, len(alphabet)) != 1:
        raise ValueError("Число 'a' должно быть взаимно простым с длиной алфавита.")
    
    encrypted_text = ''
    for char in text:
        if char in alphabet:
            x = alphabet.index(char)
             # Формула зашифрования: y_i = (a * x_i + b) mod n
            encrypted_text += alphabet[(a * x + b) % len(alphabet)]
        else:
            encrypted_text += char  # Оставляем символы, которых нет в алфавите, без изменений
    return encrypted_text


def affine_decrypt(text, a, b, alphabet):
    '''
    Функция для расшифрования аффинного шифра
    '''
    m = len(alphabet)
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        raise ValueError("Число 'a' не имеет мультипликативного обратного в Z_m.")
    
    decrypted_text = ''
    for char in text:
        if char in alphabet:
            y = alphabet.index(char)
            # Формула расшифрования: x_i = a^-1 * (y_i - b) mod n
            decrypted_text += alphabet[(a_inv * (y - b)) % m]
        else:
            decrypted_text += char  # Оставляем символы, которых нет в алфавите, без изменений
    return decrypted_text


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
        

        # Ввод пользователем текста и выбор режима
        text = input("Введите последовательность символов: ")
        mode = get_choice("Выберите режим:", ["Зашифровка", "Расшифровка"]).lower()
        
        if mode == "зашифровка":
            while True:
                try:
                    a = int(input("Введите коэффициент 'a' (взаимно простой с длиной алфавита): "))
                    if math.gcd(a, len(alphabet)) != 1:
                        print("Число 'a' должно быть взаимно простым с длиной алфавита.")
                        continue
                    b = int(input("Введите коэффициент 'b': "))
                    break
                except ValueError:
                    print("Некорректный ввод. Введите целые числа.")
            
            encrypted_text = affine_encrypt(text, a, b, alphabet)
            print(f"Исходный текст: {text}")
            print(f"Зашифрованный текст: {encrypted_text}")
            print(f"Ключ: a={a}, b={b}")
        
        elif mode == "расшифровка":
            while True:
                try:
                    a = int(input("Введите коэффициент 'a' (взаимно простой с длиной алфавита): "))
                    if math.gcd(a, len(alphabet)) != 1:
                        print("Число 'a' должно быть взаимно простым с длиной алфавита.")
                        continue
                    b = int(input("Введите коэффициент 'b': "))
                    break
                except ValueError:
                    print("Некорректный ввод. Введите целые числа.")
            
            decrypted_text = affine_decrypt(text, a, b, alphabet)
            print(f"Исходный текст: {text}")
            print(f"Расшифрованный текст: {decrypted_text}")
            print(f"Ключ: a={a}, b={b}")
        else:
            print("Некорректный режим.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
