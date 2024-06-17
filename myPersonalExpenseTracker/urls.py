from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('member/', views.member, name='member'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('protected/', views.protected_view, name='protected'),
    path('home/', views.home, name='home'),  # Home page
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('manage_accounts/', views.manage_accounts, name='manage_accounts'),
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('manage_tags/', views.manage_tags, name='manage_tags'),
    path('delete_tag/<int:tag_id>/', views.delete_tag, name='delete_tag'),
]