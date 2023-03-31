import pygame, math, sys, random, os, time;
pygame.init();
tacobell = input("type 'True' or 'False' for using images");
if tacobell == "True" or tacobell == "t":
    useImage = True;
else: useImage = False;

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
        this.offsetX = 0;
        this.offsetY = 0;
        
camera = Camera();

skyblue = pygame.Color("skyblue");
green = pygame.Color("green");
brown = pygame.Color("brown");
gray = pygame.Color("gray");


tileSize = 30;


def tryImageLoad (filePath="/images") :
    global useImage;
    try: 
        pygame.image.load(path + "/images/stick figure/run.png");
    except:
        useImage = False;
print(useImage)
tryImageLoad();

    

if useImage:
    def transformImage (imageSource, animation, scale, frames) :
    
        width = imageSource[animation][0].get_width();
        height = imageSource[animation][0].get_height();
        imageSource[animation][0] = pygame.transform.scale(imageSource[animation][0], (width * scale, height * scale));
        imageSource[animation][5] = imageSource[animation][0].get_width() / frames;
        imageSource[animation][6] = imageSource[animation][0].get_height();

    stickAnim = {
        # items are: image, current frame, last frame, inbetween currect frame, inbetween last frame, width, height
        "run": [pygame.image.load(path+"/images/stick figure/run.png").convert_alpha(), 0, 22, 0, 1, 11, 11],
        # 22 frames, run at 22 - 44 fps, scale by 0.28
        "walk": [pygame.image.load(path+"/images/stick figure/walk.png").convert_alpha(), 0, 16, 0, 1, 11, 11],
        # 16 frames, run at 16 - 32 fps, scale by 0.255
        "idle": [pygame.image.load(path+"/images/stick figure/idle.png").convert_alpha(), 0, 2, 0, FPS*2, 11, 11],
        # 2 frames, run at 0.5 - 2 fps, scale by 0.255
        #"crouch": [pygame.image.load(path+"/images/stick figure/crouch.png").convert_alpha(), 0, 0, 0, 0]
        # single frame crouch animation, scale by 0.225
        "slide": [pygame.image.load(path+"/images/stick figure/slide.png").convert_alpha(), 0, 0, 0, 0, 11, 11]

    }

    tileImgs = [
    
    0,
    pygame.image.load(path + "\images\grass.png").convert(),
    pygame.image.load(path + "\images\dirt.png").convert(),
    pygame.image.load(path + "\images\stone.png").convert()
    
    ]

    transformImage(stickAnim, "run",  0.28, 22);
    transformImage(stickAnim, "walk", 0.255, 16);
    transformImage(stickAnim, "idle", 0.255, 2);
    transformImage(stickAnim, "slide", 0.255, 1);
    #transformImage(stickAnim, "crouch", 0.255);

else:
    
    stickAnim = {
        "run": [pygame.Rect(0, 0, 28, 57), 0, 22, 0, 1, 11, 11],
        # 22 frames, run at 22 - 44 fps, scale by 0.28
        "walk": [pygame.Rect(0, 0, 28, 57), 0, 16, 0, 1, 11, 11],
        # 16 frames, run at 16 - 32 fps, scale by 0.255
        "idle": [pygame.Rect(0, 0, 28, 57), 0, 2, 0, FPS, 11, 11],
        # 2 frames, run at 0.5 - 2 fps, scale by 0.255
        #"crouch": [pygame.image.load(path+"/images/stick figure/crouch.png").convert_alpha(), 0, 0, 0, 0]
        # single frame crouch animation, scale by 0.225
        "slide": [pygame.Rect(0, 0, 28, 28), 0, 0, 0, 0, 0]
    }

    tileImgs = [
        0,
        [pygame.Rect(0, 0, tileSize, tileSize), green], # grass
        [pygame.Rect(0, 0, tileSize, tileSize), brown], # dirt
        [pygame.Rect(0, 0, tileSize, tileSize), gray] # stone
    ]
    






chunks = {}
chunkSize = 10;



totalChunkSize = chunkSize * tileSize;

screenChunks = [1, 1];
 # calculate how many chunks should be on screen (width, height)
screenChunks[0] = math.ceil(sW / totalChunkSize) + 2;
screenChunks[1] = math.ceil(sH / totalChunkSize) + 2;




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
    
    
    
    
    
class Mouse:
    def __init__(mouse):
        
        mouse.absX = 0;
        mouse.absY = 0;
        mouse.x = 0;
        mouse.y = 0;

        mouse.offsetX = 0;
        mouse.offsetY = 0;

mouse = Mouse();



class Player ():
    def __init__(this):
    
        this.x = 0;
        this.y = 50;
        
        this.xv = 0;
        this.yv = 0;

        this.jumpPower = -3;
        this.maxXV = 8;
        this.maxYV = 300;

        this.lastChunkPos = 0;

        this.accel = 0.3;
        this.friction = 15;

        this.angle = 0;
        
        this.width = tileSize - 2;
        this.height = this.width * 2;
        this.flipH = False;

        this.animFrame = 0;
        this.anim = "run";

        this.image = stickAnim;
        
        

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
    
    try:
        tile = chunks [ ( chunkPos[0], chunkPos[1] ) ] [ ( tileX, tileY ) ];
    except:
        generateChunk(chunkPos[0], chunkPos[1])
        tile = chunks [ ( chunkPos[0], chunkPos[1] ) ] [ ( tileX, tileY ) ];
    else:
        tile = chunks [ ( chunkPos[0], chunkPos[1] ) ] [ ( tileX, tileY ) ];
        
    data = tile[0];
    
    if otherInfo: data = tile;
    
    
    return data;

player = Player();


def updateCamera () :
    
    camera.offsetX = mouse.absX - sW/2;
    camera.offsetY = mouse.absY - sH/2;
    
    camera.realX -= round((camera.realX - (player.x + player.width/2) + sW/2 - camera.offsetX) / camera.smoothness);
    camera.realY -= round((camera.realY - (player.y + player.height/2) + sH/2 - camera.offsetY) / camera.smoothness);
    
    if camera.shakeTime > 0:
        camera.shakeTime -= 1;
        camera.realX += random.randint(0, camera.shakeStrength*2) - camera.shakeStrength;
        camera.realY += random.randint(0, camera.shakeStrength*2) - camera.shakeStrength;
        
    camera.x = round(camera.realX);
    camera.y = round(camera.realY);


 # nav player
def playerFrame () :
    
    
    updateCamera();
    
    player.px = player.x;
    player.py = player.y;
    
    player.x += player.xv;
    player.y += player.yv;
    
    player.chunkPos = getChunkPos(player.x, player.y);
    
    player.tilePos = getTilePos(player.x, player.y);
    
    tileBelow = getTile(player.x, player.y + player.height);
  
    tileBottomRight = getTile(player.x + 1, player.y + 2);
   
    left = keys[pygame.K_a];
    right = keys[pygame.K_d];
    up = keys[pygame.K_SPACE];
    down = keys[pygame.K_s];
    

    

    if down:
        if tileBelow:
            if abs(player.xv) > player.maxXV / 2:
                player.anim = "slide";
            if player.anim == "slide":
                pass
    
    if tileBelow: 
        if useImage: screen.blit(tileImgs[3], (100, 100)); # show if ground collided without print's lag
        player.yv = 0;
        player.y = player.tilePos[1];
    else:
        player.yv += gravity;
    if not player.anim == "slide":
        if right: 
            if player.xv < player.maxXV: player.xv += player.accel;
        if left: 
            if player.xv > -player.maxXV: player.xv -= player.accel;
        
        if up and tileBelow:
            if not player.anim == "slide": player.yv = player.jumpPower;

    if player.xv == 0:
        if tileBelow:
            player.anim = "idle";
    
    if not player.xv == 0 and not player.anim == "slide":
        if tileBelow:
            if abs(player.xv) < player.maxXV / 1.5:
                player.anim = "walk";
            else:
                player.anim = "run";
    
    


    if (not left and not right) or (left and right) or player.anim == "slide":
         # friction
        
        player.xv -= player.xv / player.friction;
        if player.xv > -0.1 and player.xv < 0.1:
            player.xv = 0;


    if player.xv > 0:
        player.flipH = False;
    
    if player.xv < 0:
        player.flipH = True;

  
    if player.anim == "slide":
        player.height = player.width;
    else: player.height = player.width * 2;


    
    def animate () :
        if useImage:
            anim = player.image[player.anim];
            animRect = pygame.Rect(anim[1] * anim[5], 0, anim[5], anim[6]);
            num = 0;
            if player.anim == "run": num = -5;


            image = anim[0];

            image = pygame.Surface.subsurface(image, animRect);

            if player.flipH:
                image = pygame.transform.flip(image, True, False);

            image = pygame.transform.rotate(image, player.angle);


            screen.blit(image, (player.x-camera.x+num, player.y-camera.y+3));
            if not anim[2] == 0:
                anim[1] += 1;
                if anim[1] == anim[2]: anim[1] = 0;
            
                anim[3] += 1;
                

                player.image[player.anim] = anim;
        
        else:
            player.image[player.anim][0].x = int(player.x) - camera.x;
            player.image[player.anim][0].y = int(player.y) - camera.y;
            pygame.draw.rect(screen, gray, player.image[player.anim][0]);
    
    animate();

    
    if not player.lastChunkPos == player.chunkPos:
        print(player.chunkPos);
    player.lastChunkPos = player.chunkPos;
    

#Player Movement Things



def renderTiles (chunkPos) :
    
    chunkList = [];
    chunkPosList = [];
    currentChunk = 0;
    
    for x in range(screenChunks[0]):
        for y in range(screenChunks[1]):
            
            chunkX = chunkPos[0] + x;
            chunkY = chunkPos[1] + y;
            
            chunkPosList.append((chunkX, chunkY));
            try:
                chunkList.append(chunks[(chunkX, chunkY)]);
            except:
                generateChunk(chunkX, chunkY);
                chunkList.append(chunks[(chunkX, chunkY)]);
           # else:
           #     chunkList.append(chunks[(chunkX, chunkY)]);

    
    
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
                
                
                
                if useImage: screen.blit(tileImgs[tile[0]], (x-camera.x, y-camera.y));
                else: 
                    tileImgs[tile[0]][0].x = x - camera.x;
                    tileImgs[tile[0]][0].y = y - camera.y;
                    pygame.draw.rect(screen, tileImgs[tile[0]][1], tileImgs[tile[0]][0]);
        currentChunk += 1;
              
                
                
                
running = True;
while running: # game loop

    screen.fill(skyblue);
    
    keys = pygame.key.get_pressed();
    mousePos = pygame.mouse.get_pos();
    mouse.absX, mouse.absY = mousePos[0], mousePos[1];
    mouse.x, mouse.y = mouse.absX + camera.x, mouse.absY + camera.y;
    
    
    
    playerFrame();

    cameraChunk = getChunkPos(int(player.x - sW/2 + camera.offsetX), int(player.y - sH/2 + camera.offsetY));
    # player.x - sW/2 + camera.offsetX
    
    renderTiles(cameraChunk);
    
    
    #print(str(cameraChunk[0]) + ", " + str(cameraChunk[1]));
    
    
    
    
    
    
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
        
            pygame.quit();
            sys.exit();


    pygame.display.update();
    clock.tick(FPS/timeScale);
    

input() # stop game when it ends sometimes
