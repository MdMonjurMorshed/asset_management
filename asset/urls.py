from django.urls import path
from .views import *
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from asset.asset_view.asset_view import AssetTabeView

def trigger_error(request):
    division_by_zero = 1 / 0
urlpatterns=[
    path('',HomeView.as_view(),name='home'),
    path('signup/',user_create.as_view(),name='signup'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('change-pass',Change_Password.as_view(),name='change-pass'),
    path('password-reset',PasswordResetView.as_view(template_name='userveryfy/pass_reset.html'),name='pass-reset'),
    path('password-reset-done',PasswordResetDoneView.as_view(template_name='userveryfy/reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='userveryfy/reset_confirm.html'),name='password_reset_confirm'),
    path('pasword-reset-complete',PasswordResetCompleteView.as_view(template_name='userveryfy/reset_complete.html'),name='password_reset_complete'),

    # URLS FOR ASSET
    path('create-asset',AssetCreateView.as_view(),name='create-asset'),
    path('view-asset',AssetTabeView.as_view(),name='asset-view'),

    # URLS FOR UPDATE_ASSETS MODEL
    path('update-asset',UpdateAssetView.as_view(),name='update-asset'),

    # URLS FOR EMPLOYEE
    path('create-employee',EmployeeCreateView.as_view(),name='create-employee'),

    # URLS FOR ASSET ASIGN
    path('asset-asign',AssetAsignView.as_view(),name='asset-asign'),

    # URLS FOR ASSET RETURN
    path('asset-return',AssetReturnView.as_view(),name='asset-return'),
    path('filter-data',ReturnAssetAjax.as_view(),name='filter-data'),
    
    # URL for sentry
    path('sentry-debug/', trigger_error),
    path('get-all',GetAll.as_view(),name='get_all'),


]