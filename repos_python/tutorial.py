import pygame
import sys

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 1280, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("튜토리얼")

# 색상 및 속성 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
character_step = 50  # 이동할 거리 (한 칸)

# 게임 영역 설정
game_area_x, game_area_width = 90, screen_width - 180
game_area_y, game_area_height = 100, screen_height - 200

# 캐릭터 설정
character_image = pygame.image.load("character1.png")
character_image = pygame.transform.scale(character_image, (50, 50))
character_pos = pygame.Vector2(game_area_x, screen_height - character_image.get_height() - 100) # 지피티를 이용하여 캐릭터 위치 설정

# 파괴 가능한 벽 설정
obstacle_image = pygame.image.load("obstacle.png")
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))
destructible_walls = [pygame.Rect(game_area_x + i * 50, 450, 50, 50) for i in range(game_area_width // 50)] # 지피티 사용하여 벽 일렬로 생성

# 끝 지점 설정
end_point = pygame.Rect(screen_width - 140, 100, 50, 50)

# 게임 루프
while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # 방향 키 입력에 따라 이동
            movement = pygame.Vector2(0, 0)
            if event.key == pygame.K_LEFT and character_pos.x > game_area_x:
                movement.x = -character_step
            elif event.key == pygame.K_RIGHT and character_pos.x < game_area_x + game_area_width - character_image.get_width():
                movement.x = character_step
            elif event.key == pygame.K_UP and character_pos.y > game_area_y:
                movement.y = -character_step
            elif event.key == pygame.K_DOWN and character_pos.y < game_area_y + game_area_height - character_image.get_height():
                movement.y = character_step

            # 이동할 위치로 캐릭터를 옮긴 후 충돌 체크
            new_pos = character_pos + movement
            character_rect = pygame.Rect(new_pos.x, new_pos.y, 50, 50)
            collided_wall = next((wall for wall in destructible_walls if character_rect.colliderect(wall)), None)

            # 부딪힌 벽이 있으면 삭제, 아니면 이동
            if collided_wall:
                destructible_walls.remove(collided_wall)
            else:
                character_pos = new_pos

            # 끝 지점 도착 시 종료
            if character_rect.colliderect(end_point):
                print("게임 클리어!")
                running = False

    # 화면 그리기
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (game_area_x, 0, game_area_width, 100))  # 위쪽 검은 벽
    pygame.draw.rect(screen, BLACK, (game_area_x, screen_height - 100, game_area_width, 100))  # 아래쪽 검은 벽
    pygame.draw.rect(screen, WHITE, (game_area_x, game_area_y, game_area_width, game_area_height))  # 중앙 흰색 영역

    # 파괴 가능한 벽 그리기
    for wall in destructible_walls:
        screen.blit(obstacle_image, (wall.x, wall.y))

    # 끝 지점 그리기
    pygame.draw.rect(screen, (0, 255, 0), end_point)

    # 캐릭터 그리기
    screen.blit(character_image, character_pos)
    pygame.display.flip()

# 종료
pygame.quit()
sys.exit()