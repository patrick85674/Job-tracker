import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Require at least one letter and one number
        if (
            not re.search(r'[A-Za-z]', password) or
            not re.search(r'\d', password)
        ):
            raise ValidationError(
                _("Password must include at least one letter and one number."),
                code='password_no_letter_or_number',
            )

    def get_help_text(self):
        return _(
            _("Your password must include at least one letter and one number.")
        )
