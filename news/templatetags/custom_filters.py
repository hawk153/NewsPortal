from django import template

register = template.Library()


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Должен быть текст!')

    nasty_list = [
        'редиска',
        'матрица',
        'цветы',
        'время',
        'место',
        'авто',
    ]

    for item in nasty_list:
        if item in value.lower():
            c_index = value.lower().index(item)
            value = value.replace(value[c_index:c_index+len(item)], f"{value[c_index]}{'*' * (len(item) - 1)}")
    return value