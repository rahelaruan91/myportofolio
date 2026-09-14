from django.shortcuts import render

from main.models import Experience, Project

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
    context = {
        "name": "Rahel Meilinda Aruan",
        "project_list": Project.objects.all(),
        "active_page": "project",
    }
    return render(request, "project.html", context)