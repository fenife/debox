import json
import requests
import uuid
import datetime
from requests import Response
import logging

logger = logging.getLogger(__name__)


def log_response(resp: Response, exc: Exception = None):
    if resp is None and exc is not None:
        logger.error(str(exc))
        return
    method = resp.request.method
    url = resp.request.url
    req_body = resp.request.body
    status = resp.status_code
    resp_body = resp.text
    msg = "\n url:    {url}" \
          "\n method: {m}" \
          "\n body:   {b1}" \
          "\n status: {s}" \
          "\n resp:   {b2}".format(
              m=method, url=url, b1=req_body, s=status, b2=resp_body)
    logger.info(msg)


class HttpClient(object):
    def __init__(self, base_url: str = "", host: str = "", port: int = 80) -> None:
        if not any([base_url, host]):
            raise Exception("base_url or host should not be empty")
        self.base_url = base_url or "http://{h}:{p}".format(h=host, p=port)
        self.session = requests.session()

    def do_request(self, method: str, url: str, need_raise=True, **kwargs) -> Response:
        headers = kwargs.get("headers", {})
        headers.update({
            "Content-Type": "application/json"
        })
        kwargs.update({"headers": headers})
        method = method.upper()
        # dt = datetime.datetime.now()
        resp = exc = None
        try:
            resp = self.session.request(method=method, url=url, **kwargs)
        except Exception as e:
            exc = e
        log_response(resp, exc)
        if need_raise:
            if exc is not None:
                raise exc
            else:
                resp.raise_for_status()
        return resp

    def _get_full_url(self, url):
        return self.base_url + url if self.base_url else url

    def get(self, url: str, **kwargs) -> Response:
        url = self._get_full_url(url)
        return self.do_request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        url = self._get_full_url(url)
        return self.do_request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> Response:
        url = self._get_full_url(url)
        return self.do_request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        url = self._get_full_url(url)
        return self.do_request("DELETE", url, **kwargs)
