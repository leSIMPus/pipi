def aaa(text, shift=3):
    result = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                start = ord('a')
            else:
                start = ord('A')

            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char
    return result

text = input("Введите текст: ")
print(aaa(text))
