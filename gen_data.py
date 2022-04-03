from users.models import User, StudentToCourse
import courses.models as cmodels
import secrets
import random


for x in range(100):
    user = User.objects.create(username=secrets.token_hex(20))

for x in range(3):
    univ = cmodels.University.objects.create(name=secrets.token_hex(20))

for x in range(20):
    unif = cmodels.University.objects.all().order_by('?').first()
    faculty = cmodels.Faculty.objects.create(name=secrets.token_hex(20), university=unif)

for x in range(100):
    faculty = cmodels.Faculty.objects.all().order_by('?').first()
    random_num = random.randint(100, 500)
    course = cmodels.Course.objects.create(name=f'INFO-F-{random_num}', faculty=faculty, ects=random.randint(1, 15))

for user in User.objects.all():
    for x in range(7):
        course = cmodels.Course.objects.all().order_by('?').first()
        user.courses.add(course)
        s2c = StudentToCourse.objects.get(student=user, course=course)
        s2c.grade = random.randint(0,20)
        s2c.difficulty = random.randint(0,10)
        s2c.study_time = random.randint(0,150)
        s2c.save()

