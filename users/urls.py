from django.urls import path
from users.views import UserCreateView, UserDetailDeleteView, UserListView, UserLoginView, UserLogoutView, RequestPasswordResetView, PasswordResetConfirmView
urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='user_create'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('request_password/', RequestPasswordResetView.as_view(),
         name='user_request_password'),
    path('reset_password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='user_reset_password_confirm'),
    path('list/', UserListView.as_view(), name="user_list"),
    path('detail/', UserDetailDeleteView.as_view(), name="user_detail"),
]
