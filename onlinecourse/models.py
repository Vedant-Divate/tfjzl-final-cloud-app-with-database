"""Data models for the OnlineCourse app: courses, lessons, exam and submissions."""

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Course(models.Model):
    """An online course with lessons and an exam."""
    name = models.CharField(max_length=100, default='Online Course')
    description = models.CharField(max_length=500, default='Course description')
    pub_date = models.DateField(default=now)
    total_enrollment = models.IntegerField(default=0)

    def __str__(self):
        return f"Course: {self.name}"


class Lesson(models.Model):
    """A lesson belonging to a course."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Lesson')
    content = models.TextField(default='Lesson content')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Lesson: {self.title}"


class Enrollment(models.Model):
    """Links a user to a course they enrolled in."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=20, default='audit')

    def __str__(self):
        return f"Enrollment: {self.user} in {self.course.name}"


class Question(models.Model):
    """An exam question attached to a course, worth a grade."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, default='Question')
    question_grade = models.IntegerField(default=1)

    def __str__(self):
        return f"Question: {self.content}"

    def is_get_score(self, selected_ids):
        """Return True when the selected choice ids exactly match the correct ones."""
        correct_ids = set(
            self.choice_set.filter(is_correct=True).values_list('id', flat=True)
        )
        return correct_ids == set(int(i) for i in selected_ids)


class Choice(models.Model):
    """A possible answer choice for a question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, default='Choice')
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Choice: {self.content}"


class Submission(models.Model):
    """A learner's exam attempt: chosen choices per question."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission: {self.enrollment.user} for {self.enrollment.course.name}"
