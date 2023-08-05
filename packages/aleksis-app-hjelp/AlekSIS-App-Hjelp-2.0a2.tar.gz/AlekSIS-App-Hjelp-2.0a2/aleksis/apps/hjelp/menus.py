from django.utils.translation import ugettext_lazy as _

MENUS = {
    "NAV_MENU_CORE": [
        {
            "name": _("Support"),
            "url": "#",
            "icon": "help_circle",
            "root": True,
            "submenu": [
                {
                    "name": _("Report an issue"),
                    "url": "report_issue",
                    "icon": "bug_report",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.has_person",
                    ],
                },
                {
                    "name": _("Give feedback"),
                    "url": "feedback",
                    "icon": "message_alert",
                    "validators": [
                        "menu_generator.validators.is_authenticated",
                        "aleksis.core.util.core_helpers.has_person",
                    ],
                },
                {"name": _("FAQ"), "url": "faq", "icon": "question_answer",},
            ],
        }
    ]
}
