from django import template
from courses.forms import CourseForm
from courses.models import Course

register = template.Library()


@register.simple_tag
def course_field():
    return CourseForm()
