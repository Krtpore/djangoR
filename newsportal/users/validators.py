from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

# def username_check(username):
#     # allowed_endnames = ['хороший', 'хорошая']
#     allowed_endnames = ['good', 'best']
#     if not any(endname in username for endname in allowed_endnames):
#         raise ValidationError(
#             _(username, "not allowed") #,params={'username':username}
#         )

def russian_email(email):
    allowed_domains = ['@mail.ru',
                       '@bk.ru',
                       '@yandex.ru']
    if not any(domain in email for domain in allowed_domains):
        raise ValidationError(
            _("%(email) has not allowed domain"),params={'email':email}
        )