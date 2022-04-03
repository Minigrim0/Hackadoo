from dal import autocomplete

from courses.models import Course
from users.models import StudentToCourse

class CourseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Course.objects.none()

        qs = [x.course for x in StudentToCourse.objects.filter(student=self.request.user, status="running")]
        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
