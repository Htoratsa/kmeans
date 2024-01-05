import numpy as np
import pygame

##definitions
K_MEANS = 3
SAMPLE_SIZE = 300
SECONDARY_CENTERS = 8.5  # 10.5 works
BACKGROUND_COLOR = "#24273a"
colors = ["#ed8796", "#8aadf4", "#a6da95", "#eed49f", "#c6a0f6", "#f5a97f"]


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


def reload_everything():
    new_sets = []
    new_sets.extend(generate_set(center=(0.0, 0.0), radius=10, count=SAMPLE_SIZE))  # Center distribution
    new_sets.extend(generate_set(center=(-SECONDARY_CENTERS, SECONDARY_CENTERS), radius=5, count=int(SAMPLE_SIZE/2)))  # Left distribution
    new_sets.extend(generate_set(center=(SECONDARY_CENTERS, SECONDARY_CENTERS), radius=5, count=int(SAMPLE_SIZE/2)))  # Right distribution

    new_kmeans = []
    for i in range(K_MEANS):
        new_kmeans.append(Item(center=(np.random.random(), np.random.random()), radius=20))
    return new_sets, new_kmeans

def translate_points(x, y):
    pos_x = x * SCALING_FACTOR + SCREEN_WIDTH/2
    pos_y = y * -SCALING_FACTOR + 3*SCREEN_HEIGHT/5
    return pos_x, pos_y

if __name__ == "__main__":
    #set creation
    sets, kmeans = reload_everything()

    # pygame setup
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    pygame.display.set_caption(f'K-means implementation')

    #Iteration counter
    iteration = 0

    while running:
        # poll for events
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.KEYDOWN:
                if event.dict['unicode'] == ' ':
                    # sorting groups respect means
                    update_sets(sets, kmeans)
                    # updating the means
                    update_means(Item, sets, kmeans)
                    iteration +=1
                    pygame.display.set_caption(f'iteration {iteration}')

                if event.dict['unicode'] == 'r':
                    print(f'Reloading everything...')
                    sets, kmeans = reload_everything()
                    iteration = 0
                    pygame.display.set_caption(f'Reloaded!')

            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(BACKGROUND_COLOR)

        # RENDER YOUR GAME HERE
        for element in sets:
            # plotting sets
            SCALING_FACTOR = 20
            pos_x, pos_y = translate_points(element.x, element.y)
            pygame.draw.circle(surface=screen, color=colors[element.group], center=[pos_x, pos_y], radius=4.)
        for index in range(K_MEANS):
            pos_x, pos_y = translate_points(kmeans[index].x, kmeans[index].y)
            pygame.draw.circle(surface=screen, color=colors[index], center=[pos_x, pos_y], radius=8.)

        # update sccreen
        pygame.display.update()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()