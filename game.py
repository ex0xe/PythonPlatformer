

import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join


### BUG:
### Player can still be glitched up the block if he jumps and moves at the same time when at the upper edge of the block
### jump animation bugging at the start sometimes (probably because if player falls off a block and then jumps, he can jump again)
### laggy if screen size is bigger (probably wont be implemented)
### after changing screen size via button ingame, screen is not in center
### sprite looks weird while moving (seems normal), probably because of collision detection
### if player double jumps then wall jumps, wall jump animation is not played (but double jump animation is played)
### if player changes direction to left instead of standard right, then sprite in main menu will also be turned left and the spawn is also with direction left



### TODO:
### Second Dropdown in main menu for background maybe (done, adjust to screen size)
### adjust everything to screen size (probably not because laggy)
#### Change background depending on chosen character (?)
### Pause menu (Pause implemented, now the actual pause menu)
#### Options now
### make kill() function for Player class when falling out of map (maybe with a timer)
##-> freeze screen and make a button that restarts level
### MAKE EVERYTHING IN CLASSES AND MORE FILES
#### change button size of "Game paused" and other buttons in pause menu depending on screen size and their position
#### best thing to do: change everything, update everything when resolution is changed; BUT when increased screen size is adjusted to screen, it stops lagging
#### + game is under taskbar
#### quit game square button with "Leave" (Arrow, Sprite) - symbol top right in pause_menu to quit game (right now there is only a button under options)
##### maybe add sprite to character )
### cool main menu background (maybe animated)
### Sounds
### Enemies
### More traps


pygame.init()

pygame.display.set_caption("Platformer")

BASE_WIDTH, BASE_HEIGHT = 1280, 720
WIDTH, HEIGHT = 1280, 720
FPS = 60
BASE_PLAYER_VEL = 5
BASE_GRAVITY = 1
BASE_XVELOCITY = 1
WALL_JUMP_FORCE = 20
OFFSET_X = 0
SCROLL_AREA_WIDTH = 400
OFFSET_Y = 0
SCROLL_AREA_HEIGHT = 300
CHOSEN_CHARACTER_INPUT = "" 
CHOSEN_CHARACTER = {1: "MaskDude", 2: "NinjaFrog", 3: "PinkMan", 4: "VirtualGuy"}
CHOSEN_CHARACTER_KEY = 0
CHOSEN_CHARACTER_VALUE = "MaskDude"
CHOSEN_BACKGROUND = {1: "Blue.png", 2: "Brown.png", 3: "Gray.png", 4: "Green.png", 5: "Pink.png", 6: "Purple.png", 7: "Yellow.png"}
BACKGROUND = "Blue.png"
block_size = 96
objects = []


window = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))


def flip(sprites):
    """if called, the function flips the sprite at the x-axis"""
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def set_background (background):
    """method takes the background as parameter and sets it as the new background"""

    global BACKGROUND
    character = BACKGROUND
    for key, value in CHOSEN_BACKGROUND.items():
        if key == (background + 1):
            character = value

    BACKGROUND = character

def pause_menu(toggle=False):
    if toggle:
        pass


def start_game(in_main_menu):
    if in_main_menu == True:
        in_main_menu = False


def display_message(message, w, h):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=(w, h))
    window.blit(text, text_rect)


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """method goes into "assets" and then first directory dir1 and then sub-directory dir2
    then loads the sprite sheet and loops through images
    and updates the all_sprites dict by turning the images/sprites to playable Rectangles
    at the end it returned the all_sprites dict"""
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(width, height):
    """ method takes width and height as parameter and returns a block with the given width and height"""
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, width, height)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Game:
    OFFSET_X = 0
    OFFSET_Y = 0
    def __init__(self):
        self.in_main_menu = True
        #self.reset_game()

    def start_game(self):
        self.in_main_menu = False
        self.reset_game()
    
    def back_to_main_menu(self):
        self.in_main_menu = True
        self.reset_game()
        #playe

    def reset_game(self):
        global OFFSET_X 
        global OFFSET_Y 
        OFFSET_X = 0      
        OFFSET_Y = 0 


class PauseMenu:
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def handle_click(self, pos):
        for button in self.buttons:
            button.check_click(pos)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SPRITES = load_sprite_sheets("MainCharacters", CHOSEN_CHARACTER_VALUE, 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, gravity, xvelocity):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.GRAVITY = gravity
        self.XVELOCITY = xvelocity
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.can_wall_jump = False
        self.collide_wall_side = None

    

    def draw_hitbox(self, surface, color=(255, 0, 0)):
        pygame.draw.rect(surface, color, self.rect, 2)

    def set_character(self, character_key):
        global CHOSEN_CHARACTER_VALUE
        
        character = CHOSEN_CHARACTER_VALUE
        for key, value in CHOSEN_CHARACTER.items():
            if key == (character_key + 1):
                character = value
                
                
        CHOSEN_CHARACTER_VALUE = character
        
        self.SPRITES = load_sprite_sheets(
            "MainCharacters", CHOSEN_CHARACTER_VALUE, 32, 32, True
        )


        self.animation_count = 0
        self.update_sprite()

    def reset_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.x_vel = 0
        self.y_vel = 0
        # Reset other properties if needed
        self.update()

    
    def jump(self):
        
        collide_left = collide(self, objects, -PLAYER_VEL * 2)
        collide_right = collide(self, objects, PLAYER_VEL * 2)
        if (collide_left or collide_right) and self.fall_count > 0 and self.jump_count != 0:
            # Apply horizontal force for wall jump
            self.direction = "left" if collide_right else "right"
            self.y_vel = -self.GRAVITY * 8  # Vertical jump velocity
            self.x_vel = WALL_JUMP_FORCE * (-3 if collide_right else 3)  # Horizontal force
            #self.can_wall_jump = False
            self.fall_count = 0
            self.can_wall_jump = True

        elif self.jump_count < 2:
            self.y_vel = -self.GRAVITY * 8
            self.animation_count = 0
            self.jump_count += 1
            self.fall_count = 0
            
        self.animation_count = 0


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True
        self.hit_count = 0

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        """ if self.can_wall_jump == True:
            self.x_vel += min(1, (self.fall_count / fps) * self.XVELOCITY) """
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1

        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                if self.can_wall_jump == True:
                    sprite_sheet = "wall_jump"
                    self.can_wall_jump = False
                
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                if self.can_wall_jump == True:
                    self.can_wall_jump = False
                    sprite_sheet = "wall_jump"
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES.get(sprite_sheet_name, [])
        if sprites:
            sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
            self.sprite = sprites[sprite_index]

        self.animation_count += 1

        self.update()


    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x, offset_y):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x, offset_y):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

""" class CheckpointEnd(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "end")
        self.checkpoint = load_sprite_sheets("Checkpoints", "End", width, height)
        self.image = self.checkpoint["End (Idle)"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_count = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.checkpoint[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0        
 """

class Block(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)
        block = get_block(width, height)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            current_color = self.hover_color
        else:
            current_color = self.color
        pygame.draw.rect(screen, current_color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        # center=(self.rect.centerx // WIDTH, self.rect.centery // HEIGHT // 2)
        screen.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()


class ResolutionButton(Button):
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        color,
        hover_color,
        resolution,
        background,
        bg_image,
        player,
        objects,
        OFFSET_X,
        OFFSET_Y,
    ):
        super().__init__(
            x, y, width, height, text, color, hover_color, self.change_resolution_action
        )
        self.resolution = resolution
        self.background = background
        self.bg_image = bg_image
        self.player = player
        self.objects = objects
        self.OFFSET_X = OFFSET_X
        self.OFFSET_Y = OFFSET_Y

    def change_resolution_action(self):
        change_resolution(
            self.resolution[0],
            self.resolution[1],
            self.background,
            self.bg_image,
            self.player,
            self.objects,
            self.OFFSET_X,
            self.OFFSET_Y,
        )



class OptionBox:
    def __init__(
        self, x, y, w, h, color, highlight_color, font, option_list, selected=0
    ):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(
            surf, self.highlight_color if self.menu_active else self.color, self.rect
        )
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(
                    surf,
                    self.highlight_color if i == self.active_option else self.color,
                    rect,
                )
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
                self.rect.x,
                self.rect.y + self.rect.height,
                self.rect.width,
                self.rect.height * len(self.option_list),
            )
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    
                    return self.active_option
        return -1


def change_resolution(
    width_input, height_input, background, bg_image, player, objects, OFFSET_X, OFFSET_Y
):
    global WIDTH
    global HEIGHT
    global window
    global SCROLL_AREA_WIDTH
    global SCROLL_AREA_HEIGHT

    WIDTH = width_input
    HEIGHT = height_input
    SCROLL_AREA_WIDTH = 400
    SCROLL_AREA_HEIGHT = 300

    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    player_rect = player.rect
    new_offset_x = max(
        0, min(player_rect.x - WIDTH // 2, len(background) * block_size - WIDTH)
    )
    new_offset_y = max(0, min(player_rect.y - HEIGHT // 2, block_size * 4))

    OFFSET_X = new_offset_x
    OFFSET_Y = new_offset_y


    draw(window, background, bg_image, player, objects, OFFSET_X, OFFSET_Y)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(-BASE_WIDTH // width - 1, (BASE_WIDTH * 2) // width + 2):
        for j in range(-BASE_HEIGHT // height - 4, (BASE_HEIGHT * 2) // height + 2):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x, offset_y):
   

    for tile in background:
       
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x, offset_y)
        # print(window)

    player.draw(window, offset_x, offset_y)

    pygame.display.update()


def create_objects():
    floor = [
        Block(i * block_size, BASE_HEIGHT - block_size, block_size, block_size)
        for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size, )
    ]
    global objects
    objects = [
        *floor,
        Block(block_size * -6, BASE_HEIGHT - block_size * 2, block_size, block_size),
        Block(block_size * -6, BASE_HEIGHT - block_size * 3, block_size, block_size),
        Block(block_size * -6, BASE_HEIGHT - block_size * 4, block_size, block_size),
        Block(block_size * -6, BASE_HEIGHT - block_size * 5, block_size, block_size),
        Block(0, BASE_HEIGHT - block_size * 2, block_size, block_size),
        Block(0, BASE_HEIGHT - block_size * 3, block_size, block_size),
        Block(block_size * 4, BASE_HEIGHT - block_size * 4, block_size, block_size),
        Block(block_size * 9, BASE_HEIGHT - block_size * 4, block_size, block_size),
        Block(block_size * 12, BASE_HEIGHT - block_size * 6, block_size, block_size),
        Block(block_size * 16, BASE_HEIGHT - block_size * 8, block_size, block_size),
        Block(block_size * 12, BASE_HEIGHT - block_size * 10, block_size, block_size),
        Block(block_size * 16, BASE_HEIGHT - block_size * 12, block_size, block_size),
        Block(block_size * 20, BASE_HEIGHT - block_size * 14, block_size, block_size),
        Block(block_size * 23, BASE_HEIGHT - block_size * 16, block_size, block_size),
        Block(block_size * 20, BASE_HEIGHT - block_size * 18, block_size, block_size),
        Block(block_size * 19, BASE_HEIGHT - block_size * 18, block_size, block_size),
        Block(block_size * 18, BASE_HEIGHT - block_size * 18, block_size, block_size),
        Block(block_size * 18, BASE_HEIGHT - block_size * 18, block_size, block_size),
    ]


def handle_vertical_collision(player, objects):
    #collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if player.y_vel > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif player.y_vel < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects, can_move):
    keys = pygame.key.get_pressed()
    

    player.x_vel = 0
    # multipliziert mit 2, da immernoch manchmal der Bug entsteht, dass wenn der Spieler sich bewegt, er auf den Block "teleportiert wird"
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)
    

    

    if can_move:
        if keys[pygame.K_a] and not collide_left:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_d] and not collide_right:
            player.move_right(PLAYER_VEL)
      


def scroll_background(player):
    global OFFSET_X
    global OFFSET_Y
    global SCROLL_AREA_HEIGHT
    global SCROLL_AREA_WIDTH

    if (
        (player.rect.right - OFFSET_X >= WIDTH - SCROLL_AREA_WIDTH) and player.x_vel > 0
    ) or ((player.rect.left - OFFSET_X <= SCROLL_AREA_WIDTH) and player.x_vel < 0):
        OFFSET_X += player.x_vel

    if (
        (player.rect.top - OFFSET_Y >= HEIGHT - SCROLL_AREA_HEIGHT) and player.y_vel > 0
    ) or ((player.rect.bottom - OFFSET_Y <= SCROLL_AREA_HEIGHT) and player.y_vel < 0):
        OFFSET_Y += player.y_vel


def quit_game():
    pygame.quit()
    quit()


def main(window):
    game = Game()

    global WIDTH
    global HEIGHT
    global OFFSET_X
    global OFFSET_Y
  

    clock = pygame.time.Clock()
    global PLAYER_VEL
    fire = Fire(200, BASE_HEIGHT - block_size - 64, 16, 32)
    fire.on()
    scale_factor = ((WIDTH / BASE_WIDTH) + (HEIGHT / BASE_HEIGHT)) / 2

    PLAYER_VEL = BASE_PLAYER_VEL * scale_factor

    scaled_gravity = BASE_GRAVITY * scale_factor
    scaled_xvelocity = BASE_XVELOCITY * scale_factor
    
    #player = Player(100, 100, 50, 50, scaled_gravity)

    list1 = OptionBox(
        10,
        40,
        160,
        40,
        (150, 150, 150),
        (100, 200, 255),
        pygame.font.SysFont(None, 30),
        ["MaskDude", "NinjaFrog", "PinkMan", "VirtualGuy"],
    )

    list2 = OptionBox(
        WIDTH - 170,
        40,
        160,
        40,
        (150, 150, 150),
        (100, 200, 255),
        pygame.font.SysFont(None, 30),
        ["Blue", "Brown", "Gray", "Green", "Pink", "Purple", "Yellow"],
    )
 

    resolution_button = Button(
        (WIDTH - 200) // 2,
        (HEIGHT - 50) // 2,
        200,
        50,
        "Change Resolution",
        (255, 0, 0),
        (150, 0, 0),
        lambda: change_resolution(
            1920, 1080, background, bg_image, player, objects, OFFSET_X, OFFSET_Y
        ),
    )

    options_button_pause_menu = Button(
        (WIDTH - 200) // 2,
        (HEIGHT - 50) // 2,
        200,
        50,
        "Options",
        (255, 0, 0),
        (150, 0, 0),
        lambda: ()
    )

    resume_button_pause_menu = Button(
        (WIDTH - 200) // 2,
        (HEIGHT - 50) // 2.5,
        200,
        50,
        "Resume",
        (255, 0, 0),
        (150, 0, 0),
        lambda: quit_pause_menu(0, False, True)
    )

    start_button = Button(
        (WIDTH - 200) // 2,
        (HEIGHT - 50) // 2.5,
        200,
        50,
        "Start",
        (255, 0, 0),
        (150, 0, 0),
        lambda: game.start_game(),
    )

    pause_menu_back_to_main_menu = Button(
        (WIDTH - 200) // 2,
        (HEIGHT - 50) // 3.95,
        200,
        50,
        "Main Menu",
        (255, 0, 0),
        (150, 0, 0),
        game.back_to_main_menu,
    )

    quit_button_main_menu = Button(
        (WIDTH - 200) // 2,
        (HEIGHT - 50) // 1.65,
        200,
        50,
        "Quit",
        (255, 0, 0),
        (150, 0, 0),
        lambda: quit_game(),
    )

    

    create_objects()
    pygame.display.flip()
    # collision_detected = player.collide_with_block_side(objects)

    # change button size depending on screen size, here: 200 and 50

    run = True
    in_pause_menu = False
    freeze_start_time = 0
    can_move = True
    escape_press_count = 0
    chose_player_count = 0
    reset_offsets = True
    # in_main_menu = True

    
    
    def quit_pause_menu(e, i, c):
        nonlocal escape_press_count, in_pause_menu, can_move
        escape_press_count = e
        in_pause_menu = i
        can_move = c

    initial_player_x = 100
    initial_player_y = 100

    player = Player(initial_player_x, initial_player_y, 50, 50, scaled_gravity, scaled_xvelocity)
    while run:
        event_list = pygame.event.get()
        background, bg_image = get_background(BACKGROUND)
        
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_SPACE):


                    """ if (player.jump_count < 2
                    and not in_pause_menu): """
                    if not in_pause_menu:
                        player.jump()

                    

                
                elif event.key == pygame.K_ESCAPE and not game.in_main_menu:
                    in_pause_menu = not in_pause_menu
                    can_move = not in_pause_menu

                    if reset_offsets:
                        OFFSET_X = 0
                        OFFSET_Y = 0
                        reset_offsets = False
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if in_pause_menu:
                    resume_button_pause_menu.check_click(pygame.mouse.get_pos())
                    options_button_pause_menu.check_click(pygame.mouse.get_pos())
                    pause_menu_back_to_main_menu.check_click(pygame.mouse.get_pos())
                if game.in_main_menu:
                    start_button.check_click(pygame.mouse.get_pos())
                    quit_button_main_menu.check_click(pygame.mouse.get_pos())
                


        if not in_pause_menu and not game.in_main_menu:
            clock.tick(FPS)
            player.loop(FPS)
            #player.update()
            
            fire.loop()
            handle_move(player, objects, can_move)
            #handle_horizontal_collision(player, objects)
            handle_vertical_collision(player, objects)
            
            draw(window, background, bg_image, player, objects, OFFSET_X, OFFSET_Y)
            scroll_background(player)
            

        elif in_pause_menu and not game.in_main_menu:
            #resolution_button.draw(window)
            resume_button_pause_menu.draw(window)
            options_button_pause_menu.draw(window)
            pause_menu_back_to_main_menu.draw(window)
            
            display_message("Game paused", (WIDTH // 2), (HEIGHT // 3))
            current_time = pygame.time.get_ticks()
            if current_time - freeze_start_time > 2000:
                pass

            clock.tick(FPS)
            
            pygame.display.flip()
        elif game.in_main_menu:

            clock.tick(FPS)
           
            window.fill((255, 255, 255))
            selected_option_character = list1.update(event_list)
            player.set_character(selected_option_character)

            selected_option_background = list2.update(event_list)
            set_background(selected_option_background)
            
            
            window.blit(bg_image, (1000, 30)) # need to be changed with screen size if other screen size is chosen
            
            #player.update_sprite()
            #player.loop(FPS)
            player.draw(window, -100, 80) # need to be changed with screen size if other screen size is chosen
            start_button.draw(window)

            quit_button_main_menu.draw(window)

            list2.draw(window)
            
            list1.draw(window)

            player.reset_position(100, 100)

            
            pygame.display.flip()

        pygame.display.flip() 

    pygame.display.flip()
    quit_game()


if __name__ == "__main__":
    main(window)
