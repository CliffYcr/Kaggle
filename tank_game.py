import pygame
import math
import random
import sys

# 初始化 Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 128, 0)
BROWN = (139, 69, 19)

class Tank:
    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 3
        self.size = 20
        self.color = color
        self.health = 100
        self.max_health = 100
        self.controls = controls
        self.bullets = []
        self.last_shot = 0
        self.shot_cooldown = 500  # 毫秒
        
    def update(self, keys):
        # 移动控制
        old_x, old_y = self.x, self.y
        
        if keys[self.controls['up']]:
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed
        if keys[self.controls['down']]:
            self.x -= math.cos(math.radians(self.angle)) * self.speed
            self.y -= math.sin(math.radians(self.angle)) * self.speed
        if keys[self.controls['left']]:
            self.angle -= 3
        if keys[self.controls['right']]:
            self.angle += 3
            
        # 边界检测
        if self.x < self.size or self.x > SCREEN_WIDTH - self.size:
            self.x = old_x
        if self.y < self.size or self.y > SCREEN_HEIGHT - self.size:
            self.y = old_y
            
        # 射击
        current_time = pygame.time.get_ticks()
        if keys[self.controls['shoot']] and current_time - self.last_shot > self.shot_cooldown:
            self.shoot()
            self.last_shot = current_time
            
        # 更新子弹
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                
    def shoot(self):
        bullet_x = self.x + math.cos(math.radians(self.angle)) * self.size
        bullet_y = self.y + math.sin(math.radians(self.angle)) * self.size
        self.bullets.append(Bullet(bullet_x, bullet_y, self.angle))
        
    def draw(self, screen):
        # 绘制坦克主体
        tank_points = []
        for angle_offset in [-135, -45, 45, 135]:
            point_angle = math.radians(self.angle + angle_offset)
            point_x = self.x + math.cos(point_angle) * self.size * 0.7
            point_y = self.y + math.sin(point_angle) * self.size * 0.7
            tank_points.append((point_x, point_y))
        pygame.draw.polygon(screen, self.color, tank_points)
        
        # 绘制炮筒
        cannon_length = self.size * 1.5
        cannon_end_x = self.x + math.cos(math.radians(self.angle)) * cannon_length
        cannon_end_y = self.y + math.sin(math.radians(self.angle)) * cannon_length
        pygame.draw.line(screen, self.color, (self.x, self.y), (cannon_end_x, cannon_end_y), 5)
        
        # 绘制生命值条
        bar_width = 40
        bar_height = 6
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size - 15
        
        # 背景条
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        # 生命值条
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw(screen)
            
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 8
        self.size = 3
        
    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.size)
        
    def is_off_screen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or 
                self.y < 0 or self.y > SCREEN_HEIGHT)
                
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("坦克大战")
        self.clock = pygame.time.Clock()
        
        # 创建玩家坦克
        player1_controls = {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d,
            'shoot': pygame.K_SPACE
        }
        
        player2_controls = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'shoot': pygame.K_RETURN
        }
        
        self.player1 = Tank(150, 150, BLUE, player1_controls)
        self.player2 = Tank(650, 450, RED, player2_controls)
        
        # 创建墙壁
        self.walls = [
            Wall(200, 200, 100, 20),
            Wall(500, 300, 20, 100),
            Wall(300, 400, 150, 20),
            Wall(600, 150, 20, 80),
            Wall(100, 350, 80, 20),
            Wall(400, 100, 20, 120),
        ]
        
        self.running = True
        self.winner = None
        
    def handle_collisions(self):
        # 子弹与坦克的碰撞
        for bullet in self.player1.bullets[:]:
            bullet_rect = bullet.get_rect()
            if bullet_rect.colliderect(self.player2.get_rect()):
                self.player1.bullets.remove(bullet)
                if self.player2.take_damage(25):
                    self.winner = "玩家1获胜！"
                    
        for bullet in self.player2.bullets[:]:
            bullet_rect = bullet.get_rect()
            if bullet_rect.colliderect(self.player1.get_rect()):
                self.player2.bullets.remove(bullet)
                if self.player1.take_damage(25):
                    self.winner = "玩家2获胜！"
                    
        # 子弹与墙壁的碰撞
        for wall in self.walls:
            for bullet in self.player1.bullets[:]:
                if bullet.get_rect().colliderect(wall.rect):
                    self.player1.bullets.remove(bullet)
            for bullet in self.player2.bullets[:]:
                if bullet.get_rect().colliderect(wall.rect):
                    self.player2.bullets.remove(bullet)
                    
        # 坦克与墙壁的碰撞
        for wall in self.walls:
            if self.player1.get_rect().colliderect(wall.rect):
                # 简单的推回机制
                self.player1.x += random.choice([-5, 5])
                self.player1.y += random.choice([-5, 5])
            if self.player2.get_rect().colliderect(wall.rect):
                self.player2.x += random.choice([-5, 5])
                self.player2.y += random.choice([-5, 5])
                
    def draw_ui(self):
        # 绘制控制说明
        font = pygame.font.Font(None, 24)
        
        # 玩家1控制说明
        text1 = font.render("玩家1: WASD移动, 空格射击", True, WHITE)
        self.screen.blit(text1, (10, 10))
        
        # 玩家2控制说明
        text2 = font.render("玩家2: 方向键移动, 回车射击", True, WHITE)
        self.screen.blit(text2, (10, 35))
        
        # 生命值显示
        health1_text = font.render(f"玩家1生命值: {self.player1.health}", True, BLUE)
        health2_text = font.render(f"玩家2生命值: {self.player2.health}", True, RED)
        self.screen.blit(health1_text, (10, 70))
        self.screen.blit(health2_text, (10, 95))
        
        # 获胜信息
        if self.winner:
            win_font = pygame.font.Font(None, 48)
            win_text = win_font.render(self.winner, True, YELLOW)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            pygame.draw.rect(self.screen, BLACK, text_rect.inflate(20, 10))
            self.screen.blit(win_text, text_rect)
            
            restart_text = font.render("按R重新开始，按ESC退出", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            self.screen.blit(restart_text, restart_rect)
        
    def restart_game(self):
        self.player1 = Tank(150, 150, BLUE, self.player1.controls)
        self.player2 = Tank(650, 450, RED, self.player2.controls)
        self.winner = None
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r and self.winner:
                        self.restart_game()
                        
            if not self.winner:
                keys = pygame.key.get_pressed()
                self.player1.update(keys)
                self.player2.update(keys)
                self.handle_collisions()
            
            # 绘制
            self.screen.fill(DARK_GREEN)
            
            # 绘制墙壁
            for wall in self.walls:
                wall.draw(self.screen)
                
            # 绘制坦克
            if not self.winner:
                self.player1.draw(self.screen)
                self.player2.draw(self.screen)
            
            # 绘制UI
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()