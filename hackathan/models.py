from django.db import models
from authenticate.models import User


class Hackathon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathon_images')
    hackathon_image = models.ImageField(upload_to='hackathon_images')
    IMAGE = 'image'
    FILE = 'file'
    LINK = 'link'
    SUBMISSION_TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (FILE, 'File'),
        (LINK, 'Link'),
    ]
    submission_type = models.CharField(
        max_length=5,
        choices=SUBMISSION_TYPE_CHOICES,
        default=IMAGE,
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.IntegerField()

    def __str__(self):
        return self.title


class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    registration_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hackathon')

    def __str__(self):
        return f'{self.user} registered for {self.hackathon}'


class Submission(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField()
    image_submission = models.ImageField(upload_to='submission_images/', null=True, blank=True)
    file_submission = models.FileField(upload_to='submission_files/', null=True, blank=True)
    link_submission = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} submitted by {self.user} for {self.hackathon}'
