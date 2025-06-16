from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_project, name='about_project'),
    path('about/core/', views.about_core, name='about_core'),
    path('profile/', views.profile, name='profile'),

    # Boards CRUD
    path('boards/', views.boards_list, name='boards_list'),
    path('boards/create/', views.board_create, name='board_create'),
    path('boards/<int:board_id>/', views.board_detail, name='board_detail'),
    path('boards/<int:board_id>/update/', views.board_update, name='board_update'),
    path('boards/<int:board_id>/delete/', views.board_delete, name='board_delete'),
    path('boards/<int:board_id>/settings/', views.board_settings, name='board_settings'),

    path('boards/<int:board_id>/add-member/', views.board_add_member, name='board_add_member'),
    path('boards/<int:board_id>/remove-member/<int:membership_id>/', views.board_remove_member,
         name='board_remove_member'),

    # Notes
    path('notes/', views.notes_list, name='notes_list'),
    path('boards/<int:board_id>/notes/create/', views.note_create, name='note_create'),
    path('boards/<int:board_id>/notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('notes/<int:note_id>/archive/', views.note_archive, name='note_archive'),
    path('boards/<int:board_id>/notes/<int:note_id>/update/', views.note_update, name='note_update'),
    path('boards/<int:board_id>/notes/<int:note_id>/delete/', views.note_delete, name='note_delete'),

    # Checklist items
    path('checklist-items/<int:item_id>/toggle/', views.toggle_checklist_item, name='toggle_checklist_item'),
]
