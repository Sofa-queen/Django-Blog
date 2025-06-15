from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'