from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Rahel Meilinda Aruan",
        "npm": "2506598513",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "I turn research and user insight into interfaces people can navigate without thinking twice,"
            "then bring the design to life pixel by pixel in code."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rahel Meilinda Aruan",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)