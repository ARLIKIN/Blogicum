from django.contrib import admin
from django.views.generic.edit import CreateView
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

from blog.forms import ProfileForm

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path(
            'auth/registration/',
            CreateView.as_view(
                template_name='registration/registration_form.html',
                form_class=ProfileForm,
                success_url=reverse_lazy('blog:index'),
            ),
            name='registration',
        ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'blog.views.page_not_found'
CSRF_FAILURE_VIEW = 'blog.views.csrf_failure'
handler500 = 'blog.views.server_error'
