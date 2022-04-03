from django import template

register = template.Library()

@register.simple_tag
def user_running_courses(user):
    return user.coureses_followed
