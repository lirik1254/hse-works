import pymorphy3

morph = pymorphy3.MorphAnalyzer()


def pluralize_days(days):
    """
    1 день, но 2 дня
    """
    word = morph.parse("день")[0]
    return f"{days} {word.make_agree_with_number(days).word}"


def pluralize_hours(hours):
    """
    1 час, но 2 часа
    """
    word = morph.parse("час")[0]
    return f"{hours} {word.make_agree_with_number(hours).word}"
