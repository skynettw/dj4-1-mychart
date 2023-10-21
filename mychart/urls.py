from django.contrib import admin
from django.urls import path
from mysite import views

urlpatterns = [
    path('', views.index),
    path('cut/', views.cut),
    path('wordcloud/', views.wordcloud),
    path('mat/heartcurve/', views.heartcurve),
    path('mat/heartcurve-polar/', views.heartcurve_polar),
    path('mat/bar/', views.mat_bar),
    path('mat/line/', views.mat_line),
    path('mat/scatter/', views.mat_scatter),
    path('mat/3d/', views.mat_3d),
    path('admin/', admin.site.urls),
]
