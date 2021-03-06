from django.urls import path, include
from users import views, auth_token_views

app_name = 'users'

user_patterns = [
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('edit', views.EditUserView.as_view(), name='edit'),
    path('edit/password', views.EditPasswordView.as_view(), name='edit_password'),
    path('delete', views.DeleteUserView.as_view(), name='delete'),
    path('takeout', views.TakeoutDownloadUserView.as_view(), name='takeout'),

    # Homes
    path('home/<int:year>', views.DownloadFinalHomeView.as_view(), name='download-final-home'),

    # Impersonate (django-hijack)
    path('impersonate', views.ImpersonateView.as_view(), name='impersonate'),
]

auth_token_patterns = [
    path('authorize', auth_token_views.AuthorizeView.as_view(), name='token-authorize'),
    # Internal to Prologin server, access should be restricted to internal IPs by nginx
    path('token', auth_token_views.AccessTokenView.as_view(), name='token-access'),
    path('refresh', auth_token_views.RefreshTokenView.as_view(), name='token-refresh'),
]

urlpatterns = [
    # User profile, view and edit
    path('<int:pk>/', include(user_patterns)),

    # Auth token stuff
    path('auth/', include(auth_token_patterns)),

    # Login and logout
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),

    # Search
    path('search/suggest', views.UserSearchSuggestView.as_view(), name='search-suggest'),

    # Password reset
    path('password/reset/ask', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>',
         views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Register and activate views
    path('register', views.RegistrationView.as_view(), name='register'),
    path('activate/<slug>', views.ActivationView.as_view(), name='activate'),

    # Mailing unsubscribe
    path('unsubscribe', views.UnsubscribeView.as_view(), name='unsubscribe'),
]
