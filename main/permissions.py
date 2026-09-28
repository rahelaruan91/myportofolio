"""Aturan hak akses portofolio (satu sumber kebenaran untuk 4 peran).

Pengunjung : hanya membaca data
User biasa : membaca + memberi/membatalkan star.
Editor     : hak user biasa + mengubah data (tanpa membuat/menghapus).
Superuser  : semua hak (pemilik portofolio).
"""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

LOGIN_URL = "main:login"
EDITOR_GROUP_NAME = "Editor"

def is_editor(user):
    """True jika user sudah login dan tergabung dalam Django Group 'Editor'."""
    return user.is_authenticated and user.groups.filter(name=EDITOR_GROUP_NAME).exists()


def can_edit(user):
    """Boleh mengubah data: pemilik (superuser) atau Editor."""
    return user.is_superuser or is_editor(user)


def _require(check):
    """Pembuat decorator: jika belum login -> redirect ke login, jika tidak berhak -> 403."""
    def decorator(view_func):
        @login_required(login_url=LOGIN_URL)
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not check(request.user):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


owner_required = _require(lambda user: user.is_superuser)   # untuk create & delete
editor_required = _require(can_edit)                        # untuk update