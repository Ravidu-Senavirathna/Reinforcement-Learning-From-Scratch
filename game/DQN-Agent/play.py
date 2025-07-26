import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import Util
import Constants
from env   import GameEnv
from agent import DQNAgent

SAVE_PATH = os.path.join(os.path.dirname(__file__), 'dqn_weights.pth')
num_episodes = 20
fps = 60

def play():
    pygame.init()

    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pygame.display.set_caption('DQN Agent')

    font   = pygame.font.Font(None, 36)
    tick   = pygame.time.Clock()


    env   = GameEnv()
    agent = DQNAgent()
    agent.load(SAVE_PATH)


    for episode in range(1, num_episodes + 1):
        state     = env.reset()
        score     = 0
        done      = False

        while not done:
            # Quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit(); return
                
            action = agent.act(state)
            state, reward, done, info = env.step(action)
            if info.get('collected'):
                score += 1

            player, point = env.get_render_data()
            score_text = font.render(
                f'Episode {episode} | Score: {score}', True, Constants.WHITE
            )
            Util.draw_frame(screen, player, point, score_text)
            pygame.display.flip()
            tick.tick(fps)

        print(f'Episode {episode}: score = {score}')
    pygame.quit()

if __name__ == '__main__':
    play()