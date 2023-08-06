def get_request_headers():
    from connexion import request
    try:
        headers = request.headers
    except RuntimeError:
        headers = None
    return headers


def get_request_access_token():
    headers = get_request_headers()
    token = None
    if headers is not None and headers.get('Authorization') is not None:
        token = headers['Authorization'].split(' ')[-1]
    return token


def safe_json_request(method, url, **kwargs):
    """Convenience function for calling external APIs to simplify error handling.

    :param method: HTTP methond (GET, POST, PUT, etc.)
    :param url: Request URL.
    :param kwargs: Additional parameters. See requests.request for details.
    :return: tuple of status_code and json body as a python dict
    """
    from tenacity import retry, stop_after_attempt, before_log
    from requests import HTTPError, ConnectionError
    from logging import getLogger, WARNING
    import json
    logger = getLogger()
    status_code = None
    js = dict()

    @retry(stop=stop_after_attempt(3), reraise=True,
           before=before_log(logger=logger, log_level=WARNING))
    def make_request():
        import requests

        from requests.exceptions import HTTPError
        r = requests.request(method=method, url=url, **kwargs)
        if r.status_code >= 500:
            raise HTTPError(
                json.dumps(
                    dict(
                        status_code=r.status_code,
                        response=format_response_body(response=r)
                    )
                )
            )
        return r

    try:
        response = make_request()
    except ConnectionError:
        pass
    except HTTPError as exc:
        resp = json.loads(exc.args[0])
        status_code = resp['status_code']
        js = resp['response']
    else:
        status_code = response.status_code
        js = format_response_body(response=response)

    return status_code, js


def format_response_body(response):
    js = dict()
    try:
        js = response.json()
    except ValueError:
        js['content'] = response.text
    return js
