from django import template
from django.shortcuts import render

from catalog.models import Blog

register = template.Library()


@register.filter()
def media_filter (path):
    if path:
        return f'/media/{path}'
    return  "#"


# def is_published_filter(blog_objects):
#     if blog_objects:
#         return Blog.objects.filter(is_published=True)
#     else:
#         return "#"