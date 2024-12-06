import pygame
import sys
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TILE_SIZE = 50

def main():
    pygame.init()
    pygame.display.set_caption("Heart of Truth")
    width=1200
    height=700
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # 폰트 설정
    font = pygame.font.Font(None, 36)

    # 플레이어 설정
    player_pos = [1, 1]  # 플레이어 시작 위치
    initial_player_pos = player_pos[:]
    player_images = {
        "up": pygame.image.load("1up.png"),
        "down": pygame.image.load("down.png"),
        "left": pygame.image.load("left.png"),
        "right": pygame.image.load("right.png"),
    }
    current_image = player_images["down"]

    #sound = pygame.mixer.Sound
    #sound.play(-1)

    # 0: 움직일수있는 공간 1: 벽(이동x) 2:움직일수있는벽 3: 파괴가능한벽 4:몬스터 5:포탈 6:블록 놓는 위치 7: 사라지는 블럭 8 : 아이템
    level_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    # 움직이는 벽(2)와 파괴 가능한 벽(3) 위치 추적
    movable_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 2]
    destructible_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 3]

    # 아이템 위치를 찾아서 리스트 (x, y) 로 저장
    destructible_items = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 8] 

    # 탈출 위치를 찾아서 리스트 (x, y) 로 저장
    destructible_escape = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 4]

    # 초기 상태 저장
    initial_movable_walls = movable_walls[:]
    initial_destructible_walls = destructible_walls[:]
    initial_level_map = [row[:] for row in level_map]
    initial_destructible_items = destructible_items[:]

    #포탈(5) 위치 저장
    portal_positions = [[x,y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 5]

    #블록(6) 놓는 위치 저장
    target_positions = [[x,y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 6]

    #사라지는 벽(7) 위치 저장
    onoff_positions = [[x,y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 7]

    break_count = 0
    break_limit = 100

    # 타일 이미지 설정
    wall_image = pygame.image.load("1wall.png")
    wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))

    obstacle_image = pygame.image.load("removewall.png")
    obstacle_image = pygame.transform.scale(obstacle_image, (TILE_SIZE, TILE_SIZE))

    movable_wall_image = pygame.image.load("movewall.png")
    movable_wall_image = pygame.transform.scale(movable_wall_image, (TILE_SIZE, TILE_SIZE))

    goal_image = pygame.image.load("end.png")
    goal_image = pygame.transform.scale(goal_image, (TILE_SIZE, TILE_SIZE))

    portal_img = pygame.image.load("portal.png")
    portal_img = pygame.transform.scale(portal_img,(TILE_SIZE,TILE_SIZE))

    targets_img = pygame.image.load("target.png") #블록 놓는 곳
    targets_img = pygame.transform.scale(targets_img,(TILE_SIZE,TILE_SIZE))

    onoffwall_img = pygame.image.load("onoffWall.png")
    onoffwall_img = pygame.transform.scale(onoffwall_img,(TILE_SIZE,TILE_SIZE))

        # 아이템 이미지 로드
    item_image = pygame.image.load("item.png")
    item_image = pygame.transform.scale(item_image, (TILE_SIZE, TILE_SIZE))  # 타일 크기에 맞게 조정

    # 아이템 획득 여부 (기본값: False)
    item_get = False

    # 리셋 버튼 이미지 로드
    reset_btn = pygame.image.load("reset_btn.png")
    reset_btn = pygame.transform.scale(reset_btn, (TILE_SIZE, TILE_SIZE))  # 타일 크기에 맞게 조정


    # 몬스터 이미지 설정
    monster_images = {
        "monster1": pygame.image.load("monster.png"),
        "monster2": pygame.image.load("monster.png"),
        "monster3": pygame.image.load("monster.png")
    }
    # 이미지 크기 조정
    for key in monster_images:
        monster_images[key] = pygame.transform.scale(monster_images[key], (TILE_SIZE, TILE_SIZE))

    # 방향키 설정
    MOVE_KEYS = {
        pygame.K_LEFT: (-1, 0, "left"),
        pygame.K_RIGHT: (1, 0, "right"),
        pygame.K_UP: (0, -1, "up"),
        pygame.K_DOWN: (0, 1, "down")
    }
    
    # 몬스터 설정
    monsters = [
        {
            "current_pos": [0, 0],
            "direction": 1,
            "move_type": "y",
            "image": "monster3",
            "move_delay": 300,  # 이동 속도
            "last_move_time": pygame.time.get_ticks()
        },
        {
            "current_pos": [0, 0],
            "direction": -1,
            "move_type": "x",
            "image": "monster1",
            "move_delay": 500,
            "last_move_time": pygame.time.get_ticks()
        },
        {
            "current_pos": [0, 0],
            "direction": -1,
            "move_type": "y",
            "image": "monster2",
            "move_delay": 700,
            "last_move_time": pygame.time.get_ticks()
        }
    ]

    death_count = 0  # 플레이어 사망 횟수

    offset_y = 50 

    hint_button_rect = pygame.Rect(1050, 10, 80, 40)

    def draw_map():
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    screen.blit(wall_image, rect.topleft)
                elif tile == 3 and [x, y] in destructible_walls:
                    screen.blit(obstacle_image, rect.topleft)
                elif tile == 2 and [x, y] in movable_walls:
                    screen.blit(movable_wall_image, rect.topleft)
                elif tile == 4:
                    screen.blit(goal_image, rect.topleft)
                elif tile == 5:
                    screen.blit(portal_img, rect.topleft)
                elif [x,y] in target_positions:#(6 블럭 놓는 곳)
                    screen.blit(targets_img, rect.topleft)
                elif tile == 7:
                    screen.blit(onoffwall_img, rect.topleft)
                    # 8번 아이템 - 아이템 위치에 아이템 이미지 띄우기
                elif tile == 8 and [x, y] in destructible_items:
                    screen.blit(item_image, rect.topleft)

        # 몬스터 그리기
        for monster in monsters:
            monster_image = monster_images[monster["image"]]
            screen.blit(monster_image, (monster["current_pos"][0] * TILE_SIZE, monster["current_pos"][1] * TILE_SIZE + offset_y))

    def move_monsters():
        current_time = pygame.time.get_ticks()
        for monster in monsters:
            if current_time - monster["last_move_time"] >= monster["move_delay"]:
                current_x, current_y = monster["current_pos"]
                direction = monster["direction"]
                move_type = monster["move_type"]

                # 가로 이동
                if move_type == "x":
                    new_x = current_x + direction

                    if (
                        new_x < 0 or new_x >= len(level_map[0]) or
                        level_map[current_y][new_x] in (1, 2, 3)
                    ):
                        monster["direction"] *= -1 
                        new_x = current_x + monster["direction"]
                        if new_x < 0 or new_x >= len(level_map[0]) or level_map[current_y][new_x] in (1, 2, 3):
                            new_x = current_x
                        else:
                            monster["current_pos"][0] = new_x
                    else:
                        monster["current_pos"][0] = new_x

                # 세로 이동
                elif move_type == "y":
                    new_y = current_y + direction

                    if (
                        new_y < 0 or new_y >= len(level_map) or
                        level_map[new_y][current_x] in (1, 2, 3)
                    ):
                        monster["direction"] *= -1  
                        new_y = current_y + monster["direction"]
                        if new_y < 0 or new_y >= len(level_map) or level_map[new_y][current_x] in (1, 2, 3):
                            new_y = current_y
                        else:
                            monster["current_pos"][1] = new_y
                    else:
                        monster["current_pos"][1] = new_y

                monster["last_move_time"] = current_time  # 몬스터별 마지막 이동 시간 업데이트

    def move_player(dx, dy, direction):
        nonlocal player_pos, current_image, break_count, item_get
        new_x, new_y = player_pos[0] + dx, player_pos[1] + dy

        if 0 <= new_x < len(level_map[0]) and 0 <= new_y < len(level_map):
            # 움직이는 벽 처리 (2)
            if [new_x, new_y] in movable_walls:
                move_x, move_y = new_x + dx, new_y + dy
                if 0 <= move_x < len(level_map[0]) and 0 <= move_y < len(level_map):
                    if level_map[move_y][move_x] == 0 or level_map[move_y][move_x] == 6:  # 밀려날 자리가 비어 있으면
                        movable_walls.remove([new_x, new_y])
                        movable_walls.append([move_x, move_y])
                        level_map[new_y][new_x] = 0
                        level_map[move_y][move_x] = 2
                        player_pos = [new_x, new_y]
                    else:
                        return  # 밀 수 없는 경우 이동 불가
                else:
                    return  # 맵 경계 밖으로 이동 불가

            # 파괴 가능한 벽 처리 (3)
            elif [new_x, new_y] in destructible_walls:
                if break_count < break_limit:
                    destructible_walls.remove([new_x, new_y])
                    level_map[new_y][new_x] = 0
                    break_count += 1
                    player_pos = [new_x, new_y]
                else:
                    return  # 벽 부수기 제한 초과
            
            # 일반 이동
            elif level_map[new_y][new_x] == 0 or level_map[new_y][new_x] == 5 or level_map[new_y][new_x] == 6:
                player_pos = [new_x, new_y]

            # 이동 위치가 아이템 위치라면 True로 바꾸고, 위치 0으로 변경, 플레이어 위치 새로 이동
            elif [new_x, new_y] in destructible_items:
                destructible_items.remove([new_x, new_y])
                item_get = True
                level_map[new_y][new_x] = 0
                player_pos = [new_x, new_y]

            # 탈출 위치 처리 (4)
            # 아이템 획득 여부 판별과 플레이어 위치(탈출 위치)에 따른 맵 자동 이동
            elif level_map[new_y][new_x] == 4 and item_get == True:
                destructible_escape.remove([new_x, new_y])
                level_map[new_y][new_x] = 0
                player_pos = [new_x, new_y]
                os.system('python story1.py')
                pygame.quit()
                sys.exit()

            #target_position에 움직이는 블록이 있다면 맵에 있는 7을 0으로 바꿈
            cnt = 0                
            for [target_x,target_y] in target_positions:
                if level_map[target_y][target_x] == 2: #2는 움직이는 벽 번호
                    cnt +=1
                if cnt == len(target_positions):
                    for [off_x,off_y] in onoff_positions:
                        level_map[off_y][off_x]=0

        current_image = player_images[direction]
            
    def reset_all() :
        nonlocal destructible_items, death_count, item_get, player_pos, current_image, destructible_walls, movable_walls, level_map, break_count
        
        # 데스 카운트 추가
        death_count += 1
        
        # 아이템 획득 유무 초기화 및 이미지 재생성
        item_get = False
        destructible_items = initial_destructible_items

        # 플레이어 위치 초기화
        player_pos = initial_player_pos[:]
        current_image = player_images["down"]

        # 벽 부수기 횟수 초기화
        break_count = 0

        # 맵 초기화
        level_map = [row[:] for row in initial_level_map]

        # 파괴 가능한 벽 초기화
        destructible_walls = initial_destructible_walls[:]

        # 움직이는 벽 초기화
        movable_walls = initial_movable_walls[:]

    def monster_contact():
        nonlocal death_count, player_pos
        for monster in monsters:
            if player_pos == monster["current_pos"]:
                death_count += 1
                print(f"플레이어 사망! 현재 데스 카운트: {death_count}")
                reset_player_and_walls()  # 플레이어 위치와 벽들만 초기화
                break  # 하나의 몬스터와 충돌하면 더 이상 체크하지 않음

    def reset_player_and_walls():
        nonlocal player_pos, current_image, destructible_walls, movable_walls, level_map, break_count

        # 플레이어 위치 초기화
        player_pos = initial_player_pos[:]
        current_image = player_images["down"]

        # 벽 부수기 횟수 초기화
        break_count = 0

        # 맵 초기화
        level_map = [row[:] for row in initial_level_map]

        # 파괴 가능한 벽 초기화
        destructible_walls = initial_destructible_walls[:]

        # 움직이는 벽 초기화
        movable_walls = initial_movable_walls[:]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS:
                    dx, dy, direction = MOVE_KEYS[event.key]
                    move_player(dx, dy, direction)
                if event.key == pygame.K_SPACE:
                    if player_pos in portal_positions:
                        portal_positions_copy = portal_positions.copy()  # 포탈 목록 복사
                        portal_positions_copy.remove(player_pos)  # 현재 위치의 포탈을 제외
                        if portal_positions_copy:
                            player_pos = portal_positions_copy[0] 
            elif event.type == pygame.MOUSEBUTTONDOWN :
                mouse_pos = (pygame.mouse.get_pos())
                if hint_button_rect.collidepoint(event.pos):
                    os.system('python hint1.py')
                if (width - TILE_SIZE <= mouse_pos[0] <= width) and (0 <= mouse_pos[1] <= TILE_SIZE):    
                    reset_all()      

        move_monsters()
        monster_contact() 

        # 화면 업데이트
        screen.fill(WHITE)  # 흰색 배경으로 채우기
        draw_map()

        # 플레이어 그리기 (오프셋 적용)
        screen.blit(current_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE + offset_y))

        # 리셋 버튼 그리기
        screen.blit(reset_btn, [ 1150 , 0 ] )

        # 남은 벽 부수기 횟수와 데스 카운트, 아이템 획득 유무 출력
        info_text = font.render(f"Wall Breaks: {break_limit - break_count} | Death: {death_count}  | Acquire item : {item_get}", True, BLACK)
        screen.blit(info_text, (10, 10))

        # HINT 버튼 
        pygame.draw.rect(screen, WHITE, hint_button_rect)
        hint_text = font.render("HINT", True, BLACK)
        screen.blit(hint_text, hint_button_rect.topleft)

        pygame.display.update() 
        clock.tick(30)

if __name__ == '__main__':
    main()

