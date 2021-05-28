from django.urls import path
from . import views

urlpatterns = [
    path('api/progress', views.get_progress, name='progress')
    # path('<int:stk_id>/', views.detail, name='detail')
]