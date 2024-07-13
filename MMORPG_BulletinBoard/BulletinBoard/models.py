from django.conf import settings
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


CATEGORY_CHOICES = (
    ('TANK', 'Танки'),
    ('HEAL', 'Хилы'),
    ('DAMAGE', 'ДД'),
    ('TRADE', 'Торговцы'),
    ('GUILD', 'Гилдмастеры'),
    ('QUEST', 'Квестгиверы'),
    ('BLACKSMITH', 'Кузнецы'),
    ('LEATHERWORK', 'Кожевники'),
    ('ALCHEMY', 'Зельевары'),
    ('SPELLMASTER', 'Мастера заклинаний'),
)

STATUS_CHOICES = (
    ('PENDING', 'Ожидает рассмотрения'),
    ('ACCEPTED', 'Принят'),
)


class Ad(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    adCategory = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = RichTextUploadingField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class Response(models.Model):
    responseAd = models.ForeignKey(Ad, on_delete=models.CASCADE)
    responseUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f'{self.responseUser}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.responseAd_id)])


