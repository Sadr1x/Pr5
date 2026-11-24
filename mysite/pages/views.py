"""Сторінки навчального Django-проєкту."""

from django.shortcuts import render


def index(request):
    """Головна сторінка з описом і трьома посиланнями."""
    return render(request, "pages/index.html")


def about(request):
    """Сторінка з відомостями про практичну роботу."""
    return render(request, "pages/about.html")


def contact(request):
    """Вітає відвідувача за GET-параметром name."""
    name = request.GET.get("name", "").strip()
    return render(request, "pages/contact.html", {"name": name})
