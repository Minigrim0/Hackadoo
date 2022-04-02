from dal import autocomplete

from courses.models import Course


class CourseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Country.objects.none()

        qs = Course.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
