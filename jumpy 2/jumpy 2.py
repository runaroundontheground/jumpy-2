import pygame, math, sys, random, os;
pygame.init();



sW, sH = 600, 400;

screen = pygame.display.set_mode((sW, sH));
fps = 60;
clock = pygame.time.Clock();
path = os.path.dirname(os.path.realpath(__file__));
path += "/";

class camera():
    def __init__(c):
        c.x = 0;
        c.y = 0;
        c.shakeTime = 0;
        c.shakeStr = 5;
        c.smoothness = 15;
        
c = camera();

tileImgs = [
    
    0, # eventually change that to be images/tiles.png, then figure out clipping images
    pygame.image.load(path + "images\grass.png").convert(),
    pygame.image.load(path + "images\dirt.png").convert(),
    pygame.image.load(path + "images\stone.png").convert()
    
]




skyblue = pygame.Color("skyblue");


chunks = {}
chunkSize = 10;

tileSize = tileImgs[1].get_width(); 

totalChunkSize = chunkSize * tileSize;

screenChunks = [1, 1];
 # calculate how many chunks should be on screen (width, height)
screenChunks[0] = math.floor(sW / totalChunkSize) + 3;
screenChunks[1] = math.floor(sH / totalChunkSize) + 2;




def genChunk (chunkX, chunkY, retur = False) :
    chunkData = {};
    
    for x in range(chunkSize):
        for y in range(chunkSize):
            
             # find real position for generation
            tileX = chunkX * chunkSize + x;
            tileY = chunkY * chunkSize + y;
            
             # tile type is air by default
            tileType = 0; # air
            
            if tileY == chunkSize + 1: tileType = 1; # grass
            if tileY > chunkSize + 1: tileType = 2; # dirt
            if tileY > chunkSize * 2:
                if random.randint(1, int(100 / tileY)) == 1: tileType = 3; # stone
                
             # add tile to chunk's data
            chunkData[str(x) + ";" + str(y)] = [tileType];
            
     
    if retur: return chunkData;
    else: chunks[str(chunkX) + ";" + str(chunkY)] = chunkData;
    
    
class t(): # thing
    def __init__(t):
    
        t.x = 0;
        t.y = 50;
        
        t.xv = 0;
        t.yv = 0;
        
        t.w = tileSize;
        t.h = t.w# * 2;
        
        

 # pre-generate some chunks
for x in range(10):
    for y in range(3):
        genChunk(x, y);
        


def draw (img=tileImgs[1], x=0, y=0, static = False) :
    
    pos = 0;
    
    if static: cameraX, cameraY = 0, 0;
    else: cameraX, cameraY = c.x, c.y;
    
    if type(x) == tuple:
        pos = (x[0] + cameraX, x[1] + cameraY);
        
    else:
        pos = (x + cameraX, y + cameraY);
    
    screen.blit(img, pos);
    
def getChunkPos (x, y) :
    
    chunkX = math.floor(x / (totalChunkSize));
    chunkY = math.floor(y / (totalChunkSize));
    
    return (chunkX, chunkY);

def getChunk (chunkPos, generate = True) :
    
    chunkX = str(chunkPos[0]);
    chunkY = str(chunkPos[1]);
    
    if generate:
        try:
        
            chunk = chunks[chunkX + ";" + chunkY];
            
        except:
        
            genChunk(int(chunkX), int(chunkY));
            
            chunk = chunks[chunkX + ";" + chunkY];
    else: chunk = chunks[chunkX + ";" + chunkY];
        
    
    return chunk;
    
def getTile (chunkPos, tilePos, otherInfo = False) :
    
    if chunkPos[0] == chunkSize - 1:
        chunkPos = (chunkPos[0] + 1, chunkPos[1]);
        tilePos = (1, tilePos[1]);
    if chunkPos[1] == chunkSize - 1:
        chunkPos = (chunkPos[0], chunkPos[1] + 1);
        tilePos = (tilePos[0], 1);
    
    chunk = getChunk(chunkPos);
     # CURRENTLY FIXING GETTING THE POSITION
     # CAN'T ACCESS TILES IN A CHUNK NEARBY
    tileX = str(math.floor(tilePos[0] / tileSize))[-1];
    tileY = str(math.floor(tilePos[1] / tileSize))[-1];
    
    
    tile = chunk[str(tileX) + ";" + str(tileY)];
    data = False;
    if otherInfo:
        data = tile;
    else:
        if not tile[0] == 0:
            data = True;
    
    print(str(tileX) + ", " + str(tileY));
    
    return data;

plr = t();
plr.lastChunkPos = 0;

def playerFrame (p) :
    
     # do camera
    c.x -= round((p.x+p.w/2 + c.x - sW/2) / c.smoothness);
    c.y -= round((p.y+p.h/2 + c.y - sH/2) / c.smoothness);
    if c.shakeTime > 0:
        c.shakeTime -= 1;
        c.x += random.randint(0, c.shakeStr*2) - c.shakeStr;
        c.y += random.randint(0, c.shakeStr*2) - c.shakeStr;
        
    p.x += p.xv;
    p.y += p.yv;
    
    
    p.chunkPos = getChunkPos(p.x, p.y);
    
    tileBelow = getTile(p.chunkPos, (p.x, p.y + p.h));
    
    
    if tileBelow: draw(tileImgs[3], 100, 100, static = True);
    
    
    
    if keys[pygame.K_d]: p.x += 5;
    if keys[pygame.K_a]: p.x -= 5;
    
    if keys[pygame.K_w]: p.y -= 5; #p.yv = -3;
    if keys[pygame.K_s]: p.y += 5;
    
   

    draw(tileImgs[1], (p.x, p.y));
    
    if not p.lastChunkPos == p.chunkPos:
        print(p.chunkPos);
    p.lastChunkPos = p.chunkPos;
    



def renderTiles (chunkPos) :
    
    renderList = [];
    chunkPosList = [];
    
    xOffset = math.floor(screenChunks[0]/2);
    yOffset = math.floor(screenChunks[1]/2);
    
    for x in range(screenChunks[0]):
        for y in range(screenChunks[1]):
            
            chunkX = chunkPos[0] + x - xOffset;
            chunkY = chunkPos[1] + y - yOffset;
            pos = (chunkX, chunkY);
            
            chunkPosList.append(pos);
            renderList.append(getChunk(pos));
    
    currentChunk = 0;
    
    for chunk in renderList:
        for tilePos, tile in chunk.items():
            if not tile[0] == 0:
                
                xpos = int(tilePos[0]);
                ypos = int(tilePos[2]);
                
                x = xpos * chunkSize;
                y = ypos * chunkSize;
                
                chunkX = chunkPosList[currentChunk][0];
                chunkY = chunkPosList[currentChunk][1];
                
                x += chunkX * totalChunkSize;
                y += chunkY * totalChunkSize;
                
                
                 # close gap between tiles
                x += xpos * (tileSize - chunkSize);
                y += ypos * (tileSize - chunkSize);
                
                
                
                draw(tileImgs[tile[0]], (x, y));
        currentChunk += 1;
              
                
                
keys = pygame.key.get_pressed();
playerFrame(plr);
                
running = True;
while running: # game loop

    screen.fill(skyblue);
    
    keys = pygame.key.get_pressed();
    
    renderTiles(plr.chunkPos);
    
    
    
    playerFrame(plr);
    
    
    
    
    
    
    
    
    
    
    
    
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
        
            pygame.quit();
            sys.exit();


    pygame.display.update();
    clock.tick(fps);
    

input() # stop game when it ends sometimes