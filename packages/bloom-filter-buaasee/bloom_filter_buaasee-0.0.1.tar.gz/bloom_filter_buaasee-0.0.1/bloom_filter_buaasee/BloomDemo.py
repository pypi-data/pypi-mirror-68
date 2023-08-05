import redis
import math

class HashMap:
    def __init__(self, m, seed):
        self.m = m
        self.seed = seed

    def hash_value(self, ele):
        hash_value = 0
        for i in range(len(ele)):
            hash_value += self.seed * hash_value + ord(ele[i])
        return hash_value%(self.m-1)


class BloomFilter:
    times = 0
    def __init__(self, server, name, bit, hash_func_num):
        self.bit = bit
        self.m = 1 << bit
        self.name = name
        self.server = server
        self.k = hash_func_num
        self.seeds = range(hash_func_num)
        self.maps = [HashMap(self.m, seed) for seed in self.seeds]
        # n = int(input("请输入预期的爬取数据量，用于计算预期误差。若不清楚或忽略本步骤则输入 0 ，采用默认配置，可以处理千万级数据\n"))
        # self.n_pre = n
        # if BloomFilter.times == 0:
        #     self.error_rate()
        #     BloomFilter.times += 1

    def exist(self, ele):
        if ele is None:
            return 'none'
        exist = 1
        for every_map in self.maps:
            hash_value = every_map.hash_value(ele)
            print(hash_value)
            exist = exist & self.server.getbit(self.name, hash_value)
        if exist == 0:
            return 0
        return exist

    def put_into(self, ele):
        for every_map in self.maps:
            hash_value = every_map.hash_value(ele)
            self.server.setbit(self.name, hash_value, 1)

    def error_rate(self):
        if self.n_pre ==0:
            return
        self.seeds =range(self.k)
        error_real = math.pow((1-math.pow(math.e, (-1*self.k*self.n_pre/self.m))), self.k)
        print("当前hash函数个数为:", self.k, "当前位数组位数为", self.m)
        print('当前预期误判率为', error_real)
        print('当前预期误判数为', error_real*self.n_pre)
        print("是否需要调整参数？（Y/N）")
        modify = input()
        if modify == 'y' or modify == 'Y':
            print("如需增加hash函数个数则输入h（不建议超过8），将位数组位数乘2输入m，输入其他视为放弃")
            para = input()
            if para == 'h' or para == 'H':
                self.k += 1
                self.seeds = range(self.k)
                self.maps = [HashMap(self.m, seed) for seed in self.seeds]
                self.error_rate()
            elif para == 'm' or para == 'M':
                self.m*=2
                self.seeds = range(self.k)
                self.maps = [HashMap(self.m, seed) for seed in self.seeds]
                self.error_rate()
            else:
                return
        else:
            return

