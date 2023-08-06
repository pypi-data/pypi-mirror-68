import requests


from os import getenv
from time import time
from copy import deepcopy
from typing import List, Union
from .user_agents import user_agents_list


class BadProxyError(Exception):
    """Custom Exception class."""
    def __init__(self):
        pass


class Downloader:
    """This class allows to process 'GET' and 'POST' requests.

       Sets arguments for request -> makes request with args -> returns response and response content.
    """

    def __init__(self, use_proxy=True, use_session=False, error_status_codes=[]) -> None:
        self.attempts = 5
        self.user_agent = None
        self.request_maker = None
        self.user_agents_list = user_agents_list

        self.use_proxy = use_proxy
        self.use_session = use_session
        self.error_status_codes = error_status_codes

        self.initialize_request_maker()

    def initialize_request_maker(self) -> None:
        """Session initializing.

        @:param self:
        @:type self: Downloader

        Enables session for requests if self.use_session else all requests without session.

        @:returns: None
        @:rtype: NoneType
        """

        if self.use_session:
            self.request_maker = requests.Session()
            # raise max pool size for use bigger thread pool size
            a = requests.adapters.HTTPAdapter(pool_maxsize=9999)
            self.request_maker.mount('https://', a)
        else:
            self.request_maker = requests

    def create_request(self, method, url, params={}, data={}, cookies={}, headers={}, timeout=60, return_response=False,
                       return_response_text=False):
        """ Manage settings for 'GET' or 'POST' request.

        @:param self:
        @:param method: request method
        @:param url: URL
        @:param params: params for 'GET' request
        @:param data: data for 'POST' request
        @:param cookies: request cookies
        @:param headers: request headers
        @:param timeout: request timeout
        @:param return_response: enable to return response object
        @:param return_response_text: enable to return analog of response.text
        @:type self: Downloader
        @:type method: str
        @:type url: str
        @:type params: dict
        @:type data: dict
        @:type cookies: dict
        @:type headers: dict
        @:type timeout: int
        @:type return_response: bool
        @:type return_response_text: bool

        @:returns: tuple of response and response content
        @:rtype: tuple
        """

        headers = deepcopy(headers)
        attempts = self.attempts
        while attempts > 0:
            user_agent = self.get_user_agent()
            headers.update({'User-Agent': user_agent})

            attempts -= 1
            raw_proxy = getenv('LOCAL_PROXY') if self.use_proxy else None
            try:
                response, response_text = self.request_to_page(proxy=raw_proxy,
                                                               method=method,
                                                               url=url,
                                                               params=params,
                                                               cookies=cookies,
                                                               data=data,
                                                               headers=headers,
                                                               timeout=timeout,
                                                               return_response=return_response,
                                                               return_response_text=return_response_text)

                return response, response_text
            except Exception as e:
                if isinstance(e, BadProxyError):
                    attempts += 1

    def request_to_page(self, proxy: str, return_response: bool = False, return_response_text: bool = False, **kwargs):
        """ Makes request with defined arguments.

        @:param self:
        @:param proxy: proxy
        @:param return_response: enable to return response object
        @:param return_response_text: enable to return analog of response.text
        @:param kwargs: any extra key arguments passed to the request (usually query parameters or data)
        @:type self: Downloader
        @:type proxy: str
        @:type return_response: bool
        @:type return_response_text: bool
        @:type kwargs: dict

        @:returns: tuple of response and response content
        @:rtype: tuple
        """

        proxies = {'https': proxy, 'http': proxy}

        start_time = time()
        response = self.request_maker.request(proxies=proxies, stream=True, **kwargs)

        if self.error_status_codes and (response.status_code in self.error_status_codes):
            raise BadProxyError

        response_text = ''
        for content in response.iter_content(1024, decode_unicode=True):
            if time() - start_time > 30:
                # if request time longer than 30 sec must stop request
                raise BadProxyError
            try:
                # if content is json object, concat it raw, else decode in utf-8
                response_text += content
            except TypeError:
                response_text += content.decode('utf-8')

        if return_response and return_response_text:
            return response, response_text
        elif return_response:
            return response, None
        elif return_response_text:
            return None, response_text

    def get(self, url, params={}, headers={}, cookies={}, timeout=60, return_response=False, return_response_text=False):
        """Makes 'GET' request with args by using create_request function.

        @:param self:
        @:param url: URL
        @:param params: params for 'GET' request
        @:param headers: request headers
        @:param cookies: request cookies
        @:param timeout: request timeout
        @:param return_response: enable to return response object
        @:param return_response_text: enable to return analog of response.text
        @:type self: Downloader
        @:type url: str
        @:type params: dict
        @:type headers: dict
        @:type cookies: dict
        @:type timeout: int
        @:type return_response: bool
        @:type return_response_text: bool

        Calls create_request function with args for 'GET' request.

        @:returns: tuple of response and response content
        @:rtype: tuple
        """
        return self.create_request(method='GET',
                                   url=url,
                                   params=params,
                                   cookies=cookies,
                                   headers=headers,
                                   timeout=timeout,
                                   return_response=return_response,
                                   return_response_text=return_response_text)

    def post(self, url, data={}, headers={}, cookies={}, timeout=60, return_response=True, return_response_text=False):
        """Makes 'POST' request with args by using create_request function.

        @:param self:
        @:param url: URL
        @:param data: data for 'POST' request
        @:param headers: request headers
        @:param cookies: request cookies
        @:param timeout: request timeout
        @:param return_response: enable to return response object
        @:param return_response_text: enable to return analog of response.text
        @:type self: Downloader
        @:type url: str
        @:type data: dict
        @:type headers: dict
        @:type cookies: dict
        @:type timeout: int
        @:type return_response: bool
        @:type return_response_text: bool

        Calls create_request function with args for 'POST' request.

        @:returns: tuple of response and response content
        @:rtype: tuple
        """
        return self.create_request(method='POST',
                                   url=url,
                                   cookies=cookies,
                                   data=data,
                                   headers=headers,
                                   timeout=timeout,
                                   return_response=return_response,
                                   return_response_text=return_response_text)

    def get_user_agent(self) -> Union[str, List]:
        """Rotates user agent.

        @:param self:
        @:type self: Downloader

        If user agent not None - appends user agent to the list -> gets first user agent from list.

        @:returns: user agent
        @:rtype: str
        """
        try:
            if self.user_agent:
                self.user_agents_list.append(self.user_agent)
            self.user_agent = self.user_agents_list.pop(0)
        except:
            return ''
        return self.user_agent
