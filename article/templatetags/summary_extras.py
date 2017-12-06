from django.template import Library
from django.template.defaultfilters import stringfilter
import bleach

# import customize module
from article import utils
from mysite.config.settings import dev_settings

register = Library()

allow_content = getattr(dev_settings, 'ALLOWED_CONTENT')


@register.filter(name='banxss')
def bleach_xss(text):
    return bleach.clean(text=text,
                        tags=allow_content['ALLOWED_TAGS'],
                        attributes=allow_content['ALLOWED_ATTRIBUTES'],
                        styles=allow_content['ALLOWED_STYLES'],
                        strip=True)


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
