
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import contact_view
from .import views
from .settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("core.urls")),
    path("",include("accounts.urls")),
    path('contact/', contact_view, name='contact'),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)

