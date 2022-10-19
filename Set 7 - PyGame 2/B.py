import os
from random import randint
import pygame as pg

pg.init()
pg.display.set_caption("Ящики")

CLOCK = pg.time.Clock()
TILE_SIZE = 64  # in pixels
LVL_SIZE = 10  # in tiles
SIZE = W, H = LVL_SIZE * TILE_SIZE, LVL_SIZE * TILE_SIZE

screen = pg.display.set_mode(SIZE)

field_sprites = pg.sprite.Group()
box_sprites = pg.sprite.Group()
player_sprites = pg.sprite.Group()

transparent = (0, 0, 0, 0)
dark_green = pg.Color("darkGreen")


class Frames:
    def __init__(self, filename, rows, cols, def_size, sep, scale=1):
        self.filename = filename
        self.frames = []
        self.def_size = self.def_w, self.def_h = def_size  # default
        self.size = self.w, self.h = round(self.def_w * scale), round(
            self.def_h * scale
        )
        self.__cut_frames(rows, cols, sep)

    def __load_img(self):
        base_path = os.path.basename(os.path.dirname(__file__))
        img_path = os.path.join(base_path, self.filename)
        try:
            img = pg.image.load(img_path).convert_alpha()
        except pg.error as message:
            print("Cannot load image:", self.filename)
            raise SystemExit(message)
        return img

    def __cut_frames(self, rows, cols, sep):
        sheet = self.__load_img()
        for row in range(rows):
            for col in range(cols):
                frame_pos = ((self.def_w + sep) * col, (self.def_h + sep) * row)
                frame = sheet.subsurface(pg.Rect(frame_pos, self.def_size))
                frame_resized = pg.transform.scale(frame, self.size)
                self.frames.append(frame_resized)


class Field(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(field_sprites)
        self.image = pg.Surface(SIZE, pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.move(0, 0)
        self.rows = self.cols = 10

        tiles = Frames(
            "assets\\B\\EarthboundTiles.png", 3, 5, (32, 32), 1, TILE_SIZE / 32
        )

        for row in range(self.rows):
            for col in range(self.cols):
                self.image.blit(
                    tiles.frames[randint(0, len(tiles.frames) - 1)],
                    (TILE_SIZE * col, TILE_SIZE * row),
                )
        for row in range(1, self.rows):
            pg.draw.line(
                self.image, dark_green, (0, row * TILE_SIZE), (W, row * TILE_SIZE)
            )
        for col in range(1, self.cols):
            pg.draw.line(
                self.image, dark_green, (col * TILE_SIZE, 0), (col * TILE_SIZE, H)
            )


class Box(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(box_sprites)
        box = Frames("assets\\B\\CompanionBox.png", 1, 1, (30, 41), 0, TILE_SIZE / 30)
        self.image = box.frames[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = ((x + 1 / 2) * TILE_SIZE, (y + 1) * TILE_SIZE)
        self.x, self.y = x, y

        self.boom = Frames(
            "assets\\B\\Boom.png", 1, 12, (96, 96), 0, TILE_SIZE * 1.5 / 96
        )
        self.broken = False
        self.boom_frame = 0

    def get_pos(self):
        return self.x, self.y

    def explode(self):
        if self.boom_frame == 0:
            self.broken = True
            self.image = pg.Surface(self.boom.size, pg.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.midbottom = (
                (self.x + 1 / 2) * TILE_SIZE,
                (self.y + 1) * TILE_SIZE,
            )

    def update(self):
        if self.broken:
            if self.boom_frame == len(self.boom.frames) - 1:
                self.kill()
            else:
                self.image.fill(transparent)
                self.image.blit(self.boom.frames[self.boom_frame], (0, 0))
            self.boom_frame += 1


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_sprites)
        self.ness = Frames("assets\\B\\Ness.png", 1, 4, (16, 24), 1, TILE_SIZE / 24)
        self.image = self.ness.frames[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = ((x + 1 / 2) * TILE_SIZE, (y + 1) * TILE_SIZE)

        self.x, self.y = x, y
        self.dir = 0  # 0 - front, 1 - left, 2 - back, 3 - right

    def get_future(self):
        if self.dir == 0:
            return self.x, self.y + 1
        if self.dir == 1:
            return self.x - 1, self.y
        if self.dir == 2:
            return self.x, self.y - 1
        if self.dir == 3:
            return self.x + 1, self.y

    def move(self, dir):
        self.dir = dir
        pos = self.get_future()
        for box in box_sprites:
            if box.get_pos() == pos:
                return
        if 0 <= pos[0] < LVL_SIZE and 0 <= pos[1] < LVL_SIZE:
            self.x, self.y = pos

    def update(self):
        self.image = self.ness.frames[self.dir]
        self.rect.midbottom = ((self.x + 1 / 2) * TILE_SIZE, (self.y + 1) * TILE_SIZE)


def lvl_gen():
    tile_num = LVL_SIZE**2
    box_tiles = {randint(0, tile_num - 1) for _ in range(randint(1, tile_num - 1))}
    for tile in box_tiles:
        Box(tile % LVL_SIZE, tile // LVL_SIZE)
    player_tile = randint(0, tile_num - 1)
    while player_tile in box_tiles:
        player_tile = randint(0, tile_num - 1)
    return box_tiles, player_tile


running = True
box_tiles, player_tile = lvl_gen()

# field instance
Field()
# box instances
for tile in box_tiles:
    Box(tile % LVL_SIZE, tile // LVL_SIZE)
# player instance
player = Player(player_tile % LVL_SIZE, player_tile // LVL_SIZE)

while running:
    field_sprites.draw(screen)
    player_sprites.draw(screen)
    box_sprites.draw(screen)

    player_sprites.update()
    box_sprites.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                for box in box_sprites:
                    if box.get_pos() == player.get_future():
                        box.explode()
            elif event.key == pg.K_DOWN:
                player.move(0)
            elif event.key == pg.K_LEFT:
                player.move(1)
            elif event.key == pg.K_UP:
                player.move(2)
            elif event.key == pg.K_RIGHT:
                player.move(3)

    pg.display.flip()
    CLOCK.tick(18)

pg.quit()
