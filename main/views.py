import datetime

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm
from main.permissions import LOGIN_URL, editor_required, owner_required

PORTFOLIO_OWNER = "Rahel Meilinda Aruan"

# ----------------------------------------------------------------------------------------- Section: About Me
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
        "active_page": "main",
        "last_login" : last_login,
    }
    return render(request, "index.html", context)

# ----------------------------------------------------------------------------------------- Section: Experience
def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": PORTFOLIO_OWNER,
        "active_page": "experience",
        "title_query": title_query,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()

    experiences = (Experience.objects.prefetch_related("starred_by").all())

    if title_query:
        experiences = experiences.filter(
            title__icontains=title_query
        )

    data = []

    for experience in experiences:
        starred_users = experience.starred_by.all()

        is_starred = (
            request.user.is_authenticated
            and starred_users.filter(
                pk=request.user.pk
            ).exists()
        )

        starred_by_names = ", ".join(
            user.username for user in starred_users
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category_label": experience.get_category_display(),
                "is_ongoing": experience.is_ongoing,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang "
                    "dapat menambahkan pengalaman."
                )
            },
            status=403,
        )

    form = ExperienceForm(request.POST)

    if form.is_valid():
        experience = form.save()

        return JsonResponse(
            {
                "message": "Pengalaman berhasil ditambahkan.",
                "pk": str(experience.id),
            },
            status=201,
        )

    return JsonResponse(
        {
            "errors": form.errors.get_json_data(),
        },
        status=400,
    )

@login_required(login_url=LOGIN_URL)
@require_POST
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    if experience.starred_by.filter(
        pk=request.user.pk
    ).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)

    return redirect("main:show_experience")

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


# ----------------------------------------------------------------------------------------- Section: Project
def show_project(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": PORTFOLIO_OWNER,
        "active_page": "project",
        "title_query": title_query,
        "form": ProjectForm(),
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
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "subheading": project.subheading,
                "description": project.description,
                "thumbnail": project.thumbnail,
                "project_url": project.project_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

    # projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    # return HttpResponse(projects_json, content_type="application/json")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

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

# ----------------------------------------------------------------------------------------- Section: Authentication
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