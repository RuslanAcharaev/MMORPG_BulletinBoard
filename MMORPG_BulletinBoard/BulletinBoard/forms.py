from django import forms
from django.core.exceptions import ValidationError

from .models import Ad, Response


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = [
            'title',
            'adCategory',
            'text',
        ]

        labels = {
            'title': 'Заголовок',
            'adCategory': 'Категория',
            'text': 'Текст объявления',
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )

        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Текст не может быть менее 20 символов."
            })

        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы"
            )
        return title


class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response
        fields = [
            'text',
        ]

        labels = {
            'text': 'Текст отклика',
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")

        if text is not None and len(text) < 10:
            raise ValidationError({
                "text": "Текст не может быть менее 10 символов."
            })

        return cleaned_data
