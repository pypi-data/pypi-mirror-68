from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField

from aleksis.core.mixins import ExtensibleModel
from aleksis.core.util.model_helpers import ICONS


class HjelpGlobalPermissions(ExtensibleModel):
    class Meta:
        managed = False
        permissions = (
            ("view_faq", _("Can view FAQ")),
            ("ask_faq", _("Can ask FAQ question")),
            ("report_issue", _("Can report issues")),
            ("send_feedback", _("Can send feedback")),
        )


class FAQSection(ExtensibleModel):
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    icon = models.CharField(
        max_length=50, blank=True, default="question_answer", choices=ICONS, verbose_name=_("Icon"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("FAQ section")
        verbose_name_plural = _("FAQ sections")


class FAQQuestion(ExtensibleModel):
    question_text = models.TextField(verbose_name=_("Question"))
    icon = models.CharField(
        max_length=50, blank=True, default="question_answer", choices=ICONS, verbose_name=_("Icon"),
    )

    show = models.BooleanField(verbose_name=_("Show"), default=False)

    answer_text = RichTextField(verbose_name=_("Answer"))

    section = models.ForeignKey(
        FAQSection,
        on_delete=models.CASCADE,
        blank=True,
        related_name="questions",
        verbose_name=_("FAQ Section"),
    )

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = _("FAQ question")
        verbose_name_plural = _("FAQ questions")


class IssueCategory(ExtensibleModel):
    name = models.CharField(max_length=40, verbose_name=_("Name"))
    icon = models.CharField(
        max_length=50, blank=True, default="bug_report", choices=ICONS, verbose_name=_("Icon"),
    )
    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Parent category"),
    )
    free_text = models.BooleanField(verbose_name=_("Free text input allowed"), default=False)
    placeholder = models.CharField(max_length=100, verbose_name=_("Placeholder"), blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.free_text:
            IssueCategory.objects.filter(parent=self).delete()
        super(IssueCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Issue category")
        verbose_name_plural = _("Issue categories")
