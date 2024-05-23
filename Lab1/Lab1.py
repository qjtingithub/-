import networkx as nx
import matplotlib.pyplot as plt
import re
import random
import heapq
import msvcrt

class Graph:

    def __init__(self):
        self.G = {}

    # 使用 Dijkstra 算法计算从 start 节点到其他所有节点的最短路径
    def dijkstra(self, start):
        # 初始化距离字典，所有节点的初始距离为无穷大
        distances = {vertex: float('infinity') for vertex in self.G}
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
            for neighbor, weight in self.G[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    shortest_path[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, shortest_path

    # 从 shortest_path 字典中获取从 start 到 end 的具体路径
    def get_shortest_path(self, shortest_path, start, end):
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

    # 展示有向图
    def showDirectedGraph(self):
        random.seed(1)
        G = nx.DiGraph()
        G_word_depth = {} # 记录对应节点深度
        G_word_order = {} # 记录在同一深度的顺序
        for word, next_words in self.G.items():
            # 这个if语句实际上只有第一个节点加入图时会用到
            if word not in G_word_depth:
                G_word_depth[word] = 1
                G_word_order[word] = 0
            for next_word, weight in next_words.items():
                if next_word not in G_word_depth:
                    G_word_depth[next_word] = G_word_depth[word] + 1 
                    G_word_order[next_word] = 0
                if not G.has_edge(word, next_word):
                    G.add_edge(word, next_word, weight = weight)
        # 处理每个节点的位置
        max_depth = max(G_word_depth.values())
        for depth in range(1, max_depth + 1):
            total = sum(1 for w in G_word_depth if G_word_depth[w] == depth)
            order = 10.0/(total + 1)
            for word in G_word_depth:
                random_step = random.random()
                if G_word_depth[word] == depth:
                    G_word_order[word] = order
                    order += (order + random_step)
        pos = {}
        for word, depth in G_word_depth.items():
            pos[word] = (G_word_order[word], max_depth - depth)
        # 绘图
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        pic_path = input("输入生成的图存储的路径和文件名：")
        plt.savefig(pic_path)
        plt.show()
        return
    
    # 查询桥接词
    def queryBridgeWords(self, word1, word2):
        if word1 not in self.G or word2 not in self.G:
            print(f"No {word1} or {word2} in the graph!")
            return
        words = []
        for word in self.G[word1]:
            if word2 in self.G[word]:
                words.append(word)
        if not words:
            print(f"No bridge words from {word1} to {word2}!")
        else:
            print(f"The bridge words from {word1} to {word2} are: " + ",".join(words))
        return
    
    # 根据bridge word生成新的文本
    def generateNewText(self, inputText):
        words = inputText.split(" ")
        new_words = []
        for i in range(len(words) - 1):
            word1 = words[i]
            word2 = words[i + 1]
            new_words.append(word1)
            # 查询桥接词
            bridgewords = []
            if word1 in self.G:
                for bridgeword in self.G[word1]:
                    if word2 in self.G[bridgeword]:
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

    
    # 计算两个单词间的最短路径
    # 完成可选功能
    def calcShortestPath(self, word1, word2 = None):
        if word1 not in self.G:
            print(f"{word1} 不在图中!")
            return
        
        if word2 is None:
            word2 = random.choice(list(self.G.keys()))
            while word2 == word1:  # 确保终点和起点不同
                word2 = random.choice(list(self.G.keys()))

        if word2 not in self.G:
            print(f"{word2} 不在图中!")
            return
        
        # 使用 Dijkstra 算法计算从 word1 到所有节点的最短路径
        distances, shortest_path = self.dijkstra(word1)

        if distances[word2] == float('infinity'):
            print(f"{word1} 和 {word2} 之间不可达!")
            return None
        
        # 获取从 word1 到 word2 的具体路径
        path = self.get_shortest_path(shortest_path, word1, word2)
        print("最短路径: " + " -> ".join(path))
        return path
    
    # 随机游走
    def randomWalk(self):
        node1 = random.choice(list(self.G.keys()))
        path = []
        edges = []
        path.append(node1)
        while 1:
            node2 = random.choice(list(self.G[node1].keys()))
            if (node1, node2) not in edges:
                path.append(node2)
                edges.append((node1, node2))
                node1 = node2
            else:
                path.append(node2)
                break
            
            if not self.G[node2]:
                break

            if msvcrt.kbhit():
                print("随机游走中止！")
                break
        
        print("随机游走结果为：" + " -> ".join(path))
        path_pos = input("请输入将随机游走生成的文本输入的文件位置和文件名：")
        content = " ".join(path)
        try:
            with open(path_pos, 'w') as file:
                file.write(content)
        except IOError:
            print("I/O错误")
        return

def main():
    filename = input("请输入文本文件的位置和文件名：")
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print("输入的文件位置或者文件名错误！")
    except IOError:
        print("I/O错误")

    #  标点符号处理
    cleaned_content = re.sub(r'[\x00-\x2F\x3A-\x40\x5B-\x60\x7B-\x7F]+', ' ', content)
    if cleaned_content is None:  # 检查是否成功替换
        print("替换操作失败，可能正则表达式匹配有误。")
        return
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
    # print(cleaned_content)

    # 生成图
    words = re.split(r'\s+', cleaned_content)
    # print(words)
    # 会匹配到空字符串，最后一个符号会被替换成空格，然后将结束符匹配进去，所以需要利用filter过滤
    # filter会将第一个参数中的函数应用到第二个参数中的每一个元素上
    # strip函数：str.strip([chars]); chars是移除的字符的序列，为空的话默认为空白字符
    words = list(filter(lambda w:w.strip(), words))
    # print(words)
    # 此时已经将文本处理好了，开始生成图
    instance = Graph()
    i = 0
    while i < len(words) - 1:
        current_word = words[i]
        next_word = words[i + 1]
        # 解决最后一个单词的节点问题
        if i == len(words) - 2:
            instance.G[next_word] = {}
        if current_word not in instance.G:
            instance.G[current_word] = {}
        if next_word in instance.G[current_word]:
            instance.G[current_word][next_word] += 1
        else:
            instance.G[current_word][next_word] = 1
        i += 1
    # print(instance.G)
    while 1:
        func_num = input("展示图请输入1，查询桥接词请输入2，根据bridge words生成新的文本请输入3，计算两个单词间最短路径请输入4，随机游走请输入5：,退出请输入6：")
        if func_num == '1':
            instance.showDirectedGraph()
        elif func_num == '2':
            while True:
                input_str = input("请输入两个英文单词:")
                words = input_str.split()
                if len(words) != 2:
                    print("请输入两个单词，以空格作为间隔：")
                else:
                    word1, word2 = words
                    break
            instance.queryBridgeWords(word1, word2)
        elif func_num == '3':
            new_text = input("请输入文本：")
            if not new_text:
                print("输入的文本为空")
            else:
                instance.generateNewText(new_text)
        elif func_num == '4':
            while True:
                input_str = input("请输入一个或者两个英文单词:")
                words = input_str.split()
                if len(words) > 2 or len(words) == 0:
                    print("请输入两个单词，以空格作为间隔：")
                elif len(words) == 1:
                    word1 = words[0]
                    word2 = None
                    break
                else:
                    word1, word2 = words
                    break
            instance.calcShortestPath(word1, word2)
        elif func_num == '5':
            print("随机游走开始，过程中你可以随时按空格键停止")
            instance.randomWalk()
        elif func_num == '6':
            print("成功退出！")
            break
        else:
            print("请根据提示输入正确的数字：")
    
if __name__ == '__main__':
    main()
