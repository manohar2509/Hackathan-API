from django.urls import path
from .views import GetHackathons, CreateHackathan, RegistrationToHackathan, CreateSubmission, GetSubmissions, GetRegisteredHackathons, GetRegistrations
urlpatterns = [
    path('', GetHackathons.as_view()),
    path('create/', CreateHackathan.as_view()),
    path('register/', RegistrationToHackathan.as_view()),
    path('registrations/', GetRegistrations.as_view()),
    path('hackathon/submissions/submit/', CreateSubmission.as_view()),
    path('hackathon/submissions/', GetSubmissions.as_view()),
    path('registered/', GetRegisteredHackathons.as_view()),
]