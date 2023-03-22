import pygame, math, sys, random, os, time;
pygame.init();



sW, sH = 1200, 800; # normally 600, 400

screen = pygame.display.set_mode((sW, sH));
clock = pygame.time.Clock();
path = os.path.dirname(os.path.realpath(__file__));

FPS = 60;
timeScale = 1.0;
gravity = 0.1;

class Camera():
    def __init__(this):
        this.realX = 0;
        this.realY = 0;
        this.x = 0;
        this.y = 0;
        this.shakeTime = 0;
        this.shakeStrength = 5;
        this.smoothness = 15;
        
camera = Camera();

tileImgs = [
    
    0, # eventually change that to be images/tiles.png, then figure out clipping images for a spritesheet
    pygame.image.load(path + "\images\grass.png").convert(),
    pygame.image.load(path + "\images\dirt.png").convert(),
    pygame.image.load(path + "\images\stone.png").convert()
    
]

tileSize = tileImgs[1].get_width(); 

stickAnim = [
    pygame.image.load(path+"/images/stick figure/run.png").convert() # 22 frame animation, best at 44 fps, * by .2
]
stickAnim[0].set_colorkey((255,255,255));
stickAnim[0] = pygame.transform.scale(stickAnim[0], (stickAnim[0].get_width()*1, stickAnim[0].get_height()*1));
print(stickAnim[0].get_height());
skyblue = pygame.Color("skyblue");


chunks = {}
chunkSize = 10;



totalChunkSize = chunkSize * tileSize;

screenChunks = [1, 1];
 # calculate how many chunks should be on screen (width, height)
screenChunks[0] = math.floor(sW / totalChunkSize) + 3;
screenChunks[1] = math.floor(sH / totalChunkSize) + 2;




def generateChunk (chunkX, chunkY) :

    chunkData = {};
    
    for x in range(chunkSize):
        for y in range(chunkSize):
            
            
            tileX = chunkX * chunkSize + x;
            tileY = chunkY * chunkSize + y;
            
            
            
            tileType = 0; # air
            if tileY == chunkSize: tileType = 1; # grass
            if tileY > chunkSize: tileType = 2; # dirt
            if tileY > chunkSize * 2:
                if random.randint(1, int(100 / tileY)) == 1: tileType = 3; # stone
            
            
            tileData = [tileType];
            
            chunkData[(x, y)] = tileData;
            
            
            
    
    chunks[(chunkX, chunkY)] = chunkData;
    
    
    
    
    
    
    
class Player (): # thing
    def __init__(t):
    
        t.x = 0;
        t.y = 50;
        
        t.xv = 0;
        t.yv = 0;
        
        t.w = tileSize;
        t.h = t.w * 2;
        
        

 # pre-generate some chunks
for x in range(10):
    for y in range(3):
        generateChunk(x, y);
        



    
def getChunkPos (x, y) :
    
    chunkX = math.floor(x / (totalChunkSize));
    chunkY = math.floor(y / (totalChunkSize));
    
    return (chunkX, chunkY);

def testChunk (x, y) :
    
    try:
        testVar = chunks[(x, y)];
    except:
        chunks[(x, y)] = generateChunk(x, y);

def getTilePos (x, y):
    
    x = math.floor(x/tileSize);
    y = math.floor(y/tileSize);
    
    x *= tileSize;
    y *= tileSize;
    
    return (x, y);
    
def getTile (x, y, otherInfo = False) :
    
    chunkPos = getChunkPos(x, y);
    
  #  chunk = getChunk(chunkPos[0], chunkPos[1]);
    
    x = math.floor(x/tileSize);
    y = math.floor(y/tileSize);
    
    tileX = int(str(x)[-1]);
    tileY = int(str(y)[-1]);
    
    tile = chunks [ ( chunkPos[0], chunkPos[1] ) ] [ ( tileX, tileY ) ];
    
    data = tile[0];
    
    if otherInfo: data = tile;
    
    
    return data;

player = Player();
player.lastChunkPos = 0;

def updateCamera () :
    
    mouseOffsetX = mousePos[0] - sW/2;
    mouseOffsetY = mousePos[1] - sH/2;
    
    camera.realX -= round((camera.realX - (player.x + player.w/2) + sW/2 - mouseOffsetX) / camera.smoothness);
    camera.realY -= round((camera.realY - (player.y + player.h/2) + sH/2 - mouseOffsetY) / camera.smoothness);
    
    if camera.shakeTime > 0:
        camera.shakeTime -= 1;
        camera.realX += random.randint(0, camera.shakeStrength*2) - camera.shakeStrength;
        camera.realY += random.randint(0, camera.shakeStrength*2) - camera.shakeStrength;
        
    camera.x = round(camera.realX);
    camera.y = round(camera.realY);



def playerFrame () :
    
     
    updateCamera();
    
    player.px = player.x;
    player.py = player.y;
    
    player.x += player.xv;
    player.y += player.yv;
    
    player.chunkPos = getChunkPos(player.x, player.y);
    
    player.tilePos = getTilePos(player.x, player.y);
    #REMOVE LATER!!!
    screen.blit(stickAnim[0], (100, 200));
    tileBelow = getTile(player.x, player.y + player.h);
    
    #print(player.tilePos);
    
    if tileBelow: 
        screen.blit(tileImgs[3], (100, 100)); # show if ground collided without print's lag
        player.yv = 0;
        player.y = player.tilePos[1];
        player.yv += 0.1;
    else:
        player.yv += gravity;
    if keys[pygame.K_d]: player.x += 5;
    if keys[pygame.K_a]: player.x -= 5;
    
    if keys[pygame.K_w] and tileBelow: player.yv = -3;
  #  if keys[pygame.K_s]: player.y += 5;
    
   

    screen.blit(tileImgs[1], (player.x-camera.x, player.y-camera.y));
    
    if not player.lastChunkPos == player.chunkPos:
        print(player.chunkPos);
    player.lastChunkPos = player.chunkPos;
    




def renderTiles (chunkPos) :
    
    chunkList = [];
    chunkPosList = [];
    renderList = [];
    
    xOffset = math.floor(screenChunks[0]/2);
    yOffset = math.floor(screenChunks[1]/2);
    
    for x in range(screenChunks[0]):
        for y in range(screenChunks[1]):
            
            chunkX = chunkPos[0] + x - xOffset;
            chunkY = chunkPos[1] + y - yOffset;
            
            chunkPosList.append((chunkX, chunkY));
            try:
                chunkList.append(chunks[(chunkX, chunkY)]);
            except:
                generateChunk(chunkX, chunkY);
                chunkList.append(chunks[(chunkX, chunkY)]);
    currentChunk = 0;
    
    for chunk in chunkList:
        for tilePos, tile in chunk.items():
            if not tile[0] == 0:
                
                xpos = int(tilePos[0]);
                ypos = int(tilePos[1]);
                
                x = xpos * chunkSize;
                y = ypos * chunkSize;
                
                chunkX = chunkPosList[currentChunk][0];
                chunkY = chunkPosList[currentChunk][1];
                
                x += chunkX * totalChunkSize;
                y += chunkY * totalChunkSize;
                
                
                 # close gap between tiles
                x += xpos * (tileSize - chunkSize);
                y += ypos * (tileSize - chunkSize);
                
                
                
                screen.blit(tileImgs[tile[0]], (x-camera.x, y-camera.y));
        currentChunk += 1;
              
                
                

                
running = True;
while running: # game loop

    screen.fill(skyblue);
    
    keys = pygame.key.get_pressed();
    mousePos = pygame.mouse.get_pos();
   
    
    
    
    playerFrame();
    cameraChunk = getChunkPos(int(mousePos[0] + camera.x), int(mousePos[1] + camera.y));
    
    renderTiles(cameraChunk);
    
    
    print(str(cameraChunk[0]) + ", " + str(cameraChunk[1]));
    
    
    
    
    
    
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
        
            pygame.quit();
            sys.exit();


    pygame.display.update();
    clock.tick(FPS/timeScale);
    

input() # stop game when it ends sometimes
