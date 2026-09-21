from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, CharField, PasswordInput

from main.models import Project, Experience

class ProjectForm(ModelForm):
    kode_rahasia = CharField(
        label="Kode Rahasia",
        widget=PasswordInput(attrs={"placeholder": "Masukkan kode rahasia.."}),
    )
    
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
            "subheading" : "Tagline Proyek",
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

    def clean_kode_rahasia(self):
        code = self.cleaned_data.get("kode_rahasia")
        if code != settings.SECRET_FORM_CODE:
            raise ValidationError("Kode rahasia salah.")
        return code

class ExperienceForm(ModelForm):
    kode_rahasia = CharField(
        label="Kode Rahasia",
        widget=PasswordInput(attrs={"placeholder": "Masukkan kode rahasia.."}),
    )

    class Meta:
        model = Experience
        fields = ["title", "description", "category", "ended_at"]

        labels = {
            "title": "Judul Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "ended_at": "Tanggal Selesai (kosongkan jika masih berlangsung)",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Masukkan Pengalamanmu Disini.."}),
            "description": Textarea(attrs={"placeholder": "Ceritakan Pengalamanmu Disini..", "rows": 3}),
            "category": Select(choices=[("", "Pilih Kategori Pengalamanmu Disini..")] + list(Experience.EXPERIENCE_CHOICES)),
            "ended_at": TextInput(attrs={"placeholder": "Masukkan Tanggal Pengalaman Berakhir Disini.."})
        }

    def clean_kode_rahasia(self):
        code = self.cleaned_data.get("kode_rahasia")
        if code != settings.SECRET_FORM_CODE:
            raise ValidationError("Kode rahasia salah.")
        return code