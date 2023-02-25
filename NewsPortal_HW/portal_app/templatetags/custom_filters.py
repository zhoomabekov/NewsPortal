from django import template

register = template.Library()

@register.filter()
def censor(value):
    # представим, что слова 'программирования', 'стандарт', 'Chrome' являются нецензурными и их нужно отфильтровать
    if 'программирования' in value:
        value = value.replace('программирования', 'п***************')
    elif 'стандарт' in value:
        value = value.replace('стандарт', 'с*******')
    elif 'Chrome' in value:
        value = value.replace('Chrome', 'C*****')

    return value