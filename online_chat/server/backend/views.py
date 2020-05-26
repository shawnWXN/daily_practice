import time
import json
import functools
import datetime
from .msg_redis import REDIS
from .common import *


def url_map(path):
    """
    :param path: 请求路径
    url与处理函数的映射方法
    :param path:
    :return:
    """
    url = {
        '/': root,
        '/online-count': obtain_online_count,
        '/latest-msg': send_latest_msg,
        '/receive-msg': receive_msg
    }
    if path.endswith('/') and len(path) != 1:
        path = path[:-1]
    return url.get(path)


def check_params(required_params):
    """
    参数检查装饰器
    :param required_params:dict, 例如{'start_date':'datetime.datetime'}
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kw):
            params_str = request.get('params')
            try:
                receive_params = json.loads(params_str)
            except Exception:
                return {
                    'status_code': 4000,
                    'message': 'json loads failed when \'params\' is [%s]' % params_str,
                    'data': {}
                }
            else:
                need_params = set(required_params.keys())
                get_params = set(receive_params.keys())
                lack_s, vain_s = need_params - get_params, get_params - need_params
                if not (lack_s or vain_s):
                    for k, v in receive_params.items():
                        ty = required_params.get(k)
                        if ty == 'str':
                            if not isinstance(v, str):
                                mess = 'param \'%s\': should be \'str\' type' % k
                                break
                        elif ty == 'int':
                            try:
                                i = int(v)
                            except Exception:
                                mess = 'param \'%s\': should be \'int\' type' % k
                                break
                            else:
                                receive_params[k] = i
                        elif ty == 'datetime.datetime' or ty == 'datetime.date':
                            try:
                                pattern = '%Y-%m-%d' if ty == 'datetime.date' else '%Y-%m-%d %H:%M:%S'
                                d = datetime.datetime.strptime(v, pattern)
                            except Exception as e:
                                mess = 'param \'%s\': %s' % (k, e.args[-1])
                                break
                            else:
                                receive_params[k] = d
                        elif ty == 'tuple':
                            if not isinstance(v, tuple):
                                mess = 'param \'%s\': should be \'tuple\' type' % k
                                break
                        else:
                            mess = 'required type \'%s\' is unknown' % ty
                            break
                    else:
                        request['params'] = receive_params
                        return func(request, *args, **kw)
                else:
                    mess = ''
                    mess += 'lack param %s,' % lack_s if lack_s else ''
                    mess += 'vain param {},' % vain_s if vain_s else ''
                return {'status_code': 4000, 'message': mess, 'data': {}}
        return wrapper

    return decorator


@check_params({'username': 'str', 'for': 'str'})
def root(request):
    print('/ receive request:', request)
    for_which = request.get('params').get('for')
    username = request.get('params').get('username')
    # address = request.get('address')[0]  # 暂时用请求源ip作用户

    if for_which == 'register':
        letter = {'content': 'Welcome, %s' % username, 'dt': dt2str(datetime.datetime.now()), 'sender': 'system'}
        if REDIS.user_online(username) == 1:
            status_code, mess, data = (2000, 'success', letter)
        else:
            status_code, mess, data = (2001, 'send msg %s to %s failed' % (letter.get('content'), username), {})
    elif for_which == 'logout':
        REDIS.user_logout(username)
        status_code, mess, data = (5000, 'user %s logout' % username, {})  # 5000:告诉服务器终止连接
    else:
        status_code, mess, data = (4000, 'param \'for\'=\'%s\' is invalid' % for_which, {})

    return {'status_code': status_code, 'message': mess, 'data': data}


def obtain_online_count(request):
    print('/online-count receive request: ', request)
    return {'status_code': 2000, 'message': 'success', 'data': REDIS.online_list()}


@check_params({'username': 'str'})
def send_latest_msg(request):
    # print('/latest-msg receive request: ', request)
    # address = request.get('address')[0]  # 暂时用请求源ip作用户
    username = request.get('params').get('username')
    letter = REDIS.pop_latest_letter('BOX_OF_%s' % username)
    letter['dt'] = dt2str(letter['dt'])
    return {'status_code': 2000, 'message': 'success', 'data': letter}


@check_params({'username': 'str', 'content': 'str', 'to': 'str'})
def receive_msg(request):
    # print('/receive-msg receive request: ', request)
    # address = request.get('address')[0]  # 暂时用请求源ip作用户
    letter = request.get('params')
    username = letter.pop('username')
    recipients = letter.pop('to')
    letter['dt'] = datetime.datetime.now()
    letter['sender'] = username

    if REDIS.deliver_to_letter_box('BOX_OF_%s' % recipients, letter) == 1:
        letter['sender'] = 'yourself'
        letter['dt'] = dt2str(letter['dt'])
        status_code, mess, data = (2000, 'success', letter)
    else:
        status_code, mess, data = (2001, 'send msg %s to %s failed' % (letter.get('content'), recipients), {})
    return {'status_code': status_code, 'message': mess, 'data': data}
