import random
import sys
import pygame

# Константы
screenWidth, screenHeight = 300, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
framePerSecond, scrollSpeed = 30, 4
baseY, pipeGap, pipeHeight, pipeWidth = screenHeight * 0.75, screenHeight / 4, 300, 70
collision = False

# Пути к изображениям
title, background, pipe, player, base, gameOver = (
    'gallery/title.png', 'gallery/background.png', 'gallery/pipes.png',
    'gallery/ruble.png', 'gallery/ground.png', 'gallery/gameOver.png'
)

# Словарь для изображений
game_images = {
    'title': pygame.transform.scale(pygame.image.load(title), (200, 100)),
    'base': pygame.transform.scale(pygame.image.load(base), (screenWidth * 2, 200)),
    'pipe': (
        pygame.transform.rotate(pygame.transform.scale(pygame.image.load(pipe), (pipeWidth, pipeHeight)), 180),
        pygame.transform.scale(pygame.image.load(pipe), (pipeWidth, pipeHeight))
    ),
    'background': pygame.transform.scale(pygame.image.load(background), (screenWidth, screenHeight)),
    'player': pygame.transform.scale(pygame.image.load(player), (50, 50)),
    'gameOver': pygame.transform.scale(pygame.image.load(gameOver), (200, 100)),
    'score': tuple(pygame.transform.scale(pygame.image.load(f'gallery/{i}.png'), (50, 50)) for i in range(10))
}


# Загрузка изображений
def load_images():
    pass


# Игровой цикл начального экрана
def startGame():
    playerX, playerY, titleX, titleY, baseX = int(screenWidth * 0.4), int(
        (screenHeight - game_images['player'].get_height()) * 0.5), int(
        (screenWidth - game_images['title'].get_width()) * 0.5), int(screenHeight * 0.2), 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                play()
            else:
                screen.blit(game_images['background'], (0, 0))
                screen.blit(game_images['player'], (playerX, playerY))
                screen.blit(game_images['base'], (baseX, baseY))
                screen.blit(game_images['title'], (titleX, titleY))
                pygame.display.update()
                fps_clock.tick(framePerSecond)


# Игровой цикл основной игры
def play():
    playerX, playerY, baseX, vel, score = int(screenWidth * 0.4), int(
        (screenHeight - game_images['player'].get_height()) * 0.5), 0, 0, 0
    newPipe1, newPipe2 = getRandomPipe(), getRandomPipe()
    upperPipes = [{'x': screenWidth + 200, 'y': newPipe1[0]['y']},
                  {'x': screenWidth + 200 + (screenWidth / 2), 'y': newPipe2[0]['y']}]
    lowerPipes = [{'x': screenWidth + 200, 'y': newPipe1[1]['y']},
                  {'x': screenWidth + 200 + (screenWidth / 2), 'y': newPipe2[1]['y']}]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                vel = -10
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                vel = 4

        playerY += vel
        collision = crashTest(playerX, playerY, upperPipes, lowerPipes)
        if collision:
            endGame(score)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] -= scrollSpeed
            lowerPipe['x'] -= scrollSpeed

        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]['x'] < -game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        screen.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_images['base'], (baseX, baseY))
        screen.blit(game_images['player'], (playerX, playerY))
        baseX -= scrollSpeed
        if abs(baseX) > screenWidth:
            baseX = 0

        playerMidPos = playerX + game_images['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_images['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_images['score'][digit].get_width()
        scoreX = (screenWidth - width) / 2
        scoreY = screenHeight * 0.12

        for digit in myDigits:
            screen.blit(game_images['score'][digit], (scoreX, scoreY))
            scoreX += game_images['score'][digit].get_width()

        pygame.display.update()
        fps_clock.tick(framePerSecond)


# Генерация случайных труб
def getRandomPipe():
    gapY = random.randrange(0, int(baseY * 0.5 - pipeGap))
    gapY += int(baseY * 0.1)
    pipeX = screenWidth + 100
    pipes = [
        {'x': pipeX, 'y': gapY - pipeHeight},  # Верхняя труба
        {'x': pipeX, 'y': gapY + pipeGap},  # Нижняя труба
    ]
    return pipes


# Проверка столкновения
def crashTest(playerx, playery, upperPipes, lowerPipes):
    score = 0
    if playery <= 0 or playery >= 700:
        return True
    else:
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            if abs(playerx - upperpipe['x']) <= game_images['pipe'][0].get_width():
                if playery <= pipeHeight + upperpipe['y']:
                    return True
            if abs(playerx - lowerpipe['x']) <= game_images['pipe'][0].get_width():
                if playery + game_images['player'].get_height() >= lowerpipe['y']:
                    return True
        return False


# Завершение игры
def endGame(score):
    gameOverX, gameOverY = int((screenWidth - game_images['gameOver'].get_width()) * 0.5), int(screenHeight * 0.2)
    screen.blit(game_images['background'], (0, 0))
    screen.blit(game_images['gameOver'], (gameOverX, gameOverY))
    screen.blit(game_images['base'], (0, baseY))
    scoreFont = pygame.font.SysFont('couriernew', 40, bold=True)
    display = scoreFont.render(f"Score: {score}", True, (255, 127, 0))
    screen.blit(display, (screenWidth * 0.2, screenHeight * 0.4))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                startGame()

        pygame.display.update()
        fps_clock.tick(framePerSecond)


# Инициализация Pygame
if __name__ == "__main__":
    pygame.init()
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Adventures of Flappy Rubles')
    load_images()

    while True:
        startGame()
