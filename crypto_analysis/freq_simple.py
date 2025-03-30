import operator
from collections import defaultdict


FREQ = {
    ' ': 15.00,
    'О': 10.97, 'Е': 8.45, 'А': 8.01, 'И': 7.35, 'Н': 6.70,
    'Т': 6.26, 'С': 5.47, 'Р': 4.73, 'В': 4.54, 'Л': 4.40,
    'К': 3.49, 'М': 3.21, 'Д': 2.98, 'П': 2.81, 'У': 2.62,
    'Я': 2.01, 'Ы': 1.90, 'Ь': 1.74, 'Г': 1.70, 'З': 1.65,
    'Б': 1.59, 'Ч': 1.44, 'Й': 1.21, 'Х': 0.97, 'Ж': 0.94,
    'Ш': 0.73, 'Ю': 0.64, 'Ц': 0.48, 'Щ': 0.36, 'Э': 0.32,
    'Ф': 0.26, 'Ъ': 0.04, 'Ё': 0.04
}


def frequency_analysis(ciphertext):
    freq = defaultdict(int)
    total = 0
    for char in ciphertext.upper():
        if char in FREQ:
            freq[char] += 1
            total += 1

    sorted_freq = sorted(
        ((k, (v / total) * 100) for k, v in freq.items()),
        key=operator.itemgetter(1),
        reverse=True
    )

    sorted_russian = sorted(
        FREQ.items(),
        key=operator.itemgetter(1),
        reverse=True
    )

    substitution = {}
    for (cipher_char, _), (rus_char, _) in zip(sorted_freq, sorted_russian):
        sub_char = rus_char.lower() if rus_char != ' ' else ' '
        substitution[cipher_char] = sub_char
    
    return substitution


def decrypt(ciphertext, substitution):
    plaintext = []
    for char in ciphertext:
        upper_char = char.upper()
        if upper_char in substitution:
            decrypted = substitution[upper_char]
            plaintext.append(decrypted.lower() if char.islower() else decrypted.upper())
        else:
            plaintext.append(char)
    return ''.join(plaintext)


if __name__ == "__main__":
    # Запрос ввода от пользователя
    ciphertext = input("Введите зашифрованный текст:\n> ")
    
    # Выполнение анализа
    substitution = frequency_analysis(ciphertext)

    # Расшифровка и вывод результата
    decrypted = decrypt(ciphertext, substitution)
    print("\nРезультат расшифровки:")
    print(decrypted)
    