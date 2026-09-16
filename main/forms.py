from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "subheading",
            "description",
            "thumbnail",
            "project_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "subheading:" "Tagline Proyek"
            "description": "Deskripsi Proyek",
            "thumbnail": "Gambar Proyek",
            "project_url": "Link Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Masukkan Nama Proyekmu disini..",
                    "maxlength": 255,
                }
            ),
            "subheading": TextInput(
                attrs={
                    "placeholder": "Masukkan Tagline Proyekmu disini..",
                    "rows": 3,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu disini..",
                    "rows": 3,
                }
            ),
            "thumbnail": TextInput(
                attrs={
                    "placeholder": "Masukkan Gambar Proyekmu disini..",
                    "rows": 3,
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "Masukkan Link Proyekmu disini..",
                    "rows": 3,
                }
            ),
            
        }