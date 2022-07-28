from .models import Account, Course, Payment


def qarzdor():
    accounts = Account.objects.all()

    for i in accounts.all():
        i.tolov_oyi
