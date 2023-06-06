import pygame
from constants import *

# ---- PLAYER COMPONENT ---
class Player:
    def __init__(self, x, y):
        self.Initialize(x, y)

    def Update(self, tiles, isGameOver, world):
        # update the player position
        # and update the game states (gameover, collisions, ...)
        dx = 0
        dy = 0
        game_state = isGameOver

        if isGameOver == 0:
            if self.rect.y > HEIGHT:
                game_state = -1
                self.deathFX.play()
                return game_state
            # Handle The player inputs
            keys = pygame.key.get_pressed()

            # Calculate the new player position
            if keys[pygame.K_LEFT]:
                # Player move to the left
                dx -= SPEED
                self.direction = -1
                self.images = self.facing_left
                self.Animate("WALK")
            elif keys[pygame.K_RIGHT]:
                # Player move to the right
                dx += SPEED
                self.direction = 1
                self.images = self.facing_right
                self.Animate("WALK")
            
            if keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
                self.frame_counter = 0
                self.frame_index = 0
                self.image = self.images[self.frame_index]
                
            if keys[pygame.K_SPACE] and self.jumped == False and self.is_grounded:
                self.velY = -JUMP_VEL
                self.jumped = True
                self.jumpFX.play()
                # Play The Jump FX
            elif keys[pygame.K_SPACE] == False:
                self.jumped = False
            
            # ADD GRAVITY
            self.velY += 1
            if self.velY > 10:
                self.velY = 10
            dy += self.velY

            game_state, dx, dy = self.HandleCollisions(dx, dy, tiles, world)

            # Update the player position
            self.rect.x += dx
            self.rect.y += dy 
            self.collide_rect.x += dx
            self.collide_rect.y += dy

            # if self.rect.bottom > HEIGHT-TILESIZE:           
            #     self.rect.bottom = HEIGHT-TILESIZE
            #     self.collide_rect.bottom = HEIGHT-TILESIZE

            return game_state

    def Animate(self, animation_name):
        if animation_name == "WALK":
            if self.frame_counter > WALK_ANIMATION:
                self.frame_index = (self.frame_index + 1) % len(self.facing_left)
                self.image = self.images[self.frame_index]
                self.frame_counter = 0
            self.frame_counter += 1
    
    def HandleCollisions(self, dx, dy, tiles, world):
        self.is_grounded = False
        game_over = 0
        # TILE COLLISION
        for tile in tiles:
            # Check collision on the X axis first
            if tile[1].colliderect(self.collide_rect.x + dx, self.collide_rect.y, self.collide_rect.w, self.collide_rect.h):
                dx = 0
            # Check collision on the Y axis
            if tile[1].colliderect(self.collide_rect.x , self.collide_rect.y + dy, self.collide_rect.w, self.collide_rect.h):
                if self.velY < 0:
                    dy = tile[1].bottom - self.collide_rect.top
                    self.velY = 0
                elif self.velY >= 0:
                    dy = tile[1].top - self.collide_rect.bottom
                    self.velY = 0
                self.is_grounded = True

        # PORTALS collision
        if pygame.sprite.spritecollide(self, world.portals, False):
            game_over = 1

        # ENEMY collision
        elif pygame.sprite.spritecollide(self, world.snakes, False):
            game_over = -1
            self.deathFX.play()
        
        # MOVING PLATFORMS
        for platform in world.platforms:
            # X axis collision
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # Y axis collision
            if platform.rect.colliderect(self.rect.x , self.rect.y + dy, self.width,  self.height):
                if abs((self.rect.top + dy) - platform.rect.bottom) < 20:
                    self.velY = 0
                    dy = platform.rect.bottom - self.rect.top
                
                elif abs((self.rect.bottom + dy) - platform.rect.top) < 20:
                    self.rect.bottom = platform.rect.top - 1
                    self.collide_rect.bottom = platform.rect.top - 1

                    self.is_grounded = True
                    dy = 0
                
                # Move the player along with the platform x axis
                if platform.mx != 0:
                    self.rect.x += platform.direction
                    self.collide_rect.x += platform.direction
            

        return game_over, dx, dy

    def Initialize(self, x, y):
        self.facing_right = []
        self.facing_left = []

        self.frame_index = 0
        self.frame_counter = 0

        self.deathFX = pygame.mixer.Sound("./assets/audio/death.wav")
        self.deathFX.set_volume(0.4)
        self.jumpFX = pygame.mixer.Sound("./assets/audio/jump1.wav")
        self.jumpFX.set_volume(0.5)

        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        for i in range(1, 5):
            sprite_right = pygame.image.load(f"./assets/images/player{i}.png")
            sprite_left = pygame.transform.flip(sprite_right, 180, 0)
            sprite_right = pygame.transform.scale(sprite_right, (self.width, self.height))
            sprite_left = pygame.transform.scale(sprite_left, (self.width, self.height))
            self.facing_left.append(sprite_left)
            self.facing_right.append(sprite_right)

        self.images = self.facing_right
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # CREATE A RECT CLONE 
        # AS A COLLISION RECT
        self.collide_rect = self.rect.copy()
        self.collide_rect.x = self.collide_rect.x + self.width//4
        self.collide_rect.y = self.collide_rect.y + self.height//4
        self.collide_rect.w = self.width//2
        self.collide_rect.h = self.height//1.3

        self.velY = 0
        self.jumped = False
        self.direction = 0
        self.is_grounded = False
        self.counter = 0

        self.footStepFX = pygame.mixer.Sound("./assets/audio/footstep.wav")
        self.footStepFX.set_volume(0.3)
        self.step_counter_sound = 0
    
    def Render(self,screen):
        screen.blit(self.image, self.rect)
        #DEBUG COLLISION RECT
        # pygame.draw.rect(screen, WHITE, self.collide_rect, 1)

# --- ENEMY COMPONENT ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.facing_right = []
        self.facing_left = []
        for i in range(1, 5):
            sprite_right = pygame.image.load(f'./assets/images/snake{i}.png')
            sprite_left = pygame.transform.flip(sprite_right, 180, 0)
            sprite_left = pygame.transform.scale(sprite_left, (SNAKE_WIDTH, SNAKE_HEIGHT))
            sprite_right = pygame.transform.scale(sprite_right, (SNAKE_WIDTH, SNAKE_HEIGHT))
            self.facing_left.append(sprite_left)
            self.facing_right.append(sprite_right)
        
        self.images = self.facing_right
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y + 10
        self.frame_index  = 0
        self.frame_counter = 0
        self.direction = 1
        self.move_distance = 30
        self.counter = 0
    
    def update(self, screen):
        if self.counter > 8:
            if self.move_distance <= 0:
                self.move_distance = 30
                self.direction *= -1
            self.rect.x += SPEED * self.direction
            self.counter = 0
            self.move_distance -= 1

        if self.direction == -1:
            self.images = self.facing_left
        else:
            self.images = self.facing_right
        self.counter += 1

        if self.frame_counter > SNAKE_ANIMATION:
            self.frame_index += 1
            if  self.frame_index >= 4:
                self.frame_index = 0 
            self.image = self.images[self.frame_index]
            self.frame_counter = 0
        self.frame_counter += 1

        # DEBUG -> SHOW RECT COLLISION
        # pygame.draw.rect(screen, WHITE, self.rect, 1)

# --- WATER COMPONENTS ----
class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite = pygame.image.load('./assets/images/water.png')
        self.image = pygame.transform.scale(sprite, (TILESIZE, TILESIZE//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- COIN COMPONENTS ----
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite = pygame.image.load("./assets/images/coin.png")
        self.image = pygame.transform.scale(sprite, (TILESIZE//2, TILESIZE//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
# --- PORTAL COMPONENT ---
class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite = pygame.image.load("./assets/images/portal.png")
        self.image = pygame.transform.scale(sprite, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- BUTTON ----
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
        self.x = x
        self.y = y
    def update(self):
        action = False
        mouse_position = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return action
    
    def draw(self, screen):
        action = self.update()
        screen.blit(self.image, self.rect)
        return action

# --- MOVING PLATFORM COMPONENT ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        super().__init__()
        image = pygame.image.load("./assets/images/platform.png")
        self.image = pygame.transform.scale(image, (TILESIZE, TILESIZE//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.timer = 0
        self.mx = move_x
        self.my = move_y
    
    def update(self, screen):
        self.rect.x += self.direction * self.mx
        self.rect.y += self.direction * self.my
        self.timer += 1
        if abs(self.timer) > 50:
            self.direction *= -1
            self.timer *= -1
        
        # DEBUG COLLISION RECt
        # pygame.draw.rect(screen, WHITE, [self.rect.x - 1, self.rect.y - 1, self.rect.w + 2, self.rect.h + 2], 1)


# ---- WORLD COMPONENT ---- 
class World:
    def __init__(self, snakes, collectables, platforms, waters, portals ,level_data=None):
        self.data = TEST_LEVEL
        self.snakes = snakes
        self.collectables = collectables
        self.platforms = platforms
        self.waters = waters
        self.portals = portals
        if level_data:
            self.data = level_data
        self.tiles = []
        self.Initialize()
    
    def Initialize(self, *args):
        grass_img = pygame.image.load('./assets/images/tile1.png')
        grass_left_img = pygame.image.load("./assets/images/tilelefttop.png")
        grass_right_img = pygame.image.load("./assets/images/tilerighttop.png")
        tile = pygame.image.load("./assets/images/centertile.png")
        left_border_tile = pygame.image.load("./assets/images/leftitle.png")
        right_border_tile = pygame.image.load("./assets/images/righttile.png")

        # ARGS -> Sprites groups
        x = 0
        for row in self.data:
            y = 0
            for item in row:
                if item == 1:
                    sprite = pygame.transform.scale(tile, (TILESIZE, TILESIZE))
                    sprite_rect = sprite.get_rect()
                    sprite_rect.x = y * TILESIZE
                    sprite_rect.y = x * TILESIZE
                    self.tiles.append([sprite, sprite_rect])
                elif item == 2:
                    sprite = pygame.transform.scale(grass_img, (TILESIZE, TILESIZE))
                    sprite_rect = sprite.get_rect()
                    sprite_rect.x = y * TILESIZE
                    sprite_rect.y = x * TILESIZE
                    self.tiles.append([sprite, sprite_rect])
                elif item == 3:
                    sprite = pygame.transform.scale(grass_left_img, (TILESIZE, TILESIZE))
                    sprite_rect = sprite.get_rect()
                    sprite_rect.x = y * TILESIZE
                    sprite_rect.y = x * TILESIZE
                    self.tiles.append([sprite, sprite_rect])
                elif item == 4:
                    sprite = pygame.transform.scale(grass_right_img, (TILESIZE, TILESIZE))
                    sprite_rect = sprite.get_rect()
                    sprite_rect.x = y * TILESIZE
                    sprite_rect.y = x * TILESIZE
                    self.tiles.append([sprite, sprite_rect])
                elif item == 5:
                    sprite = pygame.transform.scale(right_border_tile, (TILESIZE, TILESIZE))
                    sprite_rect = sprite.get_rect()
                    sprite_rect.x = y * TILESIZE
                    sprite_rect.y = x * TILESIZE
                    self.tiles.append([sprite, sprite_rect])
                elif item == 6:
                    sprite = pygame.transform.scale(left_border_tile, (TILESIZE, TILESIZE))
                    sprite_rect = sprite.get_rect()
                    sprite_rect.x = y * TILESIZE
                    sprite_rect.y = x * TILESIZE
                    self.tiles.append([sprite, sprite_rect])
                elif item == 7:
                    enemy = Enemy( y * TILESIZE, x * TILESIZE)
                    self.snakes.add(enemy)
                elif item == 8:
                    water = Water(y * TILESIZE, x * TILESIZE + TILESIZE//2)
                    self.waters.add(water)
                elif item == 9:
                    portal = Portal(y * TILESIZE, x * TILESIZE)
                    self.portals.add(portal)
                elif item == 10:
                    coin = Coin( y * TILESIZE, x *TILESIZE)
                    self.collectables.add(coin)
                elif item == 11:
                    platform = Platform(y * TILESIZE , x * TILESIZE + TILESIZE//2, 1, 0)
                    self.platforms.add(platform)
                elif item == 12:
                    platform = Platform(y * TILESIZE , x * TILESIZE + TILESIZE//2, 0, 1)
                    self.platforms.add(platform)
                y += 1
            x += 1
    
    def Render(self, screen):
        for tile in self.tiles:
            screen.blit(tile[0], tile[1])
            #DEBUG
            # pygame.draw.rect(screen, WHITE, tile[1], 1)
