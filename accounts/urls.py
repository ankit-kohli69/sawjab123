from django.conf.urls import url,include
from . import views
from django.contrib.auth.views import (
										password_reset,
										password_reset_done,
										password_reset_confirm,
                                        password_reset_complete,
									)
urlpatterns = [
    url(r"^login/$",views.LoginRegisterView.as_view(),name="login"),
    url(r"^logout/$",views.LogoutView.as_view(),name="logout"),
    # url(r"^register/$",views.RegisterView.as_view(),name="register"),
    url(r"^profile/(?P<username>\w+)$",views.ProfileAnswerView.as_view(),name="profile"),
    url(r"^profile/(?P<username>\w+)/questions$",views.ProfileQuestionView.as_view(),name="profile-questions"),
    url(r"^profile/(?P<username>\w+)/followers$",views.ProfileFollowersView.as_view(),name="profile-followers"),
    url(r"^profile/(?P<username>\w+)/following$",views.ProfileFollowingView.as_view(),name="profile-following"),
    url(r"^profile/(?P<username>\w+)/update$",views.profile_update,name="profile-update"),
    url(r"^profile/edit/$",views.ProfileUpdateView.as_view(),name="profile_edit"), 
    url(r"^follow/$",views.follow_user,name="follow"), 
    url(r"^change-password/$",views.change_password,name="change-password"),
    url(r'^reset-password/$',password_reset,{'template_name':"accounts/password_reset.html","post_reset_redirect":"accounts:password_reset_done","email_template_name":"accounts/reset_password_email.html"},name="password_reset"),
    url(r'^reset-password/done/$',password_reset_done,{"template_name":"accounts/reset_password_done.html"},name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',password_reset_confirm,{"template_name":"accounts/reset_password_confirm.html","post_reset_redirect":"accounts:password_reset_complete"},name='password_reset_confirm'),
    url(r'^reset-password/complete/$',password_reset_complete,{"template_name":"accounts/reset_password_complete.html"},name='password_reset_complete'),
]
