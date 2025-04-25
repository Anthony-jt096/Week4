import sys
import pygame
import random

LINK_PATH     = r'C:\Users\Anthony T\Downloads\link1.png'
TRIFORCE_PATH = r'C:\Users\Anthony T\Downloads\triforce_test.png'
HEART_PATH    = r'C:\Users\Anthony T\Downloads\heart.png'
RUPEE_PATH    = r'C:\Users\Anthony T\Downloads\rupee.png'
CURSOR_PATH   = r'C:\Users\Anthony T\Downloads\triforce_test.png'

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Links Adventure")
        self.screen = pygame.display.set_mode((1080, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Times New Roman', 24, bold=True)
        self.link_img     = pygame.transform.scale(pygame.image.load(LINK_PATH),     (50, 50))
        self.triforce_img = pygame.transform.scale(pygame.image.load(TRIFORCE_PATH), (40, 40))
        self.heart_img    = pygame.transform.scale(pygame.image.load(HEART_PATH),    (20, 20))
        self.rupee_img    = pygame.transform.scale(pygame.image.load(RUPEE_PATH),    (30, 30))
        self.cursor_img   = pygame.transform.scale(pygame.image.load(CURSOR_PATH),   (32, 32))
        pygame.mouse.set_visible(False)
        self.maze_done = False
        self.current = MazeMode(self)
        self.modes = {
            "1": AnimationMode(self),
            "2": ShapeDrawMode(self),
            "3": SliderMode(self),
            "4": PaintMode(self),
            "5": DataVizMode(self),
        }

    def main_menu(self):
        self.screen.fill((10, 10, 30))
        lines = [
            "Maze Complete! Choose your next trial:",
            "1: Triforce Animation",
            "2: Draw Rupee Shapes",
            "3: Tint Link’s Tunic",
            "4: Paint with Hearts",
            "5: Bar Chart",
        ]
        for i, txt in enumerate(lines):
            surf = self.font.render(txt, True, (200, 200, 100))
            self.screen.blit(surf, (50, 50 + i * 40))

    def run(self):
        while True:
            dt = self.clock.tick(1000) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.maze_done:
                    self.current.handle_event(event)
                else:
                    if self.current is None:
                        if event.type == pygame.KEYDOWN and event.unicode in self.modes:
                            self.current = self.modes[event.unicode]
                    else:
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            self.current = None
                        else:
                            self.current.handle_event(event)

            self.screen.fill((0, 0, 0))
            if not self.maze_done:
                self.current.update(dt)
                self.current.draw(self.screen)
                if self.maze_done:
                    self.current = None
            else:
                if self.current is None:
                    self.main_menu()
                else:
                    self.current.update(dt)
                    self.current.draw(self.screen)
            mx, my = pygame.mouse.get_pos()
            self.screen.blit(self.triforce_img, (mx, my))
            pygame.display.flip()

class MazeMode:
    def __init__(self, game):
        self.g = game
        W, H = game.screen.get_size()
        self.img = self.g.link_img
        self.img_pos = [50, 50]
        self.movement = [False, False, False, False]
        self.walls = [
            pygame.Rect(0, 0, W, 10), pygame.Rect(0, 0, 10, H),
            pygame.Rect(0, H - 10, W, 10), pygame.Rect(W - 10, 0, 10, H),
            pygame.Rect(100, 0, 10, 600),
            pygame.Rect(100, 600, 800, 10),
            pygame.Rect(900, 100, 10, 510),
            pygame.Rect(200, 100, 710, 10),
            pygame.Rect(200, 100, 10, 400),
            pygame.Rect(200, 500, 600, 10),
            pygame.Rect(800, 200, 10, 300),
            pygame.Rect(300, 200, 510, 10),
            pygame.Rect(300, 200, 10, 200),
            pygame.Rect(300, 400, 400, 10),
        ]
        self.exit_rect = pygame.Rect(305, 210, 400, 10)
        self.instruction_font = pygame.font.SysFont('Arial', 20)
        self.instruction_timer = 3000  # show for 3 seconds

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w: self.movement[0] = True
            elif e.key == pygame.K_s: self.movement[1] = True
            elif e.key == pygame.K_a: self.movement[2] = True
            elif e.key == pygame.K_d: self.movement[3] = True
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_w: self.movement[0] = False
            elif e.key == pygame.K_s: self.movement[1] = False
            elif e.key == pygame.K_a: self.movement[2] = False
            elif e.key == pygame.K_d: self.movement[3] = False

    def update(self, dt):
        if self.instruction_timer > 0:
            self.instruction_timer -= dt * 1000

        prev_x = self.img_pos[0]
        self.img_pos[0] += (self.movement[3] - self.movement[2]) * 5
        r = pygame.Rect(self.img_pos[0], self.img_pos[1], *self.img.get_size())
        if any(r.colliderect(w) for w in self.walls):
            self.img_pos[0] = prev_x

        prev_y = self.img_pos[1]
        self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5
        r = pygame.Rect(self.img_pos[0], self.img_pos[1], *self.img.get_size())
        if any(r.colliderect(w) for w in self.walls):
            self.img_pos[1] = prev_y

        if r.colliderect(self.exit_rect):
            self.g.maze_done = True

    def draw(self, surf):
        surf.fill((14, 120, 20))
        for w in self.walls:
            pygame.draw.rect(surf, (0,0,0), w)
        surf.blit(self.g.rupee_img, self.exit_rect.topleft)
        surf.blit(self.img, self.img_pos)

        if self.instruction_timer > 0:
            txt = self.instruction_font.render("Use W A S D to move", True, (255, 255, 200))
            surf.blit(txt, (50, 650))

class AnimationMode:
    def __init__(self, game):
        self.g = game
        self.x = -self.g.triforce_img.get_width()
        self.speed = 200
    def handle_event(self, e): pass
    def update(self, dt):
        self.x = (self.x + self.speed * dt) % self.g.screen.get_width()
    def draw(self, surf):
        surf.fill((10,60,20))
        surf.blit(self.g.triforce_img, (int(self.x), 340))

class ShapeDrawMode:
    def __init__(self, game):
        self.g = game
        self.points = []
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.points.append(e.pos)
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_c:
            self.points.clear()
    def update(self, dt): pass
    def draw(self, surf):
        surf.fill((0,0,0))
        if len(self.points) > 1:
            pygame.draw.lines(surf, (0,255,128), False, self.points, 3)
        for p in self.points:
            surf.blit(self.g.rupee_img, (p[0]-15, p[1]-15))

class Slider:
    def __init__(self, rect, name, mi, ma, v):
        self.rect = pygame.Rect(rect)
        self.name, self.mi, self.ma, self.value = name, mi, ma, v
        self.drag = False
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos):
            self.drag = True
        elif e.type == pygame.MOUSEBUTTONUP:
            self.drag = False
        elif e.type == pygame.MOUSEMOTION and self.drag:
            x = max(self.rect.x, min(e.pos[0], self.rect.right))
            pct = (x - self.rect.x) / self.rect.width
            self.value = int(self.mi + pct * (self.ma - self.mi))
    def draw(self, surf, font):
        pygame.draw.rect(surf, (80,80,80), self.rect)
        kx = self.rect.x + int((self.value-self.mi)/(self.ma-self.mi)*self.rect.width)
        pygame.draw.circle(surf, (200,180,50), (kx, self.rect.centery), 8)
        lbl = font.render(f"{self.name}: {self.value}", True, (255,255,255))
        surf.blit(lbl, (self.rect.x, self.rect.y-25))

class SliderMode:
    def __init__(self, game):
        self.g = game
        self.sliders = [
            Slider((100,100,300,20), 'Red',   0,255,100),
            Slider((100,180,300,20), 'Green', 0,255,200),
            Slider((100,260,300,20), 'Blue',  0,255,50),
        ]
    def handle_event(self, e):
        for s in self.sliders:
            s.handle_event(e)
    def update(self, dt): pass
    def draw(self, surf):
        surf.fill((20,20,60))
        r,g,b = [s.value for s in self.sliders]
        img = self.g.link_img.copy()
        img.fill((r,g,b), special_flags=pygame.BLEND_MULT)
        surf.blit(img, (515,335))
        for s in self.sliders:
            s.draw(surf, self.g.font)

class PaintMode:
    def __init__(self, game):
        self.g = game
        self.paths = []
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.paths.append([e.pos])
        elif e.type == pygame.MOUSEMOTION and e.buttons[0]:
            self.paths[-1].append(e.pos)
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_c:
            self.paths.clear()
    def update(self, dt): pass
    def draw(self, surf):
        surf.fill((30,30,30))
        for path in self.paths:
            for p in path:
                surf.blit(self.g.heart_img, (p[0]-10, p[1]-10))

class DataVizMode:
    def __init__(self, game):
        self.g = game
        self.labels = ["Forest","Desert","Castle","Sea","Mountains"]
        self.data   = [random.randint(1,20) for _ in self.labels]
    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            self.data = [random.randint(1,20) for _ in self.labels]
    def update(self, dt): pass
    def draw(self, surf):
        surf.fill((0,20,40))
        W,H = surf.get_size()
        bar_w = W//len(self.data)-20
        mx = max(self.data)
        for i, v in enumerate(self.data):
            x = 20 + i*(bar_w+20)
            h = int(v/mx*(H-100))
            y = H - h - 50
            pygame.draw.rect(surf, (0,200,200), (x,y,bar_w,h))
            surf.blit(self.g.rupee_img, (x+bar_w//2-15, y-40))
            txt = self.g.font.render(f"{self.labels[i]} ({v})", True, (220,220,220))
            surf.blit(txt, (x, H-45))

if __name__ == "__main__":
    Game().run()
