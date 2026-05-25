
from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/',include('portfolio.urls')),
    path('', RedirectView.as_view(url='/portfolio/')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/tarefas/', include('tarefas.urls')),
    path('', include('core.urls')),
    
]
