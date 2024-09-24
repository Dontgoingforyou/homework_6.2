from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    """
    Фильтр преобразует относительный путь к файлу в полноценный
    """

    if path:
        return f"/media/{path}"
    return "#"


@register.filter()
def truncate_text(value, length=100):
    """
    Фильтр обрезает текст до слова, не превышающего длину. Если длина текста больше 100 символов, добавляет троеточие
    """

    if len(value) <= length:
        return value
    else:
        truncated = value[:length].rsplit(' ', 1)[0]
        return f"{truncated}..."


@register.filter(name='add_class')
def add_class(value, arg):
    """
    Фильтр позвляет динамически добавлять CSS-классы к виджетам полей формы в Django-шаблоне
    """
    try:
        return value.as_widget(attrs={'class': arg})
    except AttributeError:
        return value
