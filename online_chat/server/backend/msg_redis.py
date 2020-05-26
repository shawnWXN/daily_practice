import redis
import pickle


class Redis(object):
    def __init__(self, host='127.0.0.1', port=6379, db=0):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.r = redis.Redis(connection_pool=pool)

    def user_online(self, value):
        """
        用户上线。即在online_users里加一条记录
        :param value:
        :return:
        """
        return self.r.sadd('online_users', pickle.dumps(value))

    def user_logout(self, value):
        """
        用户下线，从online_users里移除一条记录
        :param value:
        :return:
        """
        return self.r.srem('online_users', pickle.dumps(value))

    def online_list(self):
        """
        获取在线用户列表
        :return:
        """
        values = self.r.smembers('online_users')
        return [pickle.loads(val) for val in values]

    def deliver_to_letter_box(self, name, value):
        """
        向名为name的信箱，投递内容为values的消息
        :param name:
        :param value: dict。{'msg': 'xx', 'dt': datetime.datetime(x,x,x), 'sender': 'xxx'}
        :return:
        """
        return self.r.lpush(name, pickle.dumps(value))

    def pop_latest_letter(self, name):
        """
        从名为name的信箱中取出最新的消息
        :param name:
        :return:
        """
        tup = self.r.brpop(name, 30)
        if not tup:
            return pickle.loads(tup[1])
        return {}


REDIS = Redis()
