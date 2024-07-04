from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views
from . import views_api
app_name = "tcn"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="tcn/registration/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", views.index, name="home"),
    path("manager/newAgent/", views.SignUpView.as_view(), name="newAgent"),
    path("manager/newOffice/", views.CreateOfficeView.as_view(), name="newOffice"),
    path("manager/offices/", views.ListOffices.as_view(), name="listOffices"),
    path("manager/agents/", views.ListAgents.as_view(), name="listAgents"),
    path("client/trackedOffices/", views.ListTrackedOffices.as_view(), name='listTrackedOffices'),
    path('manager/offices/<str:ref_office>/update/', views.UpdateOfficeView.as_view(), name='updateOfficeForm'),
    path('manager/agents/<int:agent_id>/update/', views.UpdateAgentView.as_view(), name='updateAgentForm')
   ,
   # reset password
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='registration/reset_pwd_page.html'), name='password_reset'),
    # api section 
    path('api/status/', views_api.status, name='apiStatus'),
    path('api/windows/<int:number_window>/assign-agent/', views_api.assign_agent_to_window, name='apiWindowAssignAgent'),
    path('api/offices/<str:ref_office>/increment-counter/', views_api.increment_counter, name='incrementCounter'),
    path('api/offices/<int:id_user>/<str:action>/apply', views_api.apply_notify_with_action, name='officesNotifications'),
    path('api/offices/<str:ref_office>/delete', views_api.deleteOffice, name='deleteOffice'),
    path('api/offices/<str:ref_office>/agents/<int:agent_id>/delete/', views_api.deleteAgent, name='deleteAgent'),
     path('api/offices/<str:ref_office>/resetcounters', views_api.resetCounters, name='resetCounters')
]
