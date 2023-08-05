from rules import add_perm

from aleksis.core.util.predicates import has_global_perm, has_person, is_site_preference_set

# View FAQ
view_faq_predicate = is_site_preference_set("hjelp", "public_faq") | (
    has_person & has_global_perm("hjelp.view_faq")
)
add_perm("hjelp.view_faq", view_faq_predicate)

# Ask FAQ question
ask_faq_predicate = has_person & has_global_perm("hjelp.ask_faq")
add_perm("hjelp.ask_faq", ask_faq_predicate)

# Report issue
report_issue_predicate = has_person & has_global_perm("hjelp.report_issue")
add_perm("hjelp.report_issue", report_issue_predicate)

# Add feedback
send_feedback_predicate = has_person & has_global_perm("hjelp.send_feedback")
add_perm("hjelp.send_feedback", send_feedback_predicate)
