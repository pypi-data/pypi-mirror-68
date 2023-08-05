import shlex

import uncurl
from requests import Response, request


def curl_command_to_response(command) -> Response:
    """
    change curl to request
    :param command:
    :return: Request
    """
    context = uncurl.parse_context(shlex.join(command))
    data = context.data.encode('utf-8') if context.data else None
    return request(method=context.method, url=context.url, headers=context.headers, data=data)


def response_to_head_str(response: Response) -> str:
    head_str = ''
    head_str += f'HTTP {response.status_code} {response.reason}\n'
    for key, value in response.headers.items():
        head_str += f"{key}: {value}\n"
    return head_str