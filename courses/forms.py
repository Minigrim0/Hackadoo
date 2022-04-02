from dal import autocomplete

from django import forms
import courses.models as models


class CourseForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=models.Course.objects.all(), required=True,
        widget=autocomplete.ModelSelect2(url='course_autocomplete')
    )
