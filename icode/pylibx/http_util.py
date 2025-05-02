import json
import requests
import uuid
import datetime
from requests import Response
import logging

logger = logging.getLogger(__name__)


class HttpResult(object):
    def __init__(
        self,
        dt: datetime.datetime,
        resp: Response,
        exc: Exception
    ) -> None:
        self.dt: datetime.datetime = dt
        self.resp: Response = resp
        self.exc: Exception = exc
        self._resp_body = None

    def log_msg(self):
        if self.resp is None and self.exc is not None:
            return str(self.exc)
        method = self.resp.request.method
        url = self.resp.request.url
        req_body = self.resp.request.body
        status = self.resp.status_code
        resp_body = self.resp.text
        msg = "\n url:    {url}" \
              "\n method: {m}" \
              "\n body:   {b1}" \
              "\n status: {s}" \
              "\n resp:   {b2}".format(
                  m=method, url=url, b1=req_body, s=status, b2=resp_body)
        return msg

    def json(self):
        r = {"dt": str(self.dt)}
        r.update(self.resp_info())
        return json.dumps(r)

    def curl(self):
        return self._get_curl_code_snippet()

    def _get_curl_code_snippet(self):
        """
        curl -i -X POST 'service.local:8000/api/v1/user/signup' \
        --header 'Content-Type: application/json' \
        -d '{
            "name": "user1",
            "password": "xxx"
        }'
        """
        req = self.req
        if not req:
            return "curl: None"
        url = self.url
        params = []
        if req.get('params'):
            for k, v in req['params'].items():
                params.append(f"{k}={v}")
        if params:
            url += ','.join(params)
        s = f"curl -i -X {self.method} '{self.url}'"
        if req.get('headers'):
            for k, v in req['headers'].items():
                s += f" \\\n--header '{k}: {v}' "
        if req.get('body'):
            s += f" \\\n-d '{json.dumps(req['body'], indent=2)}'"
        return s


class HttpClient(object):
    def __init__(self, base_url: str = "", host: str = "", port: int = 80) -> None:
        if not any([base_url, host]):
            raise Exception("base_url or host should not be empty")
        self.base_url = base_url or "http://{h}:{p}".format(h=host, p=port)
        self.session = requests.Session()

    def do_request(self, method: str, url: str, need_raise=True, **kwargs) -> Response:
        headers = kwargs.get("headers", {})
        headers.update({
            "Content-Type": "application/json"
        })
        kwargs.update({"headers": headers})
        method = method.upper()
        dt = datetime.datetime.now()
        resp = exc = None
        try:
            resp = self.session.request(method=method, url=url, **kwargs)
        except Exception as e:
            exc = e
        result = HttpResult(dt=dt, resp=resp, exc=exc)
        logger.info(result.log_msg())
        if need_raise:
            if exc is not None:
                raise exc
            else:
                resp.raise_for_status()
        return resp

    def _get_full_url(self, url):
        return self.base_url + url if self.base_url else url

    def get(self, url: str, **kwargs) -> HttpResult:
        url = self._get_full_url(url)
        return self.do_request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> HttpResult:
        url = self._get_full_url(url)
        return self.do_request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> HttpResult:
        url = self._get_full_url(url)
        return self.do_request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> HttpResult:
        url = self._get_full_url(url)
        return self.do_request("DELETE", url, **kwargs)
