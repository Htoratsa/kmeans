import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
mplstyle.use('fast')

##definitions
MIN_X = -20
MAX_X = 20
MIN_Y = -20
MAX_Y = 20

K_MEANS = 3

SAMPLE_SIZE = 10

colors = ["red", "blue", "green", "black"]


class Item:
    def __init__(self, center: tuple, radius: float) -> None:
        direction = np.random.random() * 2 * np.pi
        magnitude = np.random.random() * radius
        self.x = np.cos(direction)*magnitude + center[0]
        self.y = np.sin(direction)*magnitude + center[1]
        self.group = -1


def generate_set(center: tuple, radius: float, count: int) -> list:
    new_set = []
    for _ in range(count):
        new_item = Item(center, radius)
        new_set.append(new_item)
    return new_set


def plotting(title) -> None:
    plt.clf()
    for element in sets:
        plt.scatter(element.x, element.y, color=colors[element.group], s=5)
    for index in range(K_MEANS):
        color = colors[index]
        plt.scatter(kmeans[index].x, kmeans[index].y, color=color, s=20)
    # plt.show()
    plt.title(title)
    plt.savefig(f'{title}.png')
    # pass


def update_sets(sets, kmeans):
    for element in sets:
        max_distance = 100000
        for index, kmean in enumerate(kmeans):
            current_distance = np.square(
                    np.linalg.norm(
                        np.array((element.x, element.y)) - np.array((kmean.x, kmean.y))
                    )
                )
            if current_distance < max_distance:
                max_distance = current_distance
                element.group = index

def update_means(Item, sets, kmeans):
    for index, kmean in enumerate(kmeans):
        starting_vector = np.array((0, 0))
        counter = 0
        for element in sets:
            if element.group == index:
                starting_vector = starting_vector + np.array((element.x, element.y))
                counter += 1
        if counter > 0:
            kmean.x = starting_vector[0] / counter
            kmean.y = starting_vector[1] / counter
        else:
            print(f'Counter for index {index} was 0! regenerating...')
            kmeans[index] = Item(center=(np.random.random(), np.random.random()), radius=20)

if __name__ == "__main__":
    #set creation
    sets = []
    sets.extend(generate_set(center=(0.0, 0.0), radius=10, count=100))
    sets.extend(generate_set(center=(-10.5, 10.5), radius=5, count=100))
    sets.extend(generate_set(center=(10.5, 10.5), radius=5, count=100))

    # random kmeans
    kmeans = []
    for i in range(K_MEANS):
        kmeans.append(Item(center=(np.random.random(), np.random.random()), radius=20))

    # first plot
    plotting('0_state')

    #SOrting iteratins
    for iteration in range(10):
        print(f'iteration {iteration}...')
        # sorting groups respect means
        update_sets(sets, kmeans)

        # updating the means
        update_means(Item, sets, kmeans)

        plotting(f'iteration_{iteration}')
