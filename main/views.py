from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse

from main.models import Experience, Project
from main.forms import ProjectForm

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
    context = {
        "name": "Rahel Meilinda Aruan",
        "experience_list": Experience.objects.all(),
        "active_page": "experience",
    }
    return render(request, "experience.html", context)

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
        "name": "Rahel",
        "form": form,
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
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")
