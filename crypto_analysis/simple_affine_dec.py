import math

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def affine_decrypt(ciphertext, a, b, alphabet):
    """
    Расшифровывает текст с использованием ключа (a, b).
    """
    m = len(alphabet)
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        return None
    
    decrypted = []
    for char in ciphertext:
        if char in alphabet:
            y = alphabet.index(char)
            x = (a_inv * (y - b)) % m
            decrypted.append(alphabet[x])
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def get_valid_a(m):
    """Возвращает список допустимых значений 'a' (взаимно простых с m)."""
    return [a for a in range(1, m) if math.gcd(a, m) == 1]

def main():
    # Два алфавита 
    alphabet_options = {
        1: "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",  # Длина 33
        2: "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя"  # Длина 67
    }
    
    print("Выберите алфавит:")
    print("1. Только заглавные буквы")
    print("2. Заглавные, строчные и пробел")
    choice = int(input("Ваш выбор: "))
    alphabet = alphabet_options.get(choice, alphabet_options[1])
    m = len(alphabet)
    print(f"Выбран алфавит длиной {m} символов.")
    
    # Ввод зашифрованного текста
    ciphertext = input("Введите зашифрованный текст: ")
    
    # Перебор ключей
    valid_a = get_valid_a(m)
    total_keys = len(valid_a) * m
    print(f"Перебор {total_keys} ключей...")
    
    for a in valid_a:
        for b in range(m):
            decrypted = affine_decrypt(ciphertext, a, b, alphabet)
            print(f"a = {a}, b = {b}: {decrypted}")

if __name__ == "__main__":
    main()