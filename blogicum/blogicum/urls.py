from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls')),
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', views.register, name='registration'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('500test/', views.trigger_error),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
