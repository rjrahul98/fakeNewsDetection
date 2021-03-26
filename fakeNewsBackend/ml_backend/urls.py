from django.contrib import admin
from django.urls import path
from . import views
from .views import Get_predictions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('predict/', Get_predictions.as_view(), name='get_prediction')
]
