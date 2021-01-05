import pygame
import os
import time
import random
from gui.sound import Sound
from enemies.space_invader_red import SpaceInvaderRed
from enemies.space_invader_green import SpaceInvaderGreen
from enemies.space_invader_blue import SpaceInvaderBlue
from enemies.player import Player
from enemies.mystery_ship import MysteryShip
from items.ship import Ship
from items.laser import Laser, collide
from config.config import WIDTH, HEIGHT, BUNKER, BUNKER2, GARAGE
from items.bunker import Bunker
import gui.inputBox as inputUser
from states.states import Save

# Mystery ship -
pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
BG = pygame.transform.scale(pygame.image.load("./assets/background-black.png"), (WIDTH, HEIGHT))
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)

MAIN_FONT = pygame.font.SysFont("comicsans", 50)
LOST_FONT = pygame.font.SysFont("comicsans", 60)
font = pygame.font.SysFont(None, 40, "Monaco")


def draw_text(line, line_num, c_let, wr_letters, f_line=(50, 100)):
    line_space = 30
    w_text = line[c_let: c_let + wr_letters]
    n_text = line[c_let + wr_letters:]
    c_text = line[:c_let]

    w_text = w_text.replace(" ", chr(9209))

    wrong_text = font.render(w_text, True, RED_COLOR)
    normal_text = font.render(n_text, True, BLACK_COLOR)
    correct_text = font.render(c_text, True, GREEN_COLOR)

    wrong_rect = wrong_text.get_rect()
    normal_rect = normal_text.get_rect()
    correct_rect = correct_text.get_rect()
    correct_rect.topleft = \
        (f_line[0], f_line[1] + line_space * line_num)
    if c_let == 0:
        correct_rect.size = (0, 0)
    wrong_rect.left, wrong_rect.top = correct_rect.right, correct_rect.top
    if wr_letters == 0:
        wrong_rect.size = (0, 0)
    normal_rect.left, normal_rect.top = wrong_rect.right, wrong_rect.top
    WIN.blit(correct_text, correct_rect)
    WIN.blit(wrong_text, wrong_rect)
    WIN.blit(normal_text, normal_rect)


def get_high_score(file, user):
    WIN.fill(WHITE_COLOR)
    w_space = 2
    list_tuple = list(file.get_items())
    list_tuple.sort(key=lambda jojo: jojo[1])
    list_tuple.reverse()
    draw_name = "%d.%s"
    s = "Highscore table (nickname -- points):"
    draw_text(s, 0, 0, 0)
    points_tuple = (470, 100)
    draw_text("Name", 2, 0, 0)
    draw_text("Points", 2, 0, 0, points_tuple)
    for j, i in enumerate(list_tuple[:11]):
        if user == i[0]:
            if j > 8:
                w_space = 3
            temp = len(i[0]) + len(str(j)) + w_space - 1
            draw_text(draw_name % (j + 1, i[0]), j + 4, temp, 0)
            draw_text("%.2f" % (i[1]), j + 4, 0, 0, points_tuple)
        else:
            draw_text(draw_name % (j + 1, i[0]), j + 4, 0, 0)
            draw_text("%.2f" % (i[1]), j + 4, 0, 0, points_tuple)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE \
                    or event.type == pygame.QUIT:
                pygame.quit()
                quit()


def get_rand_x_y(player):
    x = random.randint(100, 500)
    y = random.randint(100, 500)
    if player.x - 90 <= x <= player.x + 90 and player.y - 90 <= y <= player.y + 90:
        x, y = get_rand_x_y(player)
    return x, y


def check_collision(bunkers, player):
    return any([1 for b in bunkers if collide(player, b)])


def main():
    sound = Sound()
    sound.spaceinvaders1.play()
    k_loud = 1
    run = True
    FPS = 60
    level = 0
    player = Player(300, 630)
    enemies = []
    wave_length = 5
    bunkers = []
    player_vel = player.velocity
    clock = pygame.time.Clock()
    color_to_enemy = {
        "mystery": MysteryShip,
        "red": SpaceInvaderRed,
        "blue": SpaceInvaderBlue,
        "green": SpaceInvaderGreen
    }
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_label = MAIN_FONT.render(f"Lives: {player.lives}", 1, WHITE_COLOR)
        level_label = MAIN_FONT.render(f"Level: {level}", 1, WHITE_COLOR)
        score_label = MAIN_FONT.render(f"Score: {player.score}", 1, WHITE_COLOR)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(score_label, (10, 60))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for current_enemy in enemies:
            current_enemy.draw(WIN)
        for bunker in bunkers:
            bunker.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = LOST_FONT.render("You lost", 1, WHITE_COLOR)
            WIN.blit(lost_label, (int(WIDTH / 2 - lost_label.get_width() / 2), 350))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if player.lives <= 0 or player.health <= 0:
            lost = True
            player.health = 0
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if not enemies:
            level += 1
            if level % 3 == 0:
                enemies.append(color_to_enemy["mystery"](100, 100))
                player.health = 100
                player.armor = 100
            else:
                if player.health <= 50:
                    player.health += 50
                if player.armor <= 50:
                    player.armor += 30
                wave_length += 10
                x, y = get_rand_x_y(player)
                bunkers.append(Bunker(x, y, BUNKER2))
                for i in range(wave_length):
                    rnd_x = random.randrange(50, WIDTH - 100)
                    rnd_y = random.randrange(-1500, -100)
                    rnd_color = random.choice(["red", "blue", "green"])
                    enemy = color_to_enemy[rnd_color](rnd_x, rnd_y)
                    enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    sound.spaceinvaders1.stop()
                elif event.key == pygame.K_2:
                    k_loud -= 0.25
                    if k_loud <= 0:
                        k_loud = 0
                elif event.key == pygame.K_3:
                    k_loud = 1
        sound.spaceinvaders1.set_volume(k_loud)
        sound.shoot.set_volume(k_loud)
        sound.explosion.set_volume(k_loud)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
            if check_collision(bunkers, player):
                player.x += player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
            if check_collision(bunkers, player):
                player.x -= player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
            if check_collision(bunkers, player):
                player.y += player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
            if check_collision(bunkers, player):
                player.y -= player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_LSHIFT]:
            player.overpower_shoot()

        enemy_to_delete = []

        for enemy in enemies[:]:
            enemy.move(enemy.velocity)
            enemy.move_lasers(Laser.velocity, player, bunkers)
            if enemy.y >= HEIGHT or enemy.health <= 0:
                # enemy_to_delete.append(enemy)
                enemies.remove(enemy)
                continue
            if isinstance(enemy, MysteryShip):
                if random.randrange(0, 15 / level) == 1:
                    enemy.shoot()
            if random.randrange(0, 100) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 50
                sound.explosion.play()
                enemies.remove(enemy)
                # enemy_to_delete.append(enemy)
                continue
            elif player.health <= 0:
                player.lives -= 1
                player.health = 100
            for b in bunkers:
                if collide(enemy, b):
                    if isinstance(enemy, MysteryShip):
                        b.remove(b)
                        continue
                    b.health -= 50
                    enemies.remove(enemy)
                if b.health <= 0:
                    bunkers.remove(b)
        # enemies = [x for x in enemies if x not in enemy_to_delete]
        player.move_lasers(-Laser.velocity, enemies, bunkers)
    return player.score


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press any key to begin..", 1, WHITE_COLOR)
        WIN.blit(title_label, (int(WIDTH / 2 - title_label.get_width() / 2), 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                return main()


def load(username, file):
    return file.get(username)


def save_state(curr_user, points, file):
    file.add(curr_user, points)


def main_input():
    inputUser.inputString = "Write your nickname"
    curr_user = inputUser.main()
    if not curr_user:
        return

    file = Save('./states/data')
    if curr_user not in file.get_keys():
        save_state(curr_user, 0, file)
    points = load(curr_user, file)
    curr_points = main_menu()
    if curr_points > points:
        points = curr_points
    save_state(curr_user, points, file)
    get_high_score(file, curr_user)
    pygame.init()


if __name__ == "__main__":
    main_input()
