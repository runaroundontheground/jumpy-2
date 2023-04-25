import pygame, math, sys, random, os, time;
pygame.init();

sW, sH = 1200, 800; # normally 600, 400

screen = pygame.display.set_mode((sW, sH));
screenRect = pygame.Rect(0, 0, sW, sH);
clock = pygame.time.Clock();

hotbarRect = pygame.Rect(0, 0, 50, 50);
if os.path.exists("C:/jumpy 2 stuff"):
    path = "C:/jumpy 2 stuff/";
    useImage = True;
else:
    useImage = True;
    path = os.path.dirname(os.path.realpath(__file__));
    path += "/";



try:
    pass;
except:
    pass;

FPS = 60;
timeScale = 1.0;
gravity = 0.3;

enemies = [];
projectiles = [];
groundItems = [];


        

black = pygame.Color("black");
red = pygame.Color("red");
orange = pygame.Color("orange");
skyblue = pygame.Color("skyblue");
green = pygame.Color("green");
brown = pygame.Color("brown");
gray = pygame.Color("gray");
yellow = pygame.Color("yellow");
blue = pygame.Color("blue");

tileSize = 30;
screenRect.x = -tileSize;
screenRect.y = -tileSize;
screenRect.width += tileSize;
screenRect.height += tileSize;
    

if useImage:
    print("useing images");
    def transformImage (animation, scale) :
    
        width = stickAnim[animation]["image"].get_width();
        height = stickAnim[animation]["image"].get_height();
        stickAnim[animation]["image"] = pygame.transform.scale(stickAnim[animation]["image"], (round(width * scale), round(height * scale)));
        stickAnim[animation]["width"] = stickAnim[animation]["image"].get_width() / stickAnim[animation]["frames"];
        stickAnim[animation]["height"] = stickAnim[animation]["image"].get_height();

    stickAnim = {
        
        "run": {
            "image": pygame.image.load(path + "animations/run/run.png").convert_alpha(),
            "currentFrame": 0,
            "frames": 22, 
            "currentMidFrame": 0,
            "lastMidFrame": 1,
            "width": 1, # this isn't assigned until later
            "height": 1, # this isn't assigned until later
            "singleFrame": False
            },
        
        "walk": {
            "image": pygame.image.load(path + "animations/walk/walk.png").convert_alpha(),
            "currentFrame": 0, 
            "frames": 16, 
            "currentMidFrame": 0, 
            "lastMidFrame": 1, 
            "width": 1,
            "height": 1,
            "singleFrame": False
            },
        
        "idle": {
            "image": pygame.image.load(path + "animations/idle/idle.png").convert_alpha(), 
            "currentFrame": 0, 
            "frames": 2, 
            "currentMidFrame": 0, 
            "lastMidFrame": FPS*2, 
            "width": 1,
            "height": 1,
            "singleFrame": False
            },
        
        "slide (in)": {
            "image": pygame.image.load(path + "animations/slide/slide (in).png").convert_alpha(),
            "currentFrame": 0,
            "frames": 8, 
            "currentMidFrame": 0, 
            "lastMidFrame": 1,
            "width": 1,
            "height": 1, 
            "singleFrame": False
            },
        
        "slide (mid)": {
            "image": pygame.image.load(path + "animations/slide/slide (mid).png").convert_alpha(),
            "currentFrame": 0,
            "frames": 3,
            "currentMidFrame": 0,
            "lastMidFrame": 0,
            "width": 1,
            "height": 1,
            "singleFrame": False
           },
        
        "slide (out)": {
            "image": pygame.image.load(path + "animations/tpose.png").convert_alpha(),
            "currentFrame": 0,
            "frames": 8,
            "currentMidFrame": 0,
            "lastMidFrame": 1,
            "width": 1,
            "height": 1,
            "singleFrame": True
        },

        "crouch": {
            "image": pygame.image.load(path + "animations/tpose.png").convert_alpha(),
            "currentFrame": 0,
            "frames": 1,
            "currentMidFrame": 0,
            "lastMidFrame": 1,
            "width": 1,
            "height": 1,
            "singleFrame": True
        },

        "crouch walk": {
            "image": pygame.image.load(path + "animations/tpose.png").convert_alpha(),
            "currentFrame": 0,
            "frames": 8,
            "currentMidFrame": 0,
            "lastMidFrame": 1,
            "width": 1,
            "height": 1,
            "singleFrame": True
        },

        "swing": {
            "image": pygame.image.load(path + "animations/tpose.png").convert_alpha(),
            "currentFrame": 0,
            "frames": 8,
            "currentMidFrame": 0,
            "lastMidFrame": 1,
            "width": 1,
            "height": 1,
            "singleFrame": True
        },

        "fall": {
            "image": pygame.image.load(path + "animations/fall/fall.png").convert_alpha(),
            "currentFrame": 0,
            "frames": 1,
            "currentMidFrame": 0,
            "lastMidFrame": 1,
            "width": 1,
            "height": 1,
            "singleFrame": True
        },

        "wallclimb": {
            "image": pygame.image.load(path + "animations/tpose.png").convert_alpha(),
            "currentFrame": 0,
            "frames": 1,
            "currentMidFrame": 0,
            "lastMidFrame": 1,
            "width": 1,
            "height": 1,
            "singleFrame": True
        }

    }

    tileImgs = [
    
    0,
    pygame.image.load(path + "\images\grass.png").convert(),
    pygame.image.load(path + "\images\dirt.png").convert(),
    pygame.image.load(path + "\images\stone.png").convert()
    
    ]

    toolImgs = [
        pygame.image.load(path + "images/multitool.png")
    ]
    transformImage("run",  0.28);
    transformImage("walk", 0.255);
    transformImage("idle", 0.255);
    transformImage("slide (in)", 0.255);
    transformImage("slide (mid)", 0.255);
    transformImage("crouch", 0.255);
    transformImage("fall", 0.255);
    

else:
    
    stickAnim = {
        "run": [pygame.Rect(0, 0, 28, 57), 0, 22, 0, 1, 11, 11],
        "walk": [pygame.Rect(0, 0, 28, 57), 0, 16, 0, 3, 11, 11],
        "idle": [pygame.Rect(0, 0, 28, 57), 0, 2, 0, FPS, 11, 11],
        "slide (in)": [pygame.Rect(0, 0, 28, 28), 0, 0, 0, 0, 0],
        "slide (mid)": [pygame.Rect(0, 0, 28, 28), 0, 0, 0, 0, 0],
        "slide (out)": [pygame.Rect(0, 0, 28, 28), 0, 0, 0, 0, 0],
        "crouch": [pygame.Rect(0, 0, 28, 28), 0, 0, 0, 0, 0],
        "crouch walk": [pygame.Rect(0, 0, 28, 28), 0, 0, 0, 0, 0],
        "wallclimb": [pygame.Rect(0, 0, 28, 57), 0, 0, 0, 0, 0],
        "tpose": [pygame.Rect(0, 0, 28, 57), 0, 0, 0, 0, 0]
        
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




def generateChunk (chunkPos) :

    chunkData = {};
    
    for x in range(chunkSize):
        for y in range(chunkSize):
            
            
            tileX = chunkPos[0] * chunkSize + x;
            tileY = chunkPos[1] * chunkSize + y;
            
            #tileX is for adding like a beach or something once it go far enoghsiuus
            
            tileType = 0; # air
            if tileY == chunkSize: tileType = 1; # grass
            if tileY > chunkSize: tileType = 2; # dirt
            if tileY > chunkSize * 2:
                if random.randint(1, int(100 / tileY) + 1) == 1: tileType = 3; # stone
             # small chance for floating blocks
            if random.randint(1, 1000) == 1 and tileY < chunkSize: tileType = random.randint(1, 3);
            
            tileData = [tileType];
            
            chunkData[(x, y)] = tileData;
            
            
            
    
    chunks[chunkPos] = chunkData;
    

# item classes
if useImage:
    icons = {
        "grass": pygame.Surface.copy(tileImgs[1]),
        "dirt": pygame.Surface.copy(tileImgs[2]),
        "stone": pygame.Surface.copy(tileImgs[3]),
        "multitool": pygame.Surface.copy(toolImgs[0])
    };
    icons["multitool"] = pygame.transform.scale(icons["multitool"], (round(icons["multitool"].get_width() * 1.7), round(icons["multitool"].get_height() * 1.7)));
else:
    icons = {
        "grass": [pygame.Rect.copy(tileImgs[1][0]), tileImgs[1][1]],
        "dirt": [pygame.Rect.copy(tileImgs[2][0]), tileImgs[2][1]],
        "stone": [pygame.Rect.copy(tileImgs[3][0]), tileImgs[3][1]]
    };
    for key, icon in icons.items():
        pass # still resize, but not needed

class tileItem ():
    def __init__(this, data = [1], icon = "grass"):
        this.data = data;
        this.icon = icons[icon];

    def use(this):
            testChunk((mouse.x, mouse.y));
            chunkPos = getChunkPos(mouse.x, mouse.y);
            tilePos = getTilePos(mouse.x, mouse.y, True);

            if chunks[chunkPos][tilePos] == [0]: pass # normally place tile, otherwise blockswap and drop other tile
            chunks[chunkPos][tilePos] = this.data;

class toolItem ():
    def __init__(this, breakType = "all", icon = "multitool"):
        this.breakType = breakType;
        this.icon = icons[icon];

    def use(this):
        
        if mouse.button == 1:
            if True: pass;
            testChunk((mouse.x, mouse.y));
            chunkPos = getChunkPos(mouse.x, mouse.y);
            tilePos = getTilePos(mouse.x, mouse.y, True);

            if chunks[chunkPos][tilePos] != [0]:
                otherTilePos = getTilePos(mouse.x, mouse.y);
                spawnItem(xv = random.randint(-5, 5), yv = random.randint(-5, 5), x = otherTilePos[0], y = otherTilePos[1], id = chunks[chunkPos][tilePos][0]);

            chunks[chunkPos][tilePos] = [0];

#class meleeItem ():

#class rangedItem ():

items = [
    0,
    tileItem([1], "grass"),
    tileItem([2], "dirt"),
    tileItem([3], "stone"),
    
    toolItem()
]

class Mouse:
    def __init__(mouse):
        
        mouse.absX = 0;
        mouse.absY = 0;
        mouse.x = 0;
        mouse.y = 0;
        mouse.down = False;
        mouse.button = 1;
        mouse.pressed = False;

        mouse.offsetX = 0;
        mouse.offsetY = 0;

class Tiles ():
    def __init__ (this):
        this.right = False;
        this.left = False;
        this.top = False;
        this.bottom = False;

class Hotbar ():
    def __init__(this):
        this.slot = 1;
        this.slotContents = {
            0: "none",
            1: "none",
            2: "none",
            3: "none",
            4: "none"
        }

class Player ():
    def __init__(this):
    
        this.x = 0; # normal 0
        this.y = 50; # normal 50
        
        this.xv = 0; # normal 0
        this.yv = 0; # normal 0

        this.lockX = False;
        this.lockY = False;

        this.rect = pygame.Rect(0, 0, 0, 0);
        
        this.jumpPower = -5; # normal -5
        this.maxXV = 8; # normal 8
        this.maxYV = 300; # normal 300
        this.crouchSpeed = 3; # normal 3
        this.tilePos = (0, 0);
        this.lastChunkPos = 0;
        this.tiles = Tiles();
        this.chunkPos = (0, 0);

        this.accel = 0.3; # normal 0.3
        this.friction = 15; # normal 15
        this.angle = 0;
        this.bHopSpeed = 0.5; # normal 0.5
        
        this.abilityToggles = {
            "slide": True,
            "wallclimb": True,
            "hook": True
        };

        this.abilitesUsed = {
            "wallclimb": False,
        };

        this.width = tileSize;
        this.height = this.width * 2;
        this.flipH = False;

        this.anim = "idle";
        this.state = "idle";

        this.image = stickAnim;
        
        this.hotbar = Hotbar();

        this.hotbar.slotContents[0] = items[1];
        this.hotbar.slotContents[1] = items[4];

        this.hotbar.slot = 0;
        this.inventory = {
            0: "none",
            1: "none",
            2: "none",
            3: "none",
            4: "none",
            5: "none",
            6: "none",
            7: "none",
            8: "none",
            "open": False
        }

        this.useTime = 0;
        
class Grapple () :
    def __init__(this):
        this.x = 0;
        this.y = 0;
        
        this.px = 0;
        this.py = 0;
        
        this.distance = 0;
        this.distanceX = 0;
        this.distanceY = 0;
        
        this.xv = 0;
        this.yv = 0;
        this.angularVel = 0;
        this.angle = 0;
        this.strength = 0.05;
        this.launchVel = 20;
        
        this.fired = False;
        this.hooked = False;

    def unhook (this):
        grapple.hooked = False;
                        
        player.yv = grapple.distanceX - grapple.distance * -grapple.angularVel;
        player.xv = grapple.distanceY - grapple.distance * -grapple.angularVel;

        if grapple.angle > 270: player.yv *= -1;
        elif grapple.angle > 180: player.yv *= -1; player.xv *= -1;
        elif grapple.angle > 90: player.yv *= -1;
        
        player.xv /= 100;
        player.yv /= 100;

        
    def hook (this):
    
        grapple.hooked = True;
        grapple.fired = False;
        
        grapple.distance = math.dist((player.x, player.y), (grapple.x, grapple.y));
        #if grapple.distance > 300:
        #    grapple.inUse = False;
        dx = grapple.x - player.x;
        dy = grapple.y - player.y;

        grapple.angle = round(math.degrees(math.atan2(-dy, dx)));
        otherNum = player.yv;
        if player.xv < 0: otherNum *= -1;
        grapple.angularVel = player.xv + otherNum;
        grapple.angularVel /= 3;

        player.xv = 0;
        player.yv = 0;

        grapple.xv = 0;
        grapple.yv = 0;
    
    def fire (this):

        grapple.fired = True;

        grapple.x = player.x;
        grapple.y = player.y;
        
        dx = mouse.x - player.x;
        dy = mouse.y - player.y;

        grapple.angle = round(math.degrees(math.atan2(-dy, dx)));

        grapple.xv = math.cos(math.radians(grapple.angle));
        grapple.yv = math.sin(math.radians(grapple.angle));

        grapple.xv *= grapple.launchVel;
        grapple.yv *= -grapple.launchVel;

    def update (this):

        this.x += this.xv;
        this.y += this.yv;

        if math.dist((player.x, player.y), (this.x, this.y)) > 500: grapple.fired = False; grapple.hooked = False;

        if getTile(this.x, this.y): grapple.hook();

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
        
        this.px = 0;
        this.py = 0;

class itemEntity():
    def __init__(this, x = 0, y = 0, xv = 0, yv = 0, id = 1):

        this.x = x;
        this.y = y;

        this.xv = xv;
        this.yv = yv;

        this.data = items[id];
        this.itemId = id;
        
        this.image = this.data.icon;

def spawnItem(x = 0, y = 0, xv = 0, yv = 0, id = "dirt"):
    item = itemEntity(x, y, xv, yv, id);
    groundItems.append(item);

def getChunkPos (x, y) :
    
    chunkX = math.floor(x / (totalChunkSize));
    chunkY = math.floor(y / (totalChunkSize));
    
    return (chunkX, chunkY);

def testChunk (pos) :
    
    try:
        chunks[pos];
    except:
        generateChunk(pos);
        return False;
    else:
        return True;

def getTilePos (x, y, withinChunk = False):
    
    x = math.floor(x/tileSize);
    y = math.floor(y/tileSize);
    
    if not withinChunk:
        x *= tileSize;
        y *= tileSize;
    else:
        if x > 0: 
            while x >= chunkSize: x -= chunkSize;
        if y > 0: 
            while y >= chunkSize: y -= chunkSize;
        if x < 0:
            while x < 0: x += chunkSize;
        if y < 0:
            while y < 0: y += chunkSize;
    
    return (x, y);
    
def getTile (x, y, otherInfo = False) :
    
    chunkPos = getChunkPos(x, y);
    
    x = math.floor(x/tileSize);
    y = math.floor(y/tileSize);
    
    if x < 0: 
        while x < 0: x += chunkSize;
    if y < 0:
        while y < 0: y += chunkSize;
    if x > chunkSize:
        while x > chunkSize: x -= chunkSize;
    if y > chunkSize: 
        while y > chunkSize: y -= chunkSize;
        
    tileX = int(str(x)[-1]);
    tileY = int(str(y)[-1]);
    
    testChunk(chunkPos);
    tile = chunks[chunkPos][(tileX, tileY)];
    # if testChunk returns true, tile = thing
        
    data = tile[0];
    
    if otherInfo: data = tile;
    
    
    return data;

def updateCamera () :
    
    camera.offsetX = mouse.absX - sW/2;
    camera.offsetY = mouse.absY - sH/2;
    
    camera.px = camera.realX;
    camera.py = camera.realY;
    
    camera.realX -= round((camera.realX - (player.x + player.width/2) + sW/2 - camera.offsetX) / camera.smoothness);
    camera.realY -= round((camera.realY - (player.y + player.height/2) + sH/2 - camera.offsetY) / camera.smoothness);
    
    if camera.shakeTime > 0:
        camera.shakeTime -= 1;
        camera.realX += random.randint(0, int(camera.shakeStrength*2)) - camera.shakeStrength;
        camera.realY += random.randint(0, int(camera.shakeStrength*2)) - camera.shakeStrength;
        
    camera.x = round(camera.realX);
    camera.y = round(camera.realY);

grapple = Grapple();
player = Player();
mouse = Mouse();
camera = Camera();

 # nav player
def playerFrame () :
    global timeScale
    
    def updatePos():
        global timeScale;
        player.px = player.x;
        player.py = player.y;
        
        if not grapple.hooked:
            if not player.lockX: player.x += player.xv * timeScale;
            if not player.lockY: player.y += player.yv * timeScale;
        
        player.rect.x = int(player.x);
        player.rect.y = int(player.y);
        
        player.rect.width = int(player.width);
        player.rect.height = int(player.height);
    updatePos();

    def findChunksAndTiles():

        player.tilePos = getTilePos(player.x + player.width / 2, player.y);
        player.chunkPos = getChunkPos(player.x, player.y);

        player.tiles.top = False; player.tiles.bottom = False;
        player.tiles.left = False; player.tiles.right = False;

        if player.yv < 0:
            thing = 15;
        else: thing = 0;

        if not player.x == player.tilePos[0]: # player is not in a single tile

            bottomLeft = getTile(player.x + 1, player.y + player.height);
            bottomRight = getTile(player.x + player.width - 1, player.y + player.height);

            if bottomLeft or bottomRight:

                if player.state == "slide" or player.state == "crouch": slideHeight = 0;
                else: slideHeight = tileSize;

                if bottomRight and not getTile(player.x + player.width, player.y + slideHeight):
                    player.tiles.bottom = True;

                if bottomLeft and not getTile(player.x, player.y + slideHeight):
                    player.tiles.bottom = True;
            
            if getTile(player.x + abs(player.xv), player.y - 1) or getTile(player.x + player.width - abs(player.xv), player.y - 1):
                player.tiles.top = True;

        else:
            player.tiles.bottom = getTile(player.x, player.y + player.height);
            player.tiles.top = getTile(player.x, player.y -1);

        

        player.tiles.left = getTile(player.x - 1, player.y + thing);
        player.tiles.right = getTile(player.x + player.width + 1, player.y + thing);

        if not player.state == "slide" and not player.state == "crouch":
            if getTile(player.x - 1, player.y + tileSize + thing): player.tiles.left = True;
            if getTile(player.x + player.width + 1, player.y + tileSize + thing): player.tiles.right = True;
    
    
    findChunksAndTiles();
    
    left = keys[pygame.K_a];
    right = keys[pygame.K_d];
    space = keys[pygame.K_SPACE];
    up = keys[pygame.K_w];
    down = keys[pygame.K_s];
    

    def hotbarStuff():
        
        hotbarRect.x = round(sW/2 - hotbarRect.width * 3);
        hotbarRect.y = 50;

        item = player.hotbar.slotContents[player.hotbar.slot];
        
        if mouse.down and mouse.button == 1 and item != "none":
            item.use();
                
        def drawAndUpdateX(hotbarSlot):

            selectedHotbarSize = 2;

            if hotbarSlot == player.hotbar.slot:

                hotbarColor = orange;
                hotbarRect.x -= selectedHotbarSize;
                hotbarRect.width += selectedHotbarSize * 2;
                hotbarRect.y -= selectedHotbarSize;
                hotbarRect.height += selectedHotbarSize * 2;

            else:
                hotbarColor = blue;

            pygame.draw.rect(screen, hotbarColor, hotbarRect);
            
            if hotbarSlot == player.hotbar.slot:

                hotbarRect.x += selectedHotbarSize; hotbarRect.width -= selectedHotbarSize * 2;
                hotbarRect.y += selectedHotbarSize; hotbarRect.height -= selectedHotbarSize * 2;


            item = player.hotbar.slotContents[hotbarSlot];
            if item != "none":
                if useImage:
                    screen.blit(item.icon, hotbarRect);
                else:
                    x = hotbarRect.x + item.icon[0].width/2;
                    y = hotbarRect.y + item.icon[0].height/2;
                    pygame.draw.rect(screen, item.icon[1], (x, y, item.icon[0].width, item.icon[0].height));
            hotbarRect.x += hotbarRect.width + 3;
        
        for hotbarSlot in range(5):
            drawAndUpdateX(hotbarSlot); 
        
        if keys[pygame.K_1]: player.hotbar.slot = 0;
        if keys[pygame.K_2]: player.hotbar.slot = 1;
        if keys[pygame.K_3]: player.hotbar.slot = 2;
        if keys[pygame.K_4]: player.hotbar.slot = 3;
        if keys[pygame.K_5]: player.hotbar.slot = 4;

    hotbarStuff();
    def inventoryStuff():

        if keys[pygame.K_e]:
            if player.inventory["open"]: player.inventory["open"] = False;
            else: player.inventory["open"] = True;

        if player.inventory["open"]:
            hotbarRect.x = sW/2 - hotbarRect.width * 3;

            def drawInventoryAndUpdate():
                for x in range(3):
                    hotbarRect.y = sH/2 - hotbarRect.height * 3;
                    hotbarRect.x += hotbarRect.width + 3;
                    for y in range(3):
                        pygame.draw.rect(screen, blue, hotbarRect);

                        hotbarRect.y += hotbarRect.height + 3;
            drawInventoryAndUpdate();
        
        if mouse.down:

            pass
                        
        if keys[pygame.K_q]:
                if not grapple.hooked: grapple.fire();
                else: grapple.unhook();
    
    inventoryStuff();

    player.state = player.anim;
    if player.state == "slide (in)" or player.state == "slide (mid)" or player.state == "slide (out)":
        player.state = "slide";
    if player.state == "crouch" or player.state == "crouch walk":
        player.state = "crouch";
        
        
    def unstuckPlayerX () :
    
        if player.tiles.right:
            if player.xv > 0:
                player.xv = 0;
                player.x = player.tilePos[0];
            
        
        if player.xv < 0 and player.tiles.left:
            player.xv = 0;
            player.x = player.tilePos[0];
    def unstuckPlayerY ():

        if player.tiles.bottom:
            player.yv = 0;
            player.y = player.tilePos[1];

        elif not grapple.hooked:
            player.yv += gravity * timeScale;
        
        if player.tiles.top:
            if player.yv < 0:
                player.yv = 0;
    unstuckPlayerY();
    
    if grapple.fired or grapple.hooked:

        pygame.draw.line(screen, black, (player.x + player.width/2 - camera.x, player.y + player.height/2 - camera.y), (grapple.x - camera.x, grapple.y - camera.y), 5);
        
        if grapple.fired: 
            grapple.update();

        if grapple.hooked:
            
            grapple.distanceX = math.cos(math.radians(grapple.angle));
            grapple.distanceY = math.sin(math.radians(grapple.angle));

            player.x = grapple.x - grapple.distanceX * grapple.distance;
            player.y = grapple.y + grapple.distanceY * grapple.distance;
            
            if grapple.angle > 360: grapple.angle -= 360;
            if grapple.angle < 0: grapple.angle += 360;

            if not getTile(grapple.x, grapple.y):
                grapple.hooked = False;
            

            grapple.angularVel += gravity * grapple.distanceX * timeScale;

            def resetPosX():
                grapple.angularVel = 0;
                player.x = player.tilePos[0];
                grapple.distance = round(math.dist((player.x, player.y), (grapple.x, grapple.y)));
            def resetPosY(num = 0):
                player.y = player.tilePos[1] + num;
                grapple.distance = round(math.dist((player.x, player.y), (grapple.x, grapple.y)));

            if player.tiles.right and grapple.angularVel > 0:
                resetPosX();

            if player.tiles.left and grapple.angularVel < 0:
                resetPosX();

            if player.tiles.top:
                resetPosY(tileSize + 1);

            if player.tiles.bottom:
                resetPosY(-1);
            
            
            if up and grapple.distance > 3:
                grapple.distance -= 8;
            if down and grapple.distance < 300:
                grapple.distance += 8;

            if space:
                grapple.unhook();

            grapple.angle += grapple.angularVel * timeScale;
            grapple.angularVel -= grapple.angularVel / 100 * timeScale; 
            
            if left:
                if grapple.angle < 180:
                    grapple.angularVel -= grapple.strength;
                elif grapple.angle > 180:
                    grapple.angularVel += grapple.strength;
            if right:
                if grapple.angle < 180:
                    grapple.angularVel += grapple.strength;
                elif grapple.angle > 180:
                    grapple.angularVel -= grapple.strength;
        
        
    if not grapple.hooked:
        if not player.state == "slide":
            
            accel = player.accel * timeScale;
            
            # left/right movement
            if right: 
                if player.xv < player.maxXV: player.xv += accel;
            if left: 
                if player.xv > -player.maxXV: player.xv -= accel;
            
            if player.tiles.bottom:
                # jump
                if space and not down and not player.tiles.top and player.yv >= 0:
                    player.yv = player.jumpPower;
                    if player.xv > 0:
                        player.xv += player.bHopSpeed;
                    if player.xv < 0:
                        player.xv -= player.bHopSpeed;

                 # do animation checks
                if player.xv == 0:
                    player.anim = "idle";
                elif abs(player.xv) > player.maxXV / 2: 
                    player.anim = "run";
                else:
                    player.anim = "walk";
            else:
                if up:
                    # wallclimb
                    if not player.abilitesUsed["wallclimb"] and player.yv < 10:
                        if player.tiles.right or player.tiles.left:
                            player.lockX = True;
                            player.anim = "wallclimb";
                            player.abilitesUsed["wallclimb"] = True;
                            player.yv = player.jumpPower * 1.5;
                # walljump
                if player.tiles.right and space and left and player.xv > 0:
                    player.yv = player.jumpPower;
                    player.xv = player.jumpPower / 2;
                if player.tiles.left and space and right and player.xv < 0:
                    player.yv = player.jumpPower;
                    player.xv = player.jumpPower / -2;

        if down:
            if player.tiles.bottom:
                if abs(player.xv) > player.maxXV / 2 and not player.state == "slide":
                    player.anim = "slide (in)";
                    player.state = "slide";
                    player.y += player.width;
                    player.height = player.width;
        def doFriction():
            if player.tiles.bottom:
                if (not left and not right) or (left and right) or player.state == "slide":
                    # friction
                    friction = player.friction;
                    if player.state == "slide": friction *= 5;
                    player.xv -= player.xv / friction;
                    if player.xv > -0.1 and player.xv < 0.1:
                        player.xv = 0;
        doFriction();

        if player.xv > 0: player.flipH = False;
        elif player.xv < 0: player.flipH = True;

        def doSlideThings():
            if player.state == "slide":
                def unslide():
                    player.anim = "idle";
                    player.y -= player.width;
                    player.height = player.width * 2;

                if not player.tiles.bottom or player.tiles.right or player.tiles.left:
                    unslide();
                if not down:
                    if abs(player.xv) < player.maxXV / 2:
                        if not player.tiles.top:
                            unslide();
                        else:
                            player.anim = "crouch";
        doSlideThings();

        def doCrouchThings():
            if player.state == "crouch":
                if left:
                    player.x -= player.crouchSpeed;
                if right:
                    player.x += player.crouchSpeed;
        doCrouchThings();

        def doWallclimb():
            if player.state == "wallclimb" or player.state == "grab":

                def jumpOff(XV):
                    player.lockX = False;
                    player.xv = XV;
                    player.yv = player.jumpPower;
                    player.abilitesUsed["wallclimb"] = False;
                
                grabby = False;
                if player.tiles.right:

                    grabby = getTile(player.x + tileSize, player.y);
                    
                    
                    if not grabby:
                        player.yv = 0;
                        #player.anim == "grab";

                    if space:
                        if left: jumpOff(-3);
                    if right and up and not grabby:
                        player.y -= 3;
                if player.tiles.left:

                    grabby = getTile(player.x - tileSize, player.y);

                    if not grabby:
                        player.yv = 0;
                        #player.anim == "grab";

                    if space:
                        if right: jumpOff(3);
                    if left and up and not grabby:
                        player.y -= 3;


                if (not player.tiles.right and not player.tiles.left) or player.tiles.bottom:
                    player.lockX = False;
                    player.abilitesUsed["wallclimb"] = False;

        doWallclimb();

    





    unstuckPlayerX();
    
    

    def playerDebug () :
        global placeBlock, timeScale;
        bkRect = player.rect;
    
        player.rect.x -= camera.x;
        player.rect.y -= camera.y;
        
        

        pygame.draw.rect(screen, green, player.rect);
        
        if player.tiles.bottom:
            bottomRect = pygame.Rect(player.tilePos[0] - camera.x, player.tilePos[1] - camera.y + tileSize * 2, tileSize, tileSize);
            pygame.draw.rect(screen, yellow, bottomRect);
        if player.tiles.top:
            topRect = pygame.Rect(player.tilePos[0] - camera.x, player.tilePos[1] - camera.y - tileSize, tileSize, tileSize);
            pygame.draw.rect(screen, blue, topRect);
        if player.tiles.left:
            leftRect = pygame.Rect(player.tilePos[0] - camera.x - tileSize, player.tilePos[1] - camera.y, tileSize, tileSize);
            pygame.draw.rect(screen, orange, leftRect);
        if player.tiles.right:
            rightRect = pygame.Rect(player.tilePos[0] - camera.x + tileSize, player.tilePos[1] - camera.y, tileSize, tileSize);
            pygame.draw.rect(screen, red, rightRect);
        
        
        player.rect = bkRect;
            
        if keys[pygame.K_i]: timeScale = 0.1;
        if keys[pygame.K_o]: timeScale = 1.0;
        
    playerDebug();
    
    def playerTimers():
        if player.useTime > 0:
            player.useTime -= 1;
    playerTimers();

    anim = player.image[player.anim];
    
    def updateAnimation():
        if not anim["singleFrame"]:
            
            if anim["currentMidFrame"] < anim["lastMidFrame"]:
                
                anim["currentMidFrame"] += 1;
            else:
                
                anim["currentMidFrame"] = 0;
                anim["currentFrame"] += 1;
                
                if anim["currentFrame"] == anim["frames"]:
                    anim["currentFrame"] = 0;
                    if player.state == "slide":
                        if player.anim == "slide (in)":
                            player.anim = "slide (mid)";
            
            if not player.xv == 0:
                if player.anim == "walk":
                    anim["lastMidFrame"] = math.ceil(player.maxXV / 2 / abs(player.xv));
                if player.anim == "run":
                    if abs(player.xv) < player.maxXV: anim["lastMidFrame"] = math.floor(player.maxXV / abs(player.xv));
                    else: anim["lastMidFrame"] = 0;
            
                
    def animate () :
        if useImage:
            
            animRect = pygame.Rect(anim["currentFrame"] * anim["width"], 0, anim["width"], anim["height"]);
            num = 7;
            num2 = 0;
            if player.anim == "run":
                if player.xv > 0: num = -15;
                else: num = -2;
            if player.state == "slide":
                num2 = -tileSize + 3;
                num = -tileSize/2;

            image = anim["image"];

            image = pygame.Surface.subsurface(image, animRect);

            if player.flipH:
                image = pygame.transform.flip(image, True, False);
            
            tilt = -player.xv / 2;
            
            if player.flipH: tilt -= player.yv;
            else: tilt += player.yv;
            
            image = pygame.transform.rotate(image, player.angle + tilt);
            

            screen.blit(image, (round(player.x-camera.x+num), round(player.y-camera.y+3+num2)));
            
            updateAnimation();
            
        
        else:
            player.image[player.anim][0].x = int(player.x) - camera.x;
            player.image[player.anim][0].y = int(player.y) - camera.y;
            pygame.draw.rect(screen, gray, player.image[player.anim][0]);
    
    animate();
    
    
    
    if not player.lastChunkPos == player.chunkPos:
        print(player.chunkPos);
    player.lastChunkPos = player.chunkPos;
    
def groundItemsFrame(this):
    
    this.x += this.xv;
    this.y += this.yv;

    if this.xv > 0.1 or this.xv < -0.1:
        this.xv -= this.xv / 5;
    else:
        this.xv = 0;
    
    if getTile(this.x, this.y + tileSize):
        this.yv = 0;
    else:
        this.yv += gravity;

    this.rect = pygame.Rect(int(this.x), int(this.x), tileSize, tileSize);

    if this.rect.collidepoint((player.x, player.y)): 
        print("i should be unexist");
    
    pygame.draw.rect(screen, orange, (int(this.x - camera.x), int(this.y - camera.y), tileSize, tileSize));




    coord = (round(this.x - camera.x), round(this.y - camera.y));

    screen.blit(this.image, coord);




def renderTiles (chunkPos) :
    
    chunkList = [];
    chunkPosList = [];
    currentChunk = 0;
    
    for x in range(screenChunks[0] + 4):
        for y in range(screenChunks[1]):
            
            chunkX = chunkPos[0] + x - 2;
            chunkY = chunkPos[1] + y;
            
            chunkPosList.append((chunkX, chunkY));
            
            try:
                chunkList.append(chunks[(chunkX, chunkY)]);
            except:
                generateChunk((chunkX, chunkY));
                chunkList.append(chunks[(chunkX, chunkY)]);

    
    
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
                
                renderX = x - camera.x;
                renderY = y - camera.y;
                
                if screenRect.collidepoint(renderX, renderY):
                
                    if useImage: 
                        screen.blit(tileImgs[tile[0]], (renderX, renderY));
                    else: 
                        tileImgs[tile[0]][0].x = renderX;
                        tileImgs[tile[0]][0].y = renderY;
                        pygame.draw.rect(screen, tileImgs[tile[0]][1], tileImgs[tile[0]][0]);
                        
        currentChunk += 1;
              
                
                
                
running = True;
while running: # game loop

    screen.fill(skyblue);
    
    keys = pygame.key.get_pressed();
    
    mousePos = pygame.mouse.get_pos();
    mouse.absX, mouse.absY = mousePos[0], mousePos[1];
    
    mouse.x = mouse.absX + camera.x;
    mouse.y = mouse.absY + camera.y;
    
    cameraChunk = getChunkPos(int(player.x - sW/2 + camera.offsetX), int(player.y - sH/2 + camera.offsetY));
    
    renderTiles(cameraChunk);

    playerFrame();
    if len(groundItems) > 400:
        groundItems.reverse();
        groundItems.pop();
        groundItems.reverse();
    i = len(groundItems) - 1;
    while i > 0:
        item = groundItems[i];
        groundItemsFrame(item);
        i -= 1;
    
    
    
    updateCamera();
    
    test = pygame.Rect(mouse.x-camera.x, mouse.y-camera.y, 5, 5);
    pygame.draw.rect(screen, green, test);
    
    mouse.pressed = False;

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
        
            pygame.quit();
            sys.exit();
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.down = True;
            mouse.button = event.button;
            mouse.pressed = True;
        if event.type == pygame.MOUSEBUTTONUP:
            mouse.down = False;
            
                        
                
                
                 
                    

    pygame.display.update();
    clock.tick(FPS);
    

input() # stop game when it ends sometimes
