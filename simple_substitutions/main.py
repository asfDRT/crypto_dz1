import random
import string

def generate_key(alphabet):
    '''
    Перемешивает алфавит и создает соотвествие букв
    1. Преобразует входной алфавит в список символов
    2. Перемешивает символы в случайном порядке
    3. Создает словарь, в котором каждому символу алфавита соответствует новый случайный символ
    '''
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def reverse_key(key):
    '''
    Функция для получения обратного ключа (декодирования)
    Меняет местами ключи и значения в словаре, чтобы можно было расшифровывать текст
    '''
    return {v: k for k, v in key.items()}

def substitute(text, key):
    '''
    Функция для шифрования и расшифрование текста
    Для каждого символа текста заменяет его согласно переданному ключу
    Если символ отсутствует в ключе, он остается без изменений
    '''
    return ''.join(key.get(c, c) for c in text)

def get_choice(prompt, choices):
    '''
    Функция для взаимодействия с пользователем
    Реагирует на не числовые значения
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
            # Выбор какой будет ключ
            option = get_choice("Выберите способ получения ключа:", ["Сгенерировать", "Ввести свой"]).lower()
            
            if option == "сгенерировать":
                key = generate_key(alphabet) # генерируем случайный ключ
            else:
                # Принимаем ключ пользователя
                key_input = input("Введите ключ в виде перестановки алфавита: ")
                if len(set(key_input)) != len(alphabet) or any(c not in alphabet for c in key_input):
                    print("Некорректный ключ.")
                    return
                key = dict(zip(alphabet, key_input)) # создание словаря подстановки на основе ввода
            
            # Шифрование текста и его вывод
            encrypted_text = substitute(text, key)
            print(f"Исходный текст: {text}")
            print(f"Зашифрованный текст: {encrypted_text}")
            print(f"Ключ: {''.join(key.values())}")
        
        elif mode == "расшифровка":
            # Для необходим ключ пользователя сто процентов
            key_input = input("Введите ключ в виде перестановки алфавита: ")
            if len(set(key_input)) != len(alphabet) or any(c not in alphabet for c in key_input):
                print("Некорректный ключ.")
                return
            
            key = dict(zip(alphabet, key_input)) # создание словаря подстановки 
            reversed_key = reverse_key(key) # обратный ключ
            decrypted_text = substitute(text, reversed_key)
            
            # Расшифровали тексти и если что обработали ошибки
            print(f"Исходный текст: {text}")
            print(f"Расшифрованный текст: {decrypted_text}")
            print(f"Ключ: {''.join(key_input)}")
        else:
            print("Некорректный режим.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
