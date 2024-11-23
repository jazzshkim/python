import pygame
import sys
import time

pygame.init()

# 색상 설정
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# 화면 설정
screen_width = 1200
screen_height = 700
TILE_SIZE = 50
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Heart of Truth")

# 플레이어 초기 설정
initial_player_pos = [4, 2]
player_pos = initial_player_pos[:]
player_images = {
    "up": pygame.image.load("up.png"),
    "down": pygame.image.load("down.png"),
    "left": pygame.image.load("left.png"),
    "right": pygame.image.load("right.png"),
}
current_image = player_images["down"]

# 타일 맵 정의 (0: 빈 칸, 1: 벽, 3: 파괴 가능한 벽)
level_map = [
#x축 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 0
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 1
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 2
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 3
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 4
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 5
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 6
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 7
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 8
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 9
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 10
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 11
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 12
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # 13 
]                                                                             # y축

# 몬스터 설정
monster_image = pygame.image.load("monster.png")
monster_image = pygame.transform.scale(monster_image, (TILE_SIZE, TILE_SIZE))

# 시작 위치, 초기 방향, 이동 축
monsters = [
    {"current_pos": [16, 2], "direction": 1, "move_type": "y"},  # y축 이동
    {"current_pos": [18, 8], "direction": -1, "move_type": "x"}, # x축 이동
    {"current_pos": [4, 4], "direction": -1, "move_type": "y"} 
]
monster_move_delay = 500  # 몬스터 이동 간격 (밀리초)
last_monster_move_time = pygame.time.get_ticks()

# 파괴 가능한 벽 설정
obstacle_image = pygame.image.load("obstacle.png")
obstacle_image = pygame.transform.scale(obstacle_image, (TILE_SIZE, TILE_SIZE))
initial_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 3]
destructible_walls = initial_walls[:]
break_count = 0
break_limit = 5

# 방향키 설정
MOVE_KEYS = {
    pygame.K_LEFT: (-1, 0, "left"),
    pygame.K_RIGHT: (1, 0, "right"),
    pygame.K_UP: (0, -1, "up"),
    pygame.K_DOWN: (0, 1, "down")
}

# 변수 초기화
death_count = 0

# 맵 그리기
def draw_map():
    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:
                pygame.draw.rect(screen, GRAY, rect)
            elif tile == 3 and [x, y] in destructible_walls:
                screen.blit(obstacle_image, rect.topleft)
    for monster in monsters:
        screen.blit(monster_image, (monster["current_pos"][0] * TILE_SIZE, monster["current_pos"][1] * TILE_SIZE))

# 몬스터 이동
def move_monsters():
    global last_monster_move_time
    current_time = pygame.time.get_ticks()

    if current_time - last_monster_move_time >= monster_move_delay:
        for monster in monsters:
            current_x, current_y = monster["current_pos"]
            direction = monster["direction"]
            move_type = monster["move_type"]

            # 가로 이동
            if move_type == "x":
                new_x = current_x + direction

                # 경계 또는 회색 벽(1)에 닿으면 방향 전환
                if new_x < 0 or new_x >= len(level_map[0]) or level_map[current_y][new_x] == 1:
                    monster["direction"] *= -1 
                    new_x = current_x + monster["direction"]

                monster["current_pos"][0] = new_x

            # 세로 이동
            elif move_type == "y":
                new_y = current_y + direction

                if new_y < 0 or new_y >= len(level_map) or level_map[new_y][current_x] == 1:
                    monster["direction"] *= -1  
                    new_y = current_y + monster["direction"]

                monster["current_pos"][1] = new_y

        last_monster_move_time = current_time

# 플레이어 이동
def move_player(dx, dy, direction):
    global player_pos, current_image, break_count
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < len(level_map[0]) and 0 <= new_y < len(level_map):
        if [new_x, new_y] in destructible_walls:
            if break_count < break_limit:
                destructible_walls.remove([new_x, new_y])
                break_count += 1
        elif level_map[new_y][new_x] != 1:
            player_pos = [new_x, new_y]
    current_image = player_images[direction]

# 몬스터 충돌 검사
def monster_contact():
    global death_count, player_pos
    for monster in monsters:
        if player_pos == monster["current_pos"]:
            death_count += 1
            print(f"플레이어 사망! 현재 데스 카운트: {death_count}")
            reset_game()

# 게임 초기화
def reset_game():
    global player_pos, destructible_walls, break_count
    player_pos = initial_player_pos[:]
    destructible_walls = initial_walls[:]
    break_count = 0

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    draw_map()
    screen.blit(current_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

    # 남은 횟수와 데스 카운트 표시
    font = pygame.font.SysFont(None, 36)
    info_text = font.render(f"Limit: {break_limit - break_count} | Death: {death_count}", True, (0, 0, 0))
    text_rect = info_text.get_rect(center=(screen_width // 2, screen_height - 20))
    screen.blit(info_text, text_rect)

    move_monsters()
    monster_contact()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in MOVE_KEYS:
                dx, dy, direction = MOVE_KEYS[event.key]
                move_player(dx, dy, direction)

    pygame.display.flip()
    clock.tick(30)  

pygame.quit()