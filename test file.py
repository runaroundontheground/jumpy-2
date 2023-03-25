import pygame
pygame.init();
 # this file is for testing things, if you couldn't tell by the name lol
screen = pygame.display.set_mode((100,100));
clock = pygame.time.Clock();

testEvent = pygame.event.custom_type();
pygame.time.set_timer(testEvent, 1000);
print(testEvent);


fps = 60

timescale = 0.1

def updateAnimations () :
    
    print("update the aniamtions");
    # player.updateAnimations()
    # for enemy in enemies: enemy.updateAnimations()
    
    # this removes the previous timer, and sets a new one (delay is in ms)
    pygame.time.set_timer(testEvent, int(1000/fps/timescale));

while True:
    
    
    
    for event in pygame.event.get():
        
        if event.type == testEvent:
            updateAnimations();
    clock.tick(60);


input("don't let the thing close yet please");

