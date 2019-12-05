import matplotlib.pyplot as plt
import numpy as np


def read_data(path):
    result = []
    with open(path, 'r') as fopen:
        n_cities = int(fopen.readline())    # 获取实际城市数目
        for line in fopen:
            result.append(list(map(float, line.split()[1:])))    # 将城市坐标加入到result列表中
    return n_cities, np.array(result)


class GA():
    def __init__(self, DNA_size, cross_rate, mutation_rate, pop_size, ):
        self.DNA_size = DNA_size            # 染色体上的基因数目（即城市数）
        self.cross_rate = cross_rate        # 交叉概率
        self.mutate_rate = mutation_rate    # 编译概率
        self.pop_size = pop_size            # 种群大小
                                            # 随机生成一个200以内数字组成的种群
        self.pop = np.vstack([np.random.permutation(DNA_size) for _ in range(pop_size)])

    def translateDNA(self, DNA, city_position):
        line_x = np.empty_like(DNA, dtype=np.float64)
        line_y = np.empty_like(DNA, dtype=np.float64)
        for i, d in enumerate(DNA):
            city_coord = city_position[d]       # 按照种群中每个体中的基因编排位置
            line_x[i, :] = city_coord[:, 0]     # 获取按基因编码后得到的x坐标
            line_y[i, :] = city_coord[:, 1]     # 获取按基因编码后得到的y坐标
        return line_x, line_y

    def get_fitness(self, line_x, line_y):
        total_distance = np.empty((line_x.shape[0],), dtype=np.float64)
        for i, (xs, ys) in enumerate(zip(line_x, line_y)):
            total_distance[i] = np.sum(np.sqrt(np.square(np.diff(xs)) + np.square(np.diff(ys))))
        fitness = 1 / total_distance        # 倒数作为适应度
        return fitness, total_distance

    def select(self, fitness):
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, replace=True, p=fitness/fitness.sum())
        return self.pop[idx]

    def crossover(self, parent, pop):
        if np.random.rand() < self.cross_rate:
            i_ = np.random.randint(0, self.pop_size, size=1)                        # select another individual from pop
            cross_points = np.random.randint(0, 2, self.DNA_size).astype(np.bool)   # choose crossover points
            keep_city = parent[~cross_points]                                       # find the city number
            swap_city = pop[i_, np.isin(pop[i_].ravel(), keep_city, invert=True)]
            parent[:] = np.concatenate((keep_city, swap_city))
        return parent

    def mutate(self, child):
        for point in range(self.DNA_size):
            if np.random.rand() < self.mutate_rate:
                swap_point = np.random.randint(0, self.DNA_size)
                swapA, swapB = child[point], child[swap_point]
                child[point], child[swap_point] = swapB, swapA
        return child

    def evolve(self, fitness):
        pop = self.select(fitness)
        pop_copy = pop.copy()
        for parent in pop:  # for every parent
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop


if __name__ == "__main__":
    N_GENERATIONS = 5000         # 迭代次数
    FILE_PATH = "../genetic/input.txt"              # 文件路径
    N_CITIES, CITIES_LIST = read_data(FILE_PATH)    # 读取文件中的城市列表

    ga = GA(DNA_size=N_CITIES, cross_rate=0.01, mutation_rate=0.001, pop_size=1000)

    result = []
    gen = []
    for generation in range(N_GENERATIONS):
        lx, ly = ga.translateDNA(ga.pop, CITIES_LIST)
        fitness, total_distance = ga.get_fitness(lx, ly)
        ga.evolve(fitness)
        best_idx = np.argmax(fitness)
        print("gen: ", len(gen), "len: ", total_distance[best_idx])
        gen.append(generation)
        result.append(total_distance[best_idx])

    fout = open("output.txt", 'w')
    fout.write("the shortest path: " + str(min(result)))
    fout.close()

    plt.plot(gen, result)
    plt.show()
