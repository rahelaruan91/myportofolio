import json

from django.test import TestCase, override_settings
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="MediVoice",
            subheading="Accessibility-First Medication Platform for Elderly",
            description="A voice-first medication companion that helps elderly users manage their daily medications more safely and independently.",
            thumbnail="img/medivoice-preview.png",
            project_url="https://www.figma.com/proto/example",
        )

    def test_project_url_is_accessible(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_page(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.subheading)
        self.assertContains(response, self.project.description)
        self.assertContains(response, f'href="{self.project.project_url}"')
        self.assertContains(response, "See more")

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, "Belum ada project yang ditambahkan.")
        self.assertNotContains(response, "project-card")

@override_settings(SECRET_FORM_CODE="rahasia")
class RolePermissionTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="MediVoice", subheading="Tagline", description="Deskripsi",
            thumbnail="img/medivoice-preview.png", project_url="https://example.com",
        )
        self.experience = Experience.objects.create(
            title="Asdos PBP", description="Membantu mahasiswa.", category="part-time",
        )
        self.regular = User.objects.create_user("biasa", password="Pass12345!")
        self.editor = User.objects.create_user("editor", password="Pass12345!")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.owner = User.objects.create_superuser("owner", password="Pass12345!")

        self.create_project_url = reverse("main:create_project")
        self.update_project_url = reverse("main:update_project", args=[self.project.id])
        self.delete_project_url = reverse("main:delete_project", args=[self.project.id])
        self.create_experience_url = reverse("main:create_experience")
        self.update_experience_url = reverse("main:update_experience", args=[self.experience.id])
        self.delete_experience_url = reverse("main:delete_experience", args=[self.experience.id])
        self.star_url = reverse("main:toggle_star", args=[self.project.id])
        self.login_url = reverse("main:login")

        self.project_data = {
            "title": "Judul Baru", "subheading": "Tagline", "description": "Deskripsi",
            "thumbnail": "img/x.png", "project_url": "https://example.com",
            "kode_rahasia": "rahasia",
        }

    # --- Pengunjung tanpa login ---
    def test_anonymous_redirected_to_login(self):
        for url in [self.create_project_url, self.update_project_url,
                    self.create_experience_url, self.update_experience_url]:
            response = self.client.get(url)
            self.assertRedirects(response, f"{self.login_url}?next={url}")

    def test_anonymous_cannot_delete_or_star(self):
        response = self.client.post(self.delete_project_url, {"kode_rahasia": "rahasia"})
        self.assertRedirects(response, f"{self.login_url}?next={self.delete_project_url}",
        fetch_redirect_response=False)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

        self.client.post(self.star_url)
        self.assertEqual(self.project.starred_by.count(), 0)

    # --- User biasa ---
    def test_regular_user_gets_403(self):
        self.client.force_login(self.regular)
        for url in [self.create_project_url, self.update_project_url,
            self.create_experience_url, self.update_experience_url]:
            self.assertEqual(self.client.get(url).status_code, 403)
        response = self.client.post(self.delete_project_url, {"kode_rahasia": "rahasia"})
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    # --- Editor ---
    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_login(self.editor)
        self.assertEqual(self.client.get(self.update_project_url).status_code, 200)
        response = self.client.post(self.update_project_url, self.project_data)
        self.assertRedirects(response, reverse("main:show_project"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Judul Baru")

        self.assertEqual(self.client.get(self.create_project_url).status_code, 403)
        self.assertEqual(self.client.get(self.create_experience_url).status_code, 403)
        response = self.client.post(self.delete_project_url, {"kode_rahasia": "rahasia"})
        self.assertEqual(response.status_code, 403)
        response = self.client.post(self.delete_experience_url, {"kode_rahasia": "rahasia"})
        self.assertEqual(response.status_code, 403)

    # --- Pemilik ---
    def test_owner_can_create_update_delete(self):
        self.client.force_login(self.owner)
        self.client.post(self.create_project_url, self.project_data)
        self.assertEqual(Project.objects.count(), 2)

        response = self.client.post(self.update_project_url, self.project_data)
        self.assertEqual(response.status_code, 302)

        self.client.post(self.delete_project_url, {"kode_rahasia": "rahasia"})
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_owner_can_create_experience(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.create_experience_url, {
            "title": "Magang", "description": "Deskripsi", "category": "internship",
            "ended_at": "", "kode_rahasia": "rahasia",
        })
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Magang").exists())

    # --- Tampilan tombol ---
    def test_controls_hidden_for_regular_user(self):
        self.client.force_login(self.regular)
        response = self.client.get(reverse("main:show_project"))
        for url in [self.create_project_url, self.update_project_url, self.delete_project_url]:
            self.assertNotContains(response, url)

    def test_editor_sees_edit_only(self):
        self.client.force_login(self.editor)
        response = self.client.get(reverse("main:show_project"))
        self.assertContains(response, self.update_project_url)
        self.assertNotContains(response, self.create_project_url)
        self.assertNotContains(response, self.delete_project_url)

    def test_owner_sees_all_controls(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("main:show_project"))
        for url in [self.create_project_url, self.update_project_url, self.delete_project_url]:
            self.assertContains(response, url)

    # --- Star ---
    def test_toggle_star_adds_then_removes(self):
        self.client.force_login(self.regular)
        self.client.post(self.star_url)
        self.assertEqual(self.project.starred_by.count(), 1)
        self.client.post(self.star_url)
        self.assertEqual(self.project.starred_by.count(), 0)

    # --- API ---
    def test_projects_json_uses_usernames_not_internal_ids(self):
        self.project.starred_by.add(self.regular)
        response = self.client.get(reverse("main:get_projects_json"))
        fields = json.loads(response.content)[0]["fields"]
        self.assertEqual(fields["starred_by"], [["biasa"]])
        self.assertNotIn("password", response.content.decode())
        self.assertNotIn("email", response.content.decode())

    # --- Login next ---
    def test_login_redirects_to_safe_next(self):
        response = self.client.post(self.login_url, {
            "username": "biasa", "password": "Pass12345!", "next": self.star_url,
        })
        self.assertRedirects(response, self.star_url, fetch_redirect_response=False)
        self.assertIn("last_login", response.cookies)

    def test_login_ignores_external_next(self):
        response = self.client.post(self.login_url, {
            "username": "biasa", "password": "Pass12345!", "next": "https://evil.example.com/",
        })
        self.assertRedirects(response, reverse("main:show_main"), fetch_redirect_response=False)