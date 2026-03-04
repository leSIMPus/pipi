import string

def analyze_text(raw_text: str) -> dict[str, int | float]:
    """Удаляет знаки препинания, разбивает текст на слова по пробелам.
    Возвращает статистику по тексту.

    :param raw_text: Сырой текст, который может содержать лишние пробелы, знаки препинания и разный регистр
    :type raw_text: str
    :return: Словарь со статистикой
    :rtype: int | float

    Пример использования в main.py
    """
    text = raw_text.lower()

    clean_text = str.maketrans('', '', string.punctuation)
    text = text.translate(clean_text)

    words = text.split()

    total_words = len(words)
    unique_words = len(set(words))

    if total_words > 0:
        total_length = sum(len(word) for word in words)
        avg_word_length = round(total_length / total_words, 2)
    else:
        avg_word_length = 0.0

    return {
        'total_words': total_words,
        'unique_words': unique_words,
        "avg_word_length": avg_word_length
    }
