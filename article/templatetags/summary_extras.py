from django.template.library import Library
from django.template.defaultfilters import stringfilter
import bleach

# import customized module
from article import my_renderer
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
    renderer = my_renderer.HightlightRenderer()
    markdown = my_renderer.mistune.Markdown(escape=True,
                                            hard_wrap=True,
                                            renderer=renderer)
    return markdown(text)


@register.simple_tag(name='mypluralize')
def pluralize(num):
    if num > 1:
        return 's'
    else:
        return ''
