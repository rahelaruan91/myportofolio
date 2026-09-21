from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm

def show_main(request):
    context = {
        "name": "Rahel Meilinda Aruan",
        "npm": "2506598513",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "I turn research and user insight into interfaces people can navigate without thinking twice,"
            "then bring the design to life pixel by pixel in code."
        ),
        "active_page": "main",
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experiences_json(request)
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [experience.object for experience in experiences]

    context = {
        "name": "Rahel Meilinda Aruan",
        "experience_list": experience_list,
        "active_page": "experience",
    }
    return render(request, "experience.html", context)

def get_experiences_json(request):
    experiences = Experience.objects.all()
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Rahel Meilinda Aruan",
        "form": form,
        "form_title": "Add New Experience",
        "submit_label": "Add Experience",
    }
    return render(request, "experience_form.html", context)

def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Rahel Meilinda Aruan",
        "form": form,
        "form_title": "Edit Experience",
        "submit_label": "Save Changes",
    }
    return render(request, "experience_form.html", context)

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

def show_project(request):
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Rahel Meilinda Aruan",
        "project_list": projects,
        "active_page": "project",
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Rahel Meilinda Aruan",
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

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.POST.get("kode_rahasia") != settings.SECRET_FORM_CODE:
            messages.error(request, "Kode rahasia salah, penghapusan dibatalkan.")
            return redirect("main:show_project")
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")
