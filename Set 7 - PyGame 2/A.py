import os
import random as rd
import pygame as pg

pg.init()
pg.display.set_caption("Шарики - Sonic")
clock = pg.time.Clock()
size = width, height = 500, 500
screen = pg.display.set_mode(size)

sprites = pg.sprite.Group()
sprite_size = sprite_w, sprite_h = 48, 48

transparent = (0, 0, 0, 0)
black = pg.Color("black")
white = pg.Color("white")


class Frames:
    def __init__(self, filename, rows, cols, sep, scale=1):
        self.filename = filename
        self.frames = []
        self.def_size = self.def_w, self.def_h = sprite_size  # default
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


sonic_scale = 1.75
sonic = Frames("assets\\A\\sonic.png", 1, 8, 4, sonic_scale)

shield_scale = sonic_scale * sonic.def_w / (sonic.def_w - 4)
shield = Frames("assets\\A\\shield.png", 1, 2, 8, shield_scale)


class Sonic(pg.sprite.Sprite):
    def __init__(self, pos=screen.get_rect().center):
        super().__init__(sprites)
        self.image = pg.Surface(shield.size, pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = round(shield.w / 2) + 1
        self.sonic_frame = 2  # looking to front frame
        self.shield_frame = 0
        self.__update_img()

        self.pos = pg.math.Vector2(pos)
        self.speed = 6
        self.dir = pg.math.Vector2(rd.uniform(-1, 1), rd.uniform(-1, 1)).normalize()

    def __update_img(self):
        cur_sonic = sonic.frames[self.sonic_frame]
        rect_sonic = cur_sonic.get_rect()
        posx = round(self.rect.w / 2)
        posy = round((3.75 * self.rect.h + sonic.h) / 6)
        rect_sonic.midbottom = (posx, posy)

        cur_shield = shield.frames[self.shield_frame]

        self.image.fill(transparent)
        self.image.blits(((cur_sonic, rect_sonic), (cur_shield, (0, 0))))

    def __update_frame(self):
        self.sonic_frame = (self.sonic_frame + 1) % len(sonic.frames)
        self.shield_frame = (self.shield_frame + 1) % len(shield.frames)

    def __update_pos(self):
        self.pos += self.dir * self.speed
        self.rect.center = tuple(map(round, self.pos))

    def __update_dir(self):
        def collide(sprite1, sprite2):
            if sprite1 is sprite2:
                return False
            else:
                return pg.sprite.collide_circle(sprite1, sprite2)

        def bounce(normal):
            normalVector = pg.math.Vector2(normal)
            self.dir = self.dir.reflect(normalVector)

        collisions = pg.sprite.spritecollide(self, sprites, False, collide)
        if collisions:
            for collision in collisions:
                bounce(collision.pos - self.pos)
        if self.rect.top <= margin:
            bounce((0, -1))
        if self.rect.bottom >= height - margin:
            bounce((0, 1))
        if self.rect.left <= margin:
            bounce((1, 0))
        if self.rect.right >= width - margin:
            bounce((-1, 0))

    def update(self):
        self.__update_dir()
        self.__update_pos()
        self.__update_frame()
        self.__update_img()


running = True
margin = 20
borders = pg.Rect(margin, margin, width - 2 * margin, height - 2 * margin)
click_area = pg.Rect(
    margin + sprite_w,
    margin + sprite_h,
    width - 2 * (margin + sprite_w),
    height - 2 * (margin + sprite_h),
)

Sonic()

while running:
    screen.fill(black)

    pg.draw.rect(screen, white, borders, 1)
    sprites.draw(screen)
    sprites.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if click_area.collidepoint(mouse_pos):
                new_sonic = pg.sprite.Sprite()
                new_sonic.rect = pg.Rect((0, 0), sprite_size)
                new_sonic.rect.center = mouse_pos
                if not pg.sprite.spritecollideany(new_sonic, sprites):
                    Sonic(mouse_pos)

    pg.display.flip()
    clock.tick(24)

pg.quit()
