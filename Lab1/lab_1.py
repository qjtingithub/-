"""
这是一个完成了查询桥接词、根据bridge words生成新的文本、
计算两个单词间最短路径、随机游走功能的python项目
"""

import re
import random
import heapq
import msvcrt
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    """图类型，包含要求的方法"""
    def __init__(self):
        self.g = {}

    def dijkstra(self, start):
        """使用 Dijkstra 算法计算从 start 节点到其他所有节点的最短路径"""
        # 初始化距离字典，所有节点的初始距离为无穷大
        distances = {vertex: float('infinity') for vertex in self.g}
        # 设置起始节点到起始节点的距离为 0
        distances[start] = 0
        # 初始化优先队列，存储 (距离, 节点) 元组
        priority_queue = [(0, start)]
        # 初始化存储最短路径前一个单词的字典
        shortest_path = {}

        while priority_queue:
            # 弹出优先队列中距离最小的节点，
            current_distance, current_vertex = heapq.heappop(priority_queue)
            # 如果取出的距离大于已知距离，跳过该节点
            if current_distance > distances[current_vertex]:
                continue
            # 遍历当前节点的所有邻居
            for neighbor, weight in self.g[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    shortest_path[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, shortest_path

    def get_shortest_path(self, shortest_path, start, end):
        """从 shortest_path 字典中获取从 start 到 end 的具体路径"""
        path = []
        current_vertex = end
        # 反向追踪路径从 end 到 start，因为字典记录的是最短路径前一个节点
        while current_vertex != start:
            path.insert(0, current_vertex)
            current_vertex = shortest_path.get(current_vertex, start)
            if current_vertex == start:
                break
        path.insert(0, start)
        return path

    def show_directed_graph(self):
        """展示有向图"""
        random.seed(1)
        g = nx.DiGraph()
        g_word_depth = {} # 记录对应节点深度
        g_word_order = {} # 记录在同一深度的顺序
        for word, next_words in self.g.items():
            # 这个if语句实际上只有第一个节点加入图时会用到
            if word not in g_word_depth:
                g_word_depth[word] = 1
                g_word_order[word] = 0
            for next_word, weight in next_words.items():
                if next_word not in g_word_depth:
                    g_word_depth[next_word] = g_word_depth[word]+1
                    g_word_order[next_word] = 0
                if word not in self.g[next_word]:
                    g.add_edge(word, next_word, weight = weight)
                else:
                    g.add_edge(word, next_word, weight = weight + self.g[next_word][word])
        # 处理每个节点的位置
        max_depth = max(g_word_depth.values())
        for depth in range(1, max_depth + 1):
            total = sum(1 for v in g_word_depth.values() if v == depth)
            step = 10.0/(total + 1)
            order = step
            for word, word_depth in g_word_depth.items():
                random_step = random.random() * (order/2)
                if word_depth == depth:
                    g_word_order[word] = order
                    order += (step + random_step)
        pos = {}
        for word, depth in g_word_depth.items():
            pos[word] = (g_word_order[word], max_depth - depth)
        # 绘图
        nx.draw(g, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        edge_labels = {(u, v): d['weight'] for u, v, d in g.edges(data=True)}
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
        pic_path = input("输入生成的图存储的路径和文件名：")
        plt.savefig(pic_path)
        plt.show()

    def query_bridge_words(self, word1, word2):
        """查询桥接词"""
        if word1 not in self.g or word2 not in self.g:
            print(f"No {word1} or {word2} in the graph!")
            return
        if word1 == word2:
            print(f"No bridge words from {word1} to {word2}!")
            return
        words = []
        for word in self.g[word1]:
            if word2 in self.g[word]:
                words.append(word)
        if not words:
            print(f"No bridge words from {word1} to {word2}!")
        else:
            print(f"The bridge words from {word1} to {word2} are: " + ",".join(words))
        return

    def generate_new_text(self, input_text):
        """根据bridge word生成新的文本"""
        words = input_text.split(" ")
        new_words = []
        for i in range(len(words) - 1):
            word1 = words[i]
            word2 = words[i + 1]
            new_words.append(word1)
            # 查询桥接词
            bridgewords = []
            if word1 in self.g:
                for bridgeword in self.g[word1]:
                    if word2 in self.g[bridgeword]:
                        bridgewords.append(bridgeword)
            if bridgewords:
                # 随机选择一个桥接词
                chosen_bridge_word = random.choice(bridgewords)
                new_words.append(chosen_bridge_word)
        # 添加最后一个单词
        new_words.append(words[-1])
        # 打印处理好的新文本
        new_text = " ".join(new_words)
        print(new_text)
        return new_text

    # 完成可选功能
    def calc_shortest_path(self, word1, word2 = None):
        """计算两个单词间的最短路径"""
        if word1 not in self.g:
            print(f"{word1} 不在图中!")
            return None

        if word2 is None:
            word2 = random.choice(list(self.g.keys()))
            while word2 == word1:  # 确保终点和起点不同
                word2 = random.choice(list(self.g.keys()))

        if word2 not in self.g:
            print(f"{word2} 不在图中!")
            return None

        # 使用 Dijkstra 算法计算从 word1 到所有节点的最短路径
        distances, shortest_path = self.dijkstra(word1)

        if distances[word2] == float('infinity'):
            print(f"{word1} 和 {word2} 之间不可达!")
            return None

        # 获取从 word1 到 word2 的具体路径
        path = self.get_shortest_path(shortest_path, word1, word2)
        print("最短路径: " + " -> ".join(path))
        return path

    def random_walk(self):
        """随机游走"""
        node1 = random.choice(list(self.g.keys()))
        path = []
        edges = []
        path.append(node1)
        while 1:
            node2 = random.choice(list(self.g[node1].keys()))
            if (node1, node2) not in edges:
                path.append(node2)
                edges.append((node1, node2))
                node1 = node2
            else:
                path.append(node2)
                break

            if not self.g[node2]:
                break

            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == ' ':
                    print("随机游走中止！")
                break

        print("随机游走结果为：" + " -> ".join(path))
        path_pos = input("请输入将随机游走生成的文本输入的文件位置和文件名：")
        content = " ".join(path)
        try:
            with open(path_pos, 'w', encoding="utf-8") as file:
                file.write(content)
        except IOError:
            print("I/O错误")

def loop(instance):
    """功能循环"""
    while 1:
        func_num = input("展示图请输入1，查询桥接词请输入2，根据bridge words生成新的文本请输入3，"
                         "计算两个单词间最短路径请输入4，随机游走请输入5：,退出请输入6：")
        if func_num == '1':
            instance.show_directed_graph()
        elif func_num == '2':
            while True:
                input_str = input("请输入两个英文单词:")
                words = input_str.split()
                if len(words) != 2:
                    print("请输入两个单词并以空格作为间隔!")
                else:
                    word1, word2 = words
                    instance.query_bridge_words(word1, word2)
                    break
        elif func_num == '3':
            new_text = input("请输入文本：")
            if not new_text:
                print("输入的文本为空")
            else:
                instance.generate_new_text(new_text)
        elif func_num == '4':
            while True:
                input_str = input("请输入一个或者两个英文单词:")
                words = input_str.split()
                if len(words) > 2 or len(words) == 0:
                    print("请输入两个单词，以空格作为间隔：")
                elif len(words) == 1:
                    word1 = words[0]
                    word2 = None
                    instance.calc_shortest_path(word1, word2)
                    break
                else:
                    word1, word2 = words
                    instance.calc_shortest_path(word1, word2)
                    break
        elif func_num == '5':
            print("随机游走开始，过程中你可以随时按空格键停止")
            instance.random_walk()
        elif func_num == '6':
            print("成功退出！")
            break
        else:
            print("请根据提示输入正确的数字：")

def main():
    """主函数，生成图"""
    filename = input("请输入文本文件的位置和文件名：")
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print("输入的文件位置或者文件名错误！")
        return
    except IOError:
        print("I/O错误")
        return
    
    if content is None:
        return

    #  标点符号处理
    cleaned_content = re.sub(r'[\x00-\x2F\x3A-\x40\x5B-\x60\x7B-\x7F]+', ' ', content)
    if cleaned_content is None:  # 检查是否成功替换
        print("替换操作失败，可能正则表达式匹配有误。")
        return
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content)

    # 生成图
    words = re.split(r'\s+', cleaned_content)
    words = list(filter(lambda w:w.strip(), words))
    # 此时已经将文本处理好了，开始生成图
    instance = Graph()
    i = 0
    while i < len(words) - 1:
        current_word = words[i]
        next_word = words[i + 1]
        # 解决最后一个单词的节点问题
        if i == len(words) - 2 and next_word not in instance.g:
            instance.g[next_word] = {}
        if current_word not in instance.g:
            instance.g[current_word] = {}
        if next_word in instance.g[current_word]:
            instance.g[current_word][next_word] += 1
        else:
            instance.g[current_word][next_word] = 1
        i += 1
    print(instance.g)
    loop(instance)

if __name__ == '__main__':
    main()
