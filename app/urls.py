from django.contrib import admin
from django.urls import path
from userauth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('profile/',views.profile, name='profile'),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)