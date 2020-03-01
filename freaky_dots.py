import numpy as np
import cv2
import pygame



class button:
    def __init__(self, position, size, clr=[100, 100, 100], cngclr=None, func=None, text='', font="Segoe Print", font_size=16, font_clr=[0, 0, 0]):
        self.clr    = clr
        self.size   = size
        self.func   = func
        self.surf   = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])


        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

    def draw(self):
        self.mouseover()

        self.surf.fill(self.curclr)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            self.func(*args)

class text:
    def __init__(self, msg, position, clr=[100, 100, 100], font=None, font_size=15, mid=False):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.txt_surf = self.font.render(msg, 1, clr)

        if len(clr) == 4:
            self.txt_surf.set_alpha(clr[3])

        if mid:
            self.position = self.txt_surf.get_rect(center=position)


    def draw(self):
        screen.blit(self.txt_surf, self.position)


class Slider():
    def __init__(self, name, val, maxi, mini, pos, size=100):
        self.val = val
        self.maxi = maxi  
        self.mini = mini  
        self.xpos = pos[0] 
        self.ypos = pos[1]
        self.surf = pygame.Surface((size, 50))
        self.hit = False  
        self.size = (size, 50)

        self.txt_surf = font.render(name, 1, BLACK)
        self.txt_rect = self.txt_surf.get_rect(center=(self.size[0]//2, 15))

        self.surf.fill(WHITE)
        pygame.draw.rect(self.surf, (100, 255, 0), [0, self.size[1] - 20, self.size[0], 5], 0)

        self.surf.blit(self.txt_surf, self.txt_rect)  

        self.button_surf = pygame.Surface((20, 20))
        self.button_surf.fill(TRANS)
        self.button_surf.set_colorkey(TRANS)
        pygame.draw.circle(self.button_surf, BLACK, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, MAGENTA, (10, 10), 4, 0)

    def draw(self):
        surf = self.surf.copy()

        pos = (int((self.val-self.mini)/(self.maxi-self.mini)*self.size[0]), 33)
        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)

        screen.blit(surf, (self.xpos, self.ypos))

    def move(self, value=None):
        if value != None:
            self.val = value
        else:   
            self.val = (pygame.mouse.get_pos()[0] - self.xpos) / self.size[0] * (self.maxi - self.mini) + self.mini
            if self.val < self.mini:
                self.val = self.mini
            if self.val > self.maxi:
                self.val = self.maxi
        return self.val



def click(buttons):
    pos = pygame.mouse.get_pos()
    for idx, button in enumerate(buttons):
        if button.rect.collidepoint(pos):
            button.call_back(idx)


def reset(i):
    global temp
    temp[i] = 0
    if i == 0:
        sliders[0].move(0)
    elif i == 1:
        sliders[1].move(0)

    elif i == 2:
        sliders[2].move(0)

    elif i == 3:
        temp[3] = 10
        noise.move(10)

def change(*_):
    global c_flag
    c_flag = False if c_flag else True


def trans_affine(image, angle, tx, ty):
    row, col, *_ = image.shape
    center = tuple(np.array([row, col]) // 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    tras_mat = np.array([[1.0, 0.0, -ty],
                         [0.0, 1.0,  tx]])
    
    new_image = cv2.warpAffine(image, rot_mat, (col, row))
    new_image = cv2.warpAffine(new_image, tras_mat, (col, row))

    return new_image

def gameloop():

    screen.fill(bg)
    
    for s in sliders:
        s.draw()

    noise.draw()

    for button in button_list:
        button.draw()


########################3
    if c_flag:
        screen.blit(grid_surf, left)
        pl1 = grid
    else:
        screen.blit(orig_surf, left)
        pl1 = plane1
###############################
    # angle = (angle + 1) % 360
    plane2 = trans_affine(pl1, angle, tx, ty)
    pygame.surfarray.blit_array(surf1, 255 - (pl1 + plane2))
    screen.blit(surf1, centre)

    pygame.surfarray.blit_array(surf1, plane2)
    screen.blit(surf1, right)


    cur_fps = font.render(str(int(clock.get_fps())), False, (255, 0, 0))
    screen.blit(cur_fps, (10, 10))
    

    t = text("original", (250, 20), clr=[0, 0, 0], mid=True)
    t.draw()
    t = text("original + affine", (770, 20), clr=[0, 0, 0], mid=True)
    t.draw()
    t = text("affine", (1290, 20), clr=[0, 0, 0], mid=True)
    t.draw()

    t = text(str(tx), (1350, 630), clr=[0, 0, 0])
    t.draw()
    t = text(str(ty), (1350, 680), clr=[0, 0, 0])
    t.draw()
    t = text(str(angle), (1350, 730), clr=[0, 0, 0])
    t.draw()
    t = text(str(per), (1350, 780), clr=[0, 0, 0])
    t.draw()

if __name__ == '__main__':

    pygame.init()


    screen_size = (1540, 800)
    size  = 500
    clr   = np.array([255, 0, 255])
    per = 10
    bg = (255, 255, 255)
    block_size = 5
    c_flag = True



    angle = 0
    tx = 0
    ty = 0
    percentage = per / 100
    centre = ((screen_size[0] - size) // 2, (screen_size[1] - size) // 2 - 100)
    left   = (centre[0] - size - 10, centre[1])
    right  = (centre[0] + size + 10, centre[1])

    plane1 = np.zeros((size, size,  3), np.uint8)
    surf1 = pygame.Surface((size, size))



    grid = np.zeros((size, size, 3))
    grid_surf = pygame.Surface((size, size))

    kernel = np.ones((block_size, block_size, 3)) * 255
    kernel[:, :, 0], kernel[:, :, 1], kernel[:, :, 2] = 255 - clr

    for i in range(0, size, block_size):
        for j in range(0, size, block_size):
            if ((i + j) // (block_size)) % 2 == 0:
                grid[i:i + block_size, j:j + block_size] = kernel

    pygame.surfarray.blit_array(grid_surf, grid)

    n_pixels = size * size
    for i in range(int(n_pixels * percentage)):
        plane1[np.random.randint(0, size), np.random.randint(0, size)] = 255 - clr

    orig_surf = pygame.Surface((size, size))
    pygame.surfarray.blit_array(orig_surf, plane1)

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('freaky dots')
    clock = pygame.time.Clock()

    font_size = 15
    font = pygame.font.Font(None, font_size)




    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 50, 50)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 50)
    BLUE = (50, 50, 255)
    GREY = (200, 200, 200)
    ORANGE = (200, 100, 50)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    TRANS = (1, 1, 1)

    flow = False

    noise = Slider("noise", 10, 100, 0, (100, 750), 1200)

    trans_x = Slider("translate_x", 0, size, -size, (100, 600), 1200)
    trans_y = Slider("translate_y", 0, size, -size, (100, 650), 1200)
    rotat_x = Slider(     "rotate", 0,   60,   -60, (100, 700), 1200)
    sliders = [trans_x, trans_y, rotat_x]



    r1 = button((60, 625), (70, 50), (220, 220, 220), YELLOW, reset, 'RESET')
    r2 = button((60, 675), (70, 50), (220, 220, 220), YELLOW, reset, 'RESET')
    r3 = button((60, 725), (70, 50), (220, 220, 220), YELLOW, reset, 'RESET')
    r4 = button((60, 775), (70, 50), (220, 220, 220), YELLOW, reset, 'RESET')
    gn = button((60, 25), (100, 50), (220, 220, 220), YELLOW, change, 'noise/grid')

    button_list = [r1, r2, r3, r4, gn]


    temp = [0, 0, 0, 10]

    crash = True
    old_per = per
    while crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crash = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    crash = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click(button_list)
                pos = pygame.mouse.get_pos()
                if noise.button_rect.collidepoint(pos):
                        noise.hit = True
                for s in sliders:
                    if s.button_rect.collidepoint(pos):
                        s.hit = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for s in sliders:
                    s.hit = False
                noise.hit = False

        for idx, s in enumerate(sliders):
            if s.hit:
                temp[idx] = s.move()

        if noise.hit:
            temp[3] = noise.move()

        tx, ty, angle, per = temp

        if old_per != per:
            old_per = per
            plane1 = np.zeros((size, size,  3), np.uint8)
            for i in range(int(n_pixels * (per / 100))):
                plane1[np.random.randint(0, size), np.random.randint(0, size)] = 255 - clr

            orig_surf = pygame.Surface((size, size))
            pygame.surfarray.blit_array(orig_surf, plane1)

        gameloop()
        
        pygame.display.update()
        clock.tick(144)
