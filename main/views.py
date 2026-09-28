import datetime

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm
from main.permissions import LOGIN_URL, editor_required, owner_required

PORTFOLIO_OWNER = "Rahel Meilinda Aruan"

# ---------------------------------------------------------------- Section: About Me
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Rahel Meilinda Aruan",
        "npm": "2506598513",
        "study_program": "Information System",
        "bio": (
            "I turn research and user insight into interfaces people can navigate without thinking twice,"
            " then bring the design to life pixel by pixel in code."
        ),
        # "active_page": "main",
        "last_login" : last_login,
    }
    return render(request, "index.html", context)

# ---------------------------------------------------------------- Section: Experience
def show_experience(request):
    json_response = get_experiences_json(request)
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [experience.object for experience in experiences]

    context = {
        "name": PORTFOLIO_OWNER,
        "experience_list": experience_list,
        "active_page": "experience",
    }
    return render(request, "experience.html", context)

def get_experiences_json(request):
    experiences = Experience.objects.all()
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

@owner_required
def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": PORTFOLIO_OWNER,
        "form": form,
        "form_title": "Add New Experience",
        "submit_label": "Add Experience",
    }
    return render(request, "experience_form.html", context)

@editor_required
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": PORTFOLIO_OWNER,
        "form": form,
        "form_title": "Edit Experience",
        "submit_label": "Save Changes",
    }
    return render(request, "experience_form.html", context)

@owner_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.POST.get("kode_rahasia") != settings.SECRET_FORM_CODE:
            messages.error(request, "Kode rahasia salah, penghapusan dibatalkan.")
            return redirect("main:show_experience")
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


# ---------------------------------------------------------------- Section: Project
def show_project(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": PORTFOLIO_OWNER,
        "project_list": projects,
        "active_page": "project",
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

@owner_required
def create_project(request):
    # Dua baris berikut yang ditambahkan pada langkah ini.
    # Cek apakah akun yang sedang login adalah superuser (admin/kamu);
    # kalau bukan, hentikan permintaannya dengan 403.
    # if not request.user.is_superuser:
    #     raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": PORTFOLIO_OWNER,
        "form": form,
        "form_title": "Add New Project",
        "submit_label": "Add Project",
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

@owner_required
def delete_project(request, project_id):
    # Dua baris berikut yang ditambahkan pada langkah ini.
    # Cek apakah akun yang sedang login adalah superuser (admin/kamu);
    # kalau bukan, hentikan permintaannya dengan 403.
    # if not request.user.is_superuser:
    #     raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.POST.get("kode_rahasia") != settings.SECRET_FORM_CODE:
            messages.error(request, "Kode rahasia salah, penghapusan dibatalkan.")
            return redirect("main:show_project")
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

@editor_required
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_project")

    context = {
        "name": PORTFOLIO_OWNER,
        "form": form,
        "form_title": "Edit Project",
        "submit_label": "Save Changes",
    }
    return render(request, "projects_form.html", context)

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url=LOGIN_URL)
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if project.starred_by.filter(pk=request.user.pk).exists():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")

# ---------------------------------------------------------------- Section: Authentication
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": PORTFOLIO_OWNER,
        "form": form,
    }
    return render(request, "register.html", context)

def _get_safe_next_url(request):
    """Ambil parameter `next` hanya jika mengarah ke host kita sendiri (mencegah open redirect)."""
    next_url = request.POST.get("next") or request.GET.get("next", "")

    is_safe = url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    )
    return next_url if is_safe else ""

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    next_url = _get_safe_next_url(request)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect(next_url or "main:show_main")
        response.set_cookie(
            'last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        return response

    context = {
        "name": PORTFOLIO_OWNER,
        "form": form,
        "next": next_url
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response