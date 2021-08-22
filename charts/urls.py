# from worker.make_data import pick_progress
# from charts.forms import addToPortfolio
from os import name
from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.index, name='charts'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('loginForm', views.loginForm),
    path('loginForm', views.loginForm, name='loginForm'),
    path('login', views.login_,name='login_'),
    path('logout', views.logout_, name='logout_'),
    path('test', views.test, name='test'),
    path('addToIndex/<str:pk>/', views.addToIndex, name='addToIndex_'),
    path('rmFromIndex', views.rmFromIndex, name='rmFromIndex'),
    path('workers', views.workers, name='workers'),
    # API V2 
    path('updateHistoricalData', views.updateHistoricalData, name="historicalUpdate"),
    path('statsUpdate', views.statsUpdate, name='statsUpdate'),
    path('updateRowsInDb', views.updateRowsInDb, name='updateDbRows'),
    path('updateCharts', views.updateCharts_, name='updateCharts'),
    path('progress_', views.progress_, name='prog'),
    # path('<int:stk_id>/', views.detail, name='detail')
]