import requests
from requests.adapters import HTTPAdapter
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.backends import TokenBackend
from urllib3 import Retry


def make_request(method='get', api_url='', data={}, retries=0):
    """
    Make call to external urls using python request
    :param method: get|post (str)
    :param api_url:
    :param data: data to send in the request (dict)
    :param retries:
    :return:
    """
    retry_strategy = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
        # allowed_methods=frozenset(['GET', 'POST'])
    )
    retry_adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount('http://', retry_adapter)
    session.mount('https://', retry_adapter)
    headers = {'content-type': 'application/json'}
    method = method.lower()

    try:
        if method == 'get':
            response = session.get(api_url, params=data, headers=headers)
        elif method == 'post':
            response = session.post(api_url, data=data, headers=headers)
    except:
        return {'status_code': 500, 'data': 'internal server error'}
    return {'status_code': response.status_code, 'data': response.json()}


def _mutable(user_data):
    try:
        user_data._mutable = True
    except:
        pass
    finally:
        return user_data


def get_current_user(request):
    """
    Get user id from request
    """
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_id = valid_data['user_id']
        return user_id
    except ValidationError as v:
        print("validation error", v)
