import re
import json
import collections
import time
import pymongo
import redis



# redis的 pipe管道事务操作:
# 1. pipe为事务管道,必须要execute后才会在服务器端真正执行
# 2.当管道中使用watch开启检测后,到multi语句(或者execute语句)前,会让pipe处于"非事务阶段",
#   可以获取、删除redis服务器中的值.  (意味着此阶段的pipe.set()不需要execute())
# 3. 当pipe.execute()执行时,会把储存在pipe管道中"滞后执行"的事务操作全部一次性完成.
# 4.在"管道事务"阶段,打印出来的都是对象(在后面execute后接受str结果); 而在"非事务"阶段,返回的是字符.

# def lst_to_zset(lst=[4, 1, 88], key_name="queue"):
#     m_ = zip(lst, range(len(lst)))
#     all_z_dict = {i:j for i, j in m_}
#     r.delete(key_name)
#     r.zadd(key_name, all_z_dict)


class CookiesPool():
    """
        function:
            封装一个操作redis的对象, 把列表/哈希表/集合等redis数据结构的 '增删改查' 写成统一的'实例方法接口'
            pool的数据结构: 使用队列结构 (先进的先出, 适合爬虫项目)
                            所以: add是加到右边最后一个元素; get是左边第一个元素; pop也是左边第一个元素
        note:
            1. pool_type的种类:
                1. list
                2. dict
                3. set
    """
    def __init__(self, pool_name, pool_type="list", redis_host="localhost", redis_port=6379, db=0, decode_responses=True, **kwargs):
        if db:
            kwargs["db"] = db
        if decode_responses:
            kwargs["decode_responses"] = decode_responses
        self.redis = redis.StrictRedis(host="localhost", port=6379, **kwargs)
        self.pool_name = pool_name
        self.pool_type = pool_type
        # 先清空redis中的这个'键' (如果已经存在某些数据, 可能数据类型会和后面操作的方式对不上而报错)
        self.redis.delete(self.pool_name)

    # 增:
    # =================
    def add(self, value, key="undefined"):
        if self.pool_type == "list":
            res = self.redis.rpush(self.pool_name, value)
        elif self.pool_type == "dict":
            res = self.redis.hset(self.pool_name, key, value)
        return res

    # 删:
    # =================
    def pop(self):
        if self.pool_type == "list":
            res = self.redis.lpop(self.pool_name)
        elif self.pool_type == "dict":
            res = "'dict'类型的pool没有pop方法;\n"
        return res

    def delete(self, key):
        if self.pool_type == "list":
            res = self.redis.lrem(self.pool_name, 1, key)
        elif self.pool_type == "dict":
            res = self.redis.hdel(self.pool_name, key)
        return res

    # 改:
    # =================
    pass


    # 查:
    # =================

    def get(self, key="undefined"):
        if self.pool_type == "list":
            res = self.redis.lindex(self.pool_name, 0)
        elif self.pool_type == "dict":
            res = self.redis.hget(self.pool_name, key)
        return res

    def values(self):
        if self.pool_type == "list":
            res = self.redis.lrange(self.pool_name, 0, -1)
        elif self.pool_type == "dict":
            # "dict类型的, 直接返回items字典"
            res = self.redis.hgetall(self.pool_name)
        return res

    def length(self):
        if self.pool_type == "list":
            res = self.redis.llen(self.pool_name)
        elif self.pool_type == "dict":
            res = len(self.redis.hvals(self.pool_name))
        return res

    def __str__(self):
        return str(self.values())





# 应对业务需求，快速匹配出他们想要的消化数据
def merge_mongo(
    left_table_name="ziru_stock", right_table_name="ziru_name_list", left_join_field="所属业务组",
    right_join_field="ziru_zone", conditions_dict={}, project_dict={"_id":0}, db=None,
    ):
    """
    notes:
        1. project_dict的功能是表示哪些字段需要显示，哪些不要显示。但是只有“_id”可以为0，其他只能标记为1.
        2. 右连接的字段前必须加上matched_field才行
        3. 返回得到的 all_join_docs 中， 右连接得到的所有内容都包含在 matched_field 字段中，以dict形式存在
    """

    if db is None:
        client = pymongo.MongoClient("127.0.0.1")
        db = client["zufang_001"]

    # 输入接口：
    # left_table_name
    # right_table_name

    # 管道筛选：
    pipeline = [
                {
                    "$lookup":
                    {
                        "from":right_table_name,
                        "localField":left_join_field,
                        "foreignField":right_join_field,
                        "as":"matched_field",
                    }
                },
                {
                    "$match": conditions_dict,
                },
                {
                    "$project": project_dict,
                }
                ]

    all_join_docs = db[left_table_name].aggregate(pipeline)
    return all_join_docs



# with r.pipeline() as pipe:
#     while True:
#         try:
#             # 监视我们需要修改的键
#             queue_ = "lll"
#             # pipe.rpush(queue_, *[3, 4, 5])
#             # 进入"非事务"阶段
#             pipe.watch(queue_)
#             pipe.rpush(queue_, *[44, 88])
#
#             # 进入"事务"阶段
#             pipe.multi()
#             x = pipe.lrange(queue_, 0, -1)
#             print(x)
#             # print(pipe.rpop(queue_))
#             ss = pipe.execute()
#             print(ss)
#             break
#
#         except redis.WatchError:
#             # 如果其他客户端在我们 WATCH 和 事务执行期间，则重试
#             # pipe.unwatch()
#             pipe.reset() # unwatch和ureset的作用应该差不多
#             print("error")
#             break
#


def main():
    pass
    # r.sadd("bnm", print(3))
    # r.lpush("aabb", *[1, 2, 3])
    # print(r.lrange("a", 0, -1))
    # print(r.smembers("crawl_cost_price:crawled_queues"))



if __name__ == '__main__':
    print("start test!")
    main()
    print("\n\n\neverything is ok!")
