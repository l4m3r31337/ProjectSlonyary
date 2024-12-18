from django.urls import path
from . import views


urlpatterns = [
    path('', views.auth, name='auth'),
    path('reg.html', views.registration, name='reg'),
    path('logout/', views.logout_view, name='logout'),

    path('profile.html', views.profile, name='profile'),
    path('index.html', views.index, name='index'),
    path('drafts.html', views.drafts, name='drafts'),
    path('constructor.html', views.constructor, name='constructor'),
    path('edit_internship/<int:id>/', views.edit_internship, name='edit_internship'),

    path('profile1.html', views.profile1, name='profile1'),
    path('index1.html', views.index1, name='index1'),
    path('cards.html', views.cards, name='cards'),
    path('card/<int:id>/', views.card, name='card'),
    path('internships_list.html', views.internships_list, name='internships_list'),
    path('internship/<int:id>/', views.internship, name='internship')
]