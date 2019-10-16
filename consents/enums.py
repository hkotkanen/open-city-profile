from django.utils.translation import ugettext_lazy as _

CONSENT_PURPOSE = (
    (
        "any",
        _(
            "Helsinki city employees can access your data in order to provide services to you."
        ),
    ),
    (
        "proactive",
        _(
            "Helsinki city employees can access your data to proactively offer you services."
        ),
    ),
    (
        "youth_work",
        _("Youth officials can access your data while providing youth services"),
    ),
)
