from django.db import models

# Create your models here.

list_tags = [
    ('python', 'Python'),
    ('SEO', 'SEO'),
    ('WEB DEVELOPMENT', 'WEB DEVELOPMENT'),
    ('python SEO', 'PYTHON SEO'),
    ('knowledge python', 'Knowledge Python'),
    ('web scraping', 'Web Scraping'),
    ('python scraping', 'Python Scraping'),
    ('python crawl', 'Python Crawl'),
    ('programing', 'Programing'),
    ('other', 'Other'),
]


def convert_title_encode(string):
    import re
    patterns = {
        '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêềếểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        '[ùúủũụưừứửữự]': 'u',
        '[ỳýỷỹỵ]': 'y'
    }
    result = string
    for key, value in patterns.items():
        result = re.sub(key, value, result)
        result = re.sub(key.upper(), value.upper(), result)
    return result.replace(' ', '-')


class Blog(models.Model):
    title = models.CharField(max_length=300)
    image_blog = models.ImageField(upload_to='image_blogs', blank=True)
    content_blog = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=200)
    tags = models.CharField(choices=list_tags, max_length=200)

    def __str__(self):
        return self.title

    @property
    def encode_title(self):
        return convert_title_encode(self.title)


