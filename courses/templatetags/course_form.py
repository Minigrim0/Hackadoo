from django import template
from courses.forms import CourseForm

register = template.Library()

@register.simple_tag
def course_field():
    return CourseForm()
