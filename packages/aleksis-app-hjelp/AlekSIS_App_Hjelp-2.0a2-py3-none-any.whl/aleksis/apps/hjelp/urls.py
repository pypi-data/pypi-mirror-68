from django.urls import path

from . import views

urlpatterns = [
    path("issues/report/", views.report_issue, name="report_issue"),
    path("feedback/", views.feedback, name="feedback"),
    path("faq/", views.faq, name="faq"),
    path("faq/ask/", views.ask_faq, name="ask_faq"),
    path(
        "issues/get_next_properties/",
        views.issues_get_next_properties,
        name="issues_get_next_properties",
    ),
]
