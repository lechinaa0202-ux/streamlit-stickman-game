
import math
import random
import pygame

pygame.init()

WIDTH, HEIGHT = 960, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman vs Zombies")
clock = pygame.time.Clock()

WHITE = (240, 245, 245)
GREEN = (130, 220, 95)
RED = (220, 55, 65)
DARK = (18, 30, 38)
font = pygame.font.SysFont("arial", 22, bold=True)
small_font = pygame.font.SysFont("arial", 15, bold=True)

player = {
    "x": WIDTH / 2, "y": HEIGHT / 2,
    "hp": 100, "speed": 230, "face": [1, 0],
    "attack": 0, "cooldown": 0, "invincible": 0
}

zombies = []
particles = []
score = 0
game_over = False


def spawn_zombie():
    side = random.randrange(4)

    if side == 0:
        x, y = random.randint(20, WIDTH - 20), 100
    elif side == 1:
        x, y = WIDTH - 25, random.randint(100, HEIGHT - 20)
    elif side == 2:
        x, y = random.randint(20, WIDTH - 20), HEIGHT - 25
    else:
        x, y = 25, random.randint(100, HEIGHT - 20)

    hp = 60 + min(score, 20) * 2

    zombies.append({
        "x": float(x), "y": float(y),
        "hp": hp, "max_hp": hp,
        "speed": random.uniform(45, 65),
        "flash": 0, "cooldown": random.random()
    })


def draw_text(text, x, y, color=WHITE, font_obj=font):
    image = font_obj.render(str(text), True, color)
    screen.blit(image, (x, y))


def draw_bar(x, y, width, height, hp, max_hp, color):
    pygame.draw.rect(screen, (45, 52, 58),
                     (x, y, width, height), border_radius=4)
    ratio = max(0, min(1, hp / max_hp))
    if ratio > 0:
        pygame.draw.rect(
            screen, color,
            (x, y, int(width * ratio), height),
            border_radius=4
        )


def create_blood(x, y, fx, fy):
    for _ in range(14):
        angle = math.atan2(fy, fx) + random.uniform(-1.3, 1.3)
        speed = random.uniform(50, 190)

        particles.append({
            "x": float(x), "y": float(y),
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed - 30,
            "life": random.uniform(0.25, 0.6)
        })


def attack():
    global score

    if player["cooldown"] > 0 or game_over:
        return

    player["attack"] = 0.25
    player["cooldown"] = 0.42

    fx, fy = player["face"]

    for zombie in zombies[:]:
        dx = zombie["x"] - player["x"]
        dy = zombie["y"] - player["y"]
        distance = math.hypot(dx, dy)

        if distance < 75:
            direction = (dx * fx + dy * fy) / max(distance, 1)

            if direction > -0.25:
                zombie["hp"] -= 35
                zombie["flash"] = 0.15

                create_blood(
                    zombie["x"], zombie["y"], fx, fy
                )

                zombie["x"] += fx * 10
                zombie["y"] += fy * 10

                if zombie["hp"] <= 0:
                    zombies.remove(zombie)
                    score += 1


def draw_stickman(x, y, facing, walk=0):
    fx, fy = facing
    swing = math.sin(walk) * 7

    # Bóng dưới chân
    pygame.draw.ellipse(
        screen, (12, 20, 22),
        (x - 20, y + 15, 40, 10)
    )

    # Chân
    pygame.draw.line(
        screen, WHITE, (x - 3, y + 3),
        (x - 7 + swing, y + 15), 5
    )
    pygame.draw.line(
        screen, WHITE, (x - 7 + swing, y + 15),
        (x - 12 + swing, y + 22), 4
    )
    pygame.draw.line(
        screen, WHITE, (x + 3, y + 3),
        (x + 7 - swing, y + 15), 5
    )
    pygame.draw.line(
        screen, WHITE, (x + 7 - swing, y + 15),
        (x + 12 - swing, y + 22), 4
    )

    # Thân và đầu
    pygame.draw.line(
        screen, WHITE, (x, y - 7), (x, y + 7), 5
    )
    pygame.draw.circle(screen, WHITE, (int(x), int(y - 15)), 8)

    # Mắt hướng di chuyển
    pygame.draw.circle(
        screen, DARK,
        (int(x + fx * 3), int(y - 16 + fy)), 2
    )

    # Tay trái
    pygame.draw.line(
        screen, WHITE, (x, y - 5),
        (x - 9, y + 1), 4
    )

    # Tay cầm kiếm
    hand_x = x + fx * 10
    hand_y = y - 3 + fy * 5

    pygame.draw.line(
        screen, WHITE, (x, y - 5),
        (hand_x, hand_y), 5
    )

    angle = math.atan2(fy, fx)

    if player["attack"] > 0:
        angle -= math.sin(
            (0.25 - player["attack"]) / 0.25 * math.pi
        ) * 1.5

    # Kiếm
    end_x = hand_x + math.cos(angle) * 27
    end_y = hand_y + math.sin(angle) * 27

    pygame.draw.line(
        screen, (140, 100, 60),
        (hand_x, hand_y),
        (hand_x + fx * 8, hand_y + fy * 8), 5
    )

    pygame.draw.line(
        screen, (220, 235, 245),
        (hand_x, hand_y), (end_x, end_y), 4
    )

    pygame.draw.circle(
        screen, (245, 250, 255),
        (int(end_x), int(end_y)), 3
    )


def draw_zombie(zombie, walk):
    x, y = int(zombie["x"]), int(zombie["y"])
    skin = (255, 155, 145) if zombie["flash"] > 0 else (125, 155, 105)
    shirt = (145, 65, 65) if zombie["flash"] > 0 else (65, 85, 65)

    pygame.draw.ellipse(
        screen, (12, 20, 22), (x - 19, y + 15, 38, 9)
    )

    swing = math.sin(walk) * 5

    # Chân
    pygame.draw.line(
        screen, shirt, (x - 4, y + 4),
        (x - 8 + swing, y + 15), 6
    )
    pygame.draw.line(
        screen, skin, (x - 8 + swing, y + 15),
        (x - 12 + swing, y + 21), 4
    )
    pygame.draw.line(
        screen, shirt, (x + 4, y + 4),
        (x + 8 - swing, y + 15), 6
    )
    pygame.draw.line(
        screen, skin, (x + 8 - swing, y + 15),
        (x + 12 - swing, y + 21), 4
    )

    # Thân rách
    pygame.draw.polygon(screen, shirt, [
        (x - 9, y - 8), (x + 8, y - 8),
        (x + 10, y + 7), (x + 3, y + 10),
        (x - 10, y + 7)
    ])

    # Tay zombie vươn ra
    pygame.draw.line(
        screen, shirt, (x - 6, y - 5),
        (x - 14, y), 5
    )
    pygame.draw.line(
        screen, skin, (x - 14, y),
        (x - 17, y + 6), 4
    )
    pygame.draw.line(
        screen, shirt, (x + 6, y - 5),
        (x + 14, y), 5
    )
    pygame.draw.line(
        screen, skin, (x + 14, y),
        (x + 17, y + 6), 4
    )

    # Đầu và tóc rối
    pygame.draw.line(
        screen, skin, (x, y - 8), (x, y - 12), 5
    )
    pygame.draw.circle(screen, skin, (x, y - 17), 9)
    pygame.draw.polygon(screen, (38, 52, 39), [
        (x - 8, y - 18), (x - 10, y - 25),
        (x - 4, y - 22), (x, y - 27),
        (x + 4, y - 22), (x + 9, y - 25),
        (x + 8, y - 17)
    ])

    # Mắt phát sáng
    pygame.draw.circle(
        screen, (220, 255, 120), (x - 3, y - 18), 2
    )
    pygame.draw.circle(
        screen, (220, 255, 120), (x + 3, y - 18), 2
    )
    pygame.draw.line(
        screen, (45, 30, 30),
        (x - 4, y - 12), (x + 4, y - 12), 2
    )

    # Thanh máu trên đầu zombie
    draw_bar(
        x - 21, y - 39, 42, 6,
        zombie["hp"], zombie["max_hp"],
        GREEN if zombie["hp"] > zombie["max_hp"] * .4 else RED
    )


def draw_background():
    screen.fill((23, 40, 48))

    for x in range(0, WIDTH, 55):
        height = 35 + int(abs(math.sin(x * 0.04)) * 45)
        pygame.draw.rect(
            screen, (15, 28, 36),
            (x, 90 - height, 35, height)
        )

    pygame.draw.rect(
        screen, (39, 57, 51),
        (0, 90, WIDTH, HEIGHT - 90)
    )

    for x in range(0, WIDTH, 48):
        pygame.draw.line(
            screen, (45, 64, 57), (x, 90), (x, HEIGHT)
        )

    for y in range(110, HEIGHT, 48):
        pygame.draw.line(
            screen, (45, 64, 57), (0, y), (WIDTH, y)
        )


def draw_controls():
    # Hướng dẫn bàn phím
    draw_text(
        "WASD / Mui ten: di chuyen | SPACE: chem",
        12, HEIGHT - 25, (220, 230, 230), small_font
    )


def update(dt):
    global game_over

    keys = pygame.key.get_pressed()

    if game_over:
        return

    dx = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(
        keys[pygame.K_a] or keys[pygame.K_LEFT]
    )
    dy = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(
        keys[pygame.K_w] or keys[pygame.K_UP]
    )

    length = math.hypot(dx, dy)

    if length:
        dx, dy = dx / length, dy / length
        player["face"] = [dx, dy]
        player["x"] += dx * player["speed"] * dt
        player["y"] += dy * player["speed"] * dt

    player["x"] = max(18, min(WIDTH - 18, player["x"]))
    player["y"] = max(100, min(HEIGHT - 25, player["y"]))

    player["attack"] = max(0, player["attack"] - dt)
    player["cooldown"] = max(0, player["cooldown"] - dt)
    player["invincible"] = max(0, player["invincible"] - dt)

    for z in zombies[:]:
        z["flash"] = max(0, z["flash"] - dt)
        z["cooldown"] -= dt

        dx = player["x"] - z["x"]
        dy = player["y"] - z["y"]
        distance = math.hypot(dx, dy) or 1

        fx, fy = dx / distance, dy / distance

        if distance > 31:
            z["x"] += fx * z["speed"] * dt
            z["y"] += fy * z["speed"] * dt

        if distance < 37 and z["cooldown"] <= 0:
            z["cooldown"] = 1.0

            if player["invincible"] <= 0:
                player["hp"] = max(0, player["hp"] - 10)
                player["invincible"] = .7

                if player["hp"] <= 0:
                    game_over = True

    for particle in particles[:]:
        particle["life"] -= dt
        particle["vy"] += 260 * dt
        particle["x"] += particle["vx"] * dt
        particle["y"] += particle["vy"] * dt

        if particle["life"] <= 0:
            particles.remove(particle)


def draw():
    draw_background()

    # Vẽ nhân vật theo thứ tự chiều sâu
    actors = [(p["y"], "player", p)]
    actors += [(z["y"], "zombie", z) for z in zombies]
    actors.sort(key=lambda a: a[0])

    for _, kind, obj in actors:
        if kind == "player":
            draw_stickman(
                obj["x"], obj["y"], obj["face"], pygame.time.get_ticks() / 100
            )
        else:
            draw_zombie(obj, pygame.time.get_ticks() / 130)

    for particle in particles:
        pygame.draw.circle(
            screen, (210, 48, 57),
            (int(particle["x"]), int(particle["y"])),
            max(1, int(particle["life"] * 5))
        )

    draw_text("STICKMAN VS ZOMBIES", 15, 12, GREEN)
    draw_text(f"HP: {player['hp']}/100", 15, 42)
    draw_bar(15, 70, 170, 12, player["hp"], 100, GREEN)
    draw_text(f"Zombie da ha: {score}", WIDTH - 210, 15)

    if game_over:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 190))
        screen.blit(shade, (0, 0))
        title = font.render("BAN DA THUA!", True, RED)
        subtitle = font.render("Nhan R de choi lai", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH/2, HEIGHT/2 - 20)))
        screen.blit(subtitle, subtitle.get_rect(center=(WIDTH/2, HEIGHT/2 + 20)))


spawn_zombie()
spawn_zombie()
spawn_zombie()

running = True

while running:
    dt = min(clock.tick(60) / 1000, .035)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                attack()

            if event.key == pygame.K_r and game_over:
                player.update({
                    "x": WIDTH / 2, "y": HEIGHT / 2,
                    "hp": 100, "face": [1, 0],
                    "attack": 0, "cooldown": 0,
                    "invincible": 0
                })
                zombies.clear()
                particles.clear()
                score = 0
                game_over = False

                for _ in range(3):
                    spawn_zombie()

    update(dt)

    if not game_over and len(zombies) < min(12, 3 + score // 2):
        if random.random() < .012:
            spawn_zombie()

    draw()
    pygame.display.flip()

pygame.quit()
