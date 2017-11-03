from django.template import Library
from django.template.defaultfilters import stringfilter

# import customize module
from article import utils

register = Library()


@register.filter(name='md')
@stringfilter
def md(text):
    """
    use this function to preview homepage article list with markdown style
    :param text: origin text
    :return: markdown object
    """
    renderer = utils.HightlightRenderer()
    markdown = utils.mistune.Markdown(escape=True, hard_wrap=True,
                                      renderer=renderer)
    return markdown(text)
