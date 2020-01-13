
import re

from django.conf import settings
from django.utils.text import slugify
from unidecode import unidecode


class ArticleCleanedMixin:

    def clean_data(self):
        self.slug = slugify(unidecode(self.title))[:100]
        if not self.tags:
            self.tags = "untagged"
        else:
            self.tags = re.sub(
                settings.TAGS_FILTER_PATTERN, "", self.tags
            ).strip(",")
