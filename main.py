

import sys
import numpy as np
import miniaudio
import statsmodels.api as sm
import time
import pygame
import scipy
import utility_functions
import audio_device

from constants import WIDTH, HEIGHT, FPS,\
    SAMPLES_PER_SEC, SAMPLES_PER_BUFFER, MSECS_PER_BUFFER,\
    SAMPLES_PER_DETECTION, FREQ_STEP, NOTE_MAX, NOTE_MIN, N_LAGS, ROLLBACK, NUM_NOTES

class Player:
    def __init__(self,xpos):
        self.length = HEIGHT // 5
        self.xpos = xpos
        self.ypos = 0.0

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            'white', 
            pygame.Rect(
                self.xpos, 
                HEIGHT - (self.length / 2) - self.ypos,
                4,
                self.length
            )
        ) 

class Ball:
    def __init__(self) -> None:
        self.radius = HEIGHT // 50
        self.xpos = WIDTH / 2
        self.ypos = HEIGHT / 2
        self.xvel = -500.0
        self.yvel = 0.0
        self.deflect = 2.0

def main():

    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
    CLOCK = pygame.time.Clock()

    FREQ_MAX = utility_functions.number_to_freq(NOTE_MAX)
    FREQ_MIN = utility_functions.number_to_freq(NOTE_MIN)

    capture_device = audio_device.make_audio_capture_device()

    player_1 = Player(0)
    player_2 = Player(WIDTH)
    ball = Ball()

    # Set up requisite generator function for capture. This is the main loop
    def record_to_buffer():

        # Allocate space to run an FFT. 
        samples = np.zeros(SAMPLES_PER_DETECTION, dtype=np.int16)
        # Allocate space to represent pitch at each moment in time:
        #pitches = np.zeros(WIDTH)
        _ = yield
        while True:
            
            buffer = yield
            #print(".", end="", flush=True)
            #buffer_chunks.append(buffer)
            samples[:-SAMPLES_PER_BUFFER] = samples[SAMPLES_PER_BUFFER:]
            samples[-SAMPLES_PER_BUFFER:] = np.frombuffer(buffer, dtype=np.int16)
            
            my_auto = sm.tsa.stattools.acf(samples, nlags=N_LAGS)
            info = scipy.signal.find_peaks(my_auto, height = 0.3)
            peaks = list(info[0])
            heights = info[1]['peak_heights']
            if peaks:
                index = np.argmax(heights)
                freq = SAMPLES_PER_SEC/peaks[index]
                note_num = utility_functions.freq_to_number(freq)
                player_1.ypos = (HEIGHT*(note_num - NOTE_MIN)) // (NOTE_MAX-NOTE_MIN)

                    
                

           
        

    generator = record_to_buffer()
    next(generator)

    capture_device.start(generator)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                capture_device.stop()
                pygame.quit()
                sys.exit()
                running = False
        # Get the current state of all keys
        keys = pygame.key.get_pressed()

        # Check if two keys are pressed simultaneously
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            SCREEN.fill((100,100,100))
        
        else:
            SCREEN.fill((0, 0, 0))
        
        player_1.draw(SCREEN)

        ball.xpos += ball.xvel/FPS
        ball.ypos += ball.yvel/FPS

        if ball.xpos < ball.radius:
            if (ball.ypos < player_1.ypos + player_1.length / 2) \
            and (ball.ypos > player_1.ypos - player_1.length /2):
                ball.xpos = ball.radius - ball.xpos + ball.radius
                ball.xvel *= -1
                ball.yvel += ball.deflect*(ball.ypos - (player_1.ypos))
                
            else:
                ball.xpos = WIDTH
                ball.ypos = HEIGHT / 2
                ball.yvel = 0
        elif ball.xpos > WIDTH-ball.radius:
            ball.xpos = WIDTH - ball.radius - (ball.xpos - (WIDTH - ball.radius))
            ball.xvel *= -1

        if ball.ypos < ball.radius:
            ball.ypos = ball.radius - ball.ypos + ball.radius
            ball.yvel *= -1
        elif ball.ypos > HEIGHT-ball.radius:
            ball.ypos = HEIGHT - ball.radius - (ball.ypos - (HEIGHT - ball.radius))
            ball.yvel *= -1
        
        
        pygame.draw.circle(SCREEN,'white',(ball.xpos,HEIGHT - ball.ypos), ball.radius)
        pygame.display.flip()
        CLOCK.tick(FPS)
        

if __name__ == '__main__':
    main()
    
    