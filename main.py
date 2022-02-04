import pygame


def start_screen():
    image = pygame.image.load("data/fon.jpg")
    image = pygame.transform.scale(image, (550, 550))
    screen.blit(image, image.get_rect())
    f1 = pygame.font.Font(None, 40)
    text1 = f1.render("Заставка", True, "red")
    screen.blit(text1, (50, 150))
    zastavka = True
    exit = False
    while zastavka:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                zastavka = False
                exit = True
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                zastavka = False
        pygame.display.flip()
    return exit


def load_level(filename):
    try:
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except FileNotFoundError:
        print("Уровня с таким названием не существует")
        return 0


def generate_level(level):
    global grass_group, player_group, coords_box_x, coord_box_y
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                grass_group.add(Tile('grass', x * 50, y * 50))
            elif level[y][x] == '#':
                box_group.add(Tile('box', x * 50, y * 50))
            elif level[y][x] == '@':
                grass_group.add(Tile('grass', x * 50, y * 50))
                player_group.add(Player(x * 50 + 15, y * 50 + 5))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(f"data/{tile_type}.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load("data/mario.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, move, all_sprites, box_group):
        if move == "right":
            for el in all_sprites:
                el.rect.x -= 50
        if move == "left":
            for el in all_sprites:
                el.rect.x += 50
        if move == "up":
            for el in all_sprites:
                el.rect.y += 50
        if move == "down":
            for el in all_sprites:
                el.rect.y -= 50


if __name__ == "__main__":
    name = input("Введите название уровня: ")
    pygame.init()
    pygame.display.set_caption("Перемещение героя")
    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)
    grass_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    level = load_level(f"{name}.txt")
    all_sprites = pygame.sprite.Group()
    if not level:
        pygame.quit()
    else:
        generate_level(level)
        for el in grass_group:
            all_sprites.add(el)
        for el in box_group:
            all_sprites.add(el)
        exit = start_screen()
        if not exit:
            runing = True
            while runing:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        runing = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            player_group.update("right", all_sprites, box_group)
                        if event.key == pygame.K_LEFT:
                            player_group.update("left", all_sprites, box_group)
                        if event.key == pygame.K_UP:
                            player_group.update("up", all_sprites, box_group)
                        if event.key == pygame.K_DOWN:
                            player_group.update("down", all_sprites, box_group)
                screen.fill("black")
                grass_group.draw(screen)
                box_group.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()
            pygame.quit()
        else:
            pygame.quit()
