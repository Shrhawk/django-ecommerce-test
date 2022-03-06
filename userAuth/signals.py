import datetime

from common.external_apis_info import APIS_INFO
from common.request_helpers import make_request
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def enrich_user_data(sender, **kwargs):
    """
    enrich user data according to his/her Geolocation and Holidays
    And Validate Email
    """
    if kwargs.get('created'):
        ip = kwargs.get('instance').user_ip
        if str(ip) == '127.0.0.1':
            # If app is running on localhost it will return localhost address as our ip
            # for localhost case use Default country code PK
            ip = '101.50.64.0'
        api_url = APIS_INFO['geolocation_api'].format(ip)
        ip_address = make_request(method='get', api_url=api_url, retries=3)
        if not ip_address:
            return
        country_code = ip_address['data']['country_code']
        current_date = datetime.date.today()
        api_url = APIS_INFO['holidays_api']
        data = {
            "country": country_code,
            "year": current_date.year,
            "month": current_date.month,
            "day": current_date.day
        }
        holidays = make_request(method='get', api_url=api_url, data=data, retries=3)
        holidays = holidays.get('data', {})
        try:
            sender.objects.filter(
                pk=kwargs.get('instance').pk
            ).update(holidays=holidays)
        except:
            pass
