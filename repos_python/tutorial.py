import pygame
import sys

pygame.init()

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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

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

# 몬스터 설정
monster_image = pygame.image.load("monster.png")
monster_image = pygame.transform.scale(monster_image, (TILE_SIZE, TILE_SIZE))

# 맵에서 몬스터 초기 위치 찾기
monsters = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 4]

# 맵 그리기
def draw_map():
    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:  # 벽
                pygame.draw.rect(screen, GRAY, rect)
            elif tile == 3 and [x, y] in destructible_walls:  # 파괴 가능한 벽
                screen.blit(obstacle_image, rect.topleft)
            elif tile == 4 and [x, y] in monsters:  # 몬스터
                screen.blit(monster_image, rect.topleft)

# 캐릭터 이동
def move_player(dx, dy, direction):
    global player_pos, current_image, break_count
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < len(level_map[0]) and 0 <= new_y < len(level_map):
        # 벽 충돌 처리
        if [new_x, new_y] in destructible_walls:
            if break_count < break_limit:  # 벽 부수기 제한 확인
                destructible_walls.remove([new_x, new_y])
                break_count += 1
        elif level_map[new_y][new_x] != 1:
            player_pos = [new_x, new_y]
    current_image = player_images[direction]

# 게임 초기화 함수
def reset_game():
    global player_pos, destructible_walls, break_count
    player_pos = initial_player_pos[:]
    destructible_walls = initial_walls[:]
    break_count = 0

# 몬스터 충돌 검사
def monster_contact():
    global death_count
    for monster_pos in monsters:
        if player_pos == monster_pos:  # 플레이어와 몬스터가 같은 위치에 있으면 충돌 발생
            print("플레이어 사망!")
            death_count += 1  
            reset_game()  

# 게임 루프
running = True
death_count = 0  # 죽은 횟수 변수 추가

while running:
    screen.fill(WHITE)
    draw_map()
    screen.blit(current_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

    # 남은 횟수와 죽은 횟수 출력
    font = pygame.font.SysFont(None, 36)
    info_text = font.render(f"Limit: {break_limit - break_count} | Death: {death_count}", True, (0, 0, 0))
    text_rect = info_text.get_rect(center=(screen_width // 2, screen_height - 20))
    screen.blit(info_text, text_rect)

    monster_contact()  # 몬스터와 플레이어의 충돌 검사

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in MOVE_KEYS:
                dx, dy, direction = MOVE_KEYS[event.key]
                move_player(dx, dy, direction)  

    pygame.display.flip()

pygame.quit()