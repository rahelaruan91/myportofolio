from main.permissions import is_editor

def roles(request):
    """Sediakan variabel `is_editor` ke semua template (termasuk {% include %})."""
    return {"is_editor": is_editor(request.user)}