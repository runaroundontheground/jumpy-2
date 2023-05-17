import pygame, math, sys, random, os, json;


pygame.init();


keys = pygame.key.get_pressed();
keysPressed = [];
for num in range(len(keys)):
    keysPressed.append(False);

screenWidth, screenHeight = 1200, 800; # normally 600, 400

tileSize = 30;
chunks = {};
chunkSize = 10;

totalChunkSize = chunkSize * tileSize;

screenChunks = [1, 1];
 # calculate how many chunks should be on screen (width, height)
screenChunks[0] = math.ceil(screenWidth / totalChunkSize) + 1;
screenChunks[1] = math.ceil(screenHeight / totalChunkSize) + 1;

screen = pygame.display.set_mode((screenWidth, screenHeight));
screenRect = pygame.Rect(-tileSize, -tileSize, screenWidth + tileSize, screenHeight + tileSize);

clock = pygame.time.Clock();

hotbarRect = pygame.Rect(0, 0, 50, 50);

if os.path.exists("C:/jumpy 2 stuff"):
    path = "C:/jumpy 2 stuff/";
    useImage = True;
else:
    useImage = True;
    path = os.path.dirname(os.path.realpath(__file__)) + "/";


FPS = 60;
timeScale = 1.0;
gravity = 0.3; # normal 0.3

enemies = [];
projectiles = [];
groundItems = [];


animEventInt = pygame.event.custom_type();
animEvent = pygame.event.Event(animEventInt);
def setAnimTimer():
    pygame.time.set_timer(animEvent, int(1000 / FPS / timeScale));
runAnims = False;


        

black = pygame.Color("black");
red = pygame.Color("red");
orange = pygame.Color("orange");
skyblue = pygame.Color("skyblue");
green = pygame.Color("green");
brown = pygame.Color("brown");
gray = pygame.Color("gray");
yellow = pygame.Color("yellow");
blue = pygame.Color("blue");
white = pygame.Color("white");
purple = pygame.Color("purple");


    

stickAnim = {};
tileImgs = {};
toolImgs = {};
meleeImgs = {};
crackImgs = {};


def loadPlayerAnims():
    global stickAnim;

    animPath = path + "animations/player/player (no item)/";
    noArmPath = path + "animations/player/player (no arms)/";
    noRightArmPath = path + "animations/player/player (no right arm)/";
    noLeftArmPath = path + "animations/player/player (no left arm)/";
    noImage = path + "animations/unfinished/error.png";
    
    def addAnim(name, imagePath, frames = 1, midFrames = 0, singleFrame = False, scale = 0.255, repeat = True, nextAnim = "run"):
        global stickAnim;

        image = pygame.image.load(imagePath).convert_alpha();

        width = image.get_width();
        height = image.get_height();

        image = pygame.transform.scale(image, (round(width * scale), round(height * scale)))

        width = image.get_width() / frames;
        height = image.get_height();

        stickAnim[name] = {
            "image": image,
            "currentFrame": 0,
            "frames": frames,
            "currentMidFrame": 0,
            "lastMidFrame": midFrames,
            "width": width,
            "height": height,
            "singleFrame": singleFrame,
            "repeat": repeat,
            "posFix": [(0, 0), (0, 0)],
            "armPos": []
        }

        if not repeat:
            stickAnim[name]["nextAnim"] = nextAnim;
        for num in range(stickAnim[name]["frames"]):
            stickAnim[name]["armPos"].append((0, 0));

    def addPositionFix(name, pos1 = (0, 0), pos2 = (0, 0)):
        stickAnim[name]["posFix"] = [
            pos1, # when animation isn't flipped
            pos2 # when animation is flipped
        ];

    def addArmPos(name, list):
        stickAnim[name]["armPos"] = list;

    def addRun():
         # both arms
        addAnim("run", animPath + "run.png", 22, 1, scale = 0.28);
        addPositionFix("run", (0, 0), (0, 0));
         # no arms
        addAnim("run (no arms)", noArmPath + "run (no arms).png", 22, 1, scale = 0.28);
        addPositionFix("run (no arms)", (0, 0), (0, 0));
         # no right arm
        addAnim("run (no right arm)", noRightArmPath + "run (no right arm).png", 22, 1, False, 0.28);
        addPositionFix("run (no right arm)", (0, 0), (0, 0));

    def addWalk():
         # both arms
        addAnim("walk", animPath + "walk.png", 16, 1);
        addPositionFix("walk", (0, 0), (0, 0));
         # no arms
        addAnim("walk (no arms)", noArmPath + "walk (no arms).png", 16, 1);
         # no right arm
        addAnim("walk (no right arm)", noRightArmPath + "walk (no right arm).png", 16, 1);
        addPositionFix("walk (no right arm)", (0, 0), (0, 0));

    def addIdle():
         # both arms
        addAnim("idle", animPath + "idle.png", 2, FPS*2);
        addPositionFix("idle", (0, 0), (0, 0));
         # no arms
        addAnim("idle (no arms)", noArmPath + "idle (no arms).png", 2, FPS*2);
         # no right arm
        addAnim("idle (no right arm)", noRightArmPath + "idle (no right arm).png", 2, FPS * 2);
        addPositionFix("idle (no right arm)", (0, 0), (0, 0));
        addArmPos("idle (no right arm)", [(15, 22), (15, 19)]);

    def addJump():
         # both arms
        addAnim("jump", animPath + "jump.png", 19, 1, repeat = False, nextAnim = "fall", scale = 0.28);
        addPositionFix("jump", (0, 0), (0, 0));
         # no arms
        addAnim("jump (no arms)", noArmPath + "jump (no arms).png", 19, 1, repeat = False, nextAnim = "fall", scale = 0.28);
         # no right arm
        addAnim("jump (no right arm)", noRightArmPath + "jump (no right arm).png", 19, 1, repeat = False, nextAnim = "fall", scale = 0.28);
        addPositionFix("jump (no right arm)", (0, 0), (0, 0));

    def addFall():
         # both arms
        addAnim("fall", animPath + "fall.png", 16, 2, scale = 0.28);
        addPositionFix("fall", (0, 0), (0, 0));
         # no arms
        addAnim("fall (no arms)", noArmPath + "fall (no arms).png", 16, 2, scale = 0.28);
         # no right arm
        addAnim("fall (no right arm)", noRightArmPath + "fall (no right arm).png", 16, 2, scale = 0.28);
        addPositionFix("fall (no right arm)", (0, 0), (0, 0));

    def addSlide():
         # both arms
        addAnim("slide (in)", animPath + "slide (in).png", 8, 1, repeat = False, nextAnim = "slide (mid)");
        addPositionFix("slide (in)", (0, -13), (0, -13));
        addAnim("slide (mid)", animPath + "slide (mid).png", 3);
        addPositionFix("slide (mid)", (0, -1), (0, -1));
        addAnim("slide (out, stand)", animPath + "slide (out, stand).png", 8, 3, repeat = False, nextAnim = "idle");
        addPositionFix("slide (out, stand)", (0, -5), (0, -5));
        addAnim("slide (out, crouch)", animPath + "slide (out, crouch).png", 7, 4, repeat = False, nextAnim = "crouch");
        addPositionFix("slide (out, crouch)", (0, 0), (0, 0));

    def addCrouch():
         # both arms
        addAnim("crouch", animPath + "crouch.png", singleFrame = True);
        addPositionFix("crouch", (0, 0), (0, 0));
        addAnim("crouch walk", animPath + "crouch walk.png", 16, 1);
        addPositionFix("crouch walk", (0, 0), (0, 0));

    def addWallThings():
         # both arms
        addAnim("wallclimb", animPath + "wallclimb.png", 14, 4);
        addPositionFix("wallclimb", (0, 0), (0, 0));
        addAnim("wallhang", animPath + "wallhang.png", singleFrame = True);
        addPositionFix("wallhang", (0, 0), (0, 0));
        addAnim("wallhang (reach)", animPath + "wallhang (reach).png", singleFrame = True);
        addPositionFix("wallhang (reach)", (0, 0), (0, 0));
        addAnim("climb up", animPath + "climb up.png", 12);
        addPositionFix("climb up", (0, 0), (0, 0));

    def addSwing():
         # this one doesn't have a left arm
        addAnim("swing", noImage, singleFrame = True, scale = 1);
        addPositionFix("swing", (0, 0), (0, 0));
         # no arms
        # not made, don't even have the animation made at all yet

    def addRoll():
         # both arms
        addAnim("roll", animPath + "roll.png", 15, 1);
        addPositionFix("roll", (0, 0), (0, 0));

    def addAnims():
        addRun();
        addWalk();
        addIdle();
        addJump();
        addFall();
        addSlide();
        addCrouch();
        addWallThings(); # wallclimb, wallhang, walljump, climb up wall
        addSwing();
        addRoll();
        
    addAnims();

loadPlayerAnims();

def loadOtherImages():
    global tileImgs, toolImgs, meleeImgs, crackImgs;

    tilePath = path + "images/tiles/";
    toolPath = path + "images/tools/";

    tileImgs = {

    "air": 0,
    "grass": pygame.image.load(tilePath + "grass.png").convert_alpha(),
    "dirt": pygame.image.load(tilePath + "dirt.png").convert_alpha(),
    "stone": pygame.image.load(tilePath + "stone.png").convert_alpha()

    }

    toolImgs = {
        "multitool": pygame.image.load(toolPath + "multitool.png").convert_alpha(),
        "starter pick": pygame.image.load(toolPath + "starter pick.png").convert_alpha()
    };

    meleeImgs = {
        "katana": pygame.image.load(path + "images/melee/katana.png")
    }

    crackImgs = {
        "light": pygame.image.load(path + "images/cracks/light.png").convert_alpha(),
        "medium": pygame.image.load(path + "images/cracks/medium.png").convert_alpha(),
        "heavy": pygame.image.load(path + "images/cracks/heavy.png").convert_alpha()
    };


    for dict, image in crackImgs.items():
        image.fill(black, (0, 0, tileSize, tileSize), special_flags = pygame.BLEND_ADD);
loadOtherImages();

def generateChunk (chunkPos) :

    chunkData = {};
    
    for x in range(chunkSize):
        for y in range(chunkSize):
            
            
            tileX = chunkPos[0] * chunkSize + x;
            tileY = chunkPos[1] * chunkSize + y;
            
            #tileX is for adding like a beach or something once it go far enoghsiuus
            
            tileType = "air";
            tileHardness = 0;

            if tileY == chunkSize:
                tileType = "grass";
                tileHardness = 3;
            
            if tileY > chunkSize: 
                tileType = "dirt";
                tileHardness = 2; 
            
            if tileY > chunkSize * 2:
                if random.randint(1, int(100 / tileY) + 1) == 1:
                    tileType = "stone";
                    tileHardness = 6;
            

            tileData = {
                "type": tileType, 
                "hardness": tileHardness
            };
            
            chunkData[(x, y)] = tileData;
            
            
            
    
    chunks[chunkPos] = chunkData;


icons = {
    "grass": pygame.Surface.copy(tileImgs["grass"]),
    "dirt": pygame.Surface.copy(tileImgs["dirt"]),
    "stone": pygame.Surface.copy(tileImgs["stone"]),
    "multitool": pygame.Surface.copy(toolImgs["multitool"]),
    "starter pick": pygame.Surface.copy(toolImgs["starter pick"]),
    "katana": pygame.Surface.copy(meleeImgs["katana"])
};


for key, icon in icons.items():
    
    scale = 40 / icon.get_width();
    width = int(icon.get_width() * scale);
    height = int(icon.get_height() * scale);

    icon = pygame.transform.scale(icon, (width, height));
    
    scale = 40 / icon.get_height();
    width = int(icon.get_width() * scale);
    height = int(icon.get_height() * scale);
    icon = pygame.transform.scale(icon, (width, height));
    icons[key] = icon;

def rotatePoint(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center = pivot + rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

def changeAngleSmoothly(currentAngle, desiredAngle, smoothness = 10):

    """change an angle with configurable smoothness
    args:
        currentAngle: the current angle
        desiredAngle: the angle you want to smooth out to
        smoothness (optional): how smooth / slow the rotation is
    """
    angleChange = 0;
        # just to clarify, these are how many degrees away something is
        # ex. 180 degrees to 250 degrees would be 70 right, 290 left (for how far to rotate)
    angleToRight = 0;
    angleToLeft = 0;
    
    if currentAngle > desiredAngle:
        
        angleToRight = (360 - currentAngle) + desiredAngle;
        angleToLeft = currentAngle - desiredAngle;
        
    
    
    if currentAngle < desiredAngle:
        
        angleToLeft = (360 - desiredAngle) + currentAngle;
        angleToRight = desiredAngle - currentAngle;
        
    
    
    if angleToRight < angleToLeft: angleChange = angleToRight;
    if angleToLeft < angleToRight: angleChange = -angleToLeft;
    
    currentAngle += angleChange / smoothness;

    
    if currentAngle >= 360: currentAngle -= 360;
    if currentAngle < 0: currentAngle += 360;
    if abs(currentAngle) > 1000: currentAngle = 0;

    return currentAngle;

class tileItem ():
    def __init__(this, data = {"type": "grass", "hardness": 3}, itemType = "tile", holdType = "right"):
        this.data = data;
        this.icon = icons[this.data["type"]];
        this.itemType = itemType;
        this.useTime = 2;
        this.holdType = holdType;

    def use(this):
            testChunk((mouse.x, mouse.y));
            chunkPos = getChunkPos(mouse.x, mouse.y);
            tilePos = getTilePos(mouse.x, mouse.y, True);

            tile = chunks[chunkPos][tilePos];
            rectPos = getTilePos(player.x, player.y);
            noPlacementRect = pygame.Rect(rectPos[0], rectPos[1], player.width, player.height);

            if tile["type"] != "air" and tile != this.data:
                otherTilePos = getTilePos(mouse.x, mouse.y);
                x = otherTilePos[0];
                y = otherTilePos[1];

                totalBreakProgress = player.breakProgress / tile["hardness"];
                pos = (int(x - camera.x), int(y - camera.y));
                
                if totalBreakProgress > 0.66:
                    screen.blit(crackImgs["heavy"], pos);
                elif totalBreakProgress > 0.33:
                    screen.blit(crackImgs["medium"], pos);
                else:
                    screen.blit(crackImgs["light"], pos);
                
                if player.timers["useTime"] == 0:
                    player.breakProgress += player.breakPower;
                    player.timers["useTime"] = player.timers["toolUseTime"];

                    if tile["type"] == "grass":
                        chunks[chunkPos][tilePos] = {"type": "dirt", "hardness": 2};
                    
                    if player.breakProgress >= tile["hardness"]:
                        spawnItem(xv = random.randint(-5, 5), yv = random.randint(-5, 5), x = otherTilePos[0], y = otherTilePos[1], id = tile["type"]);
                        chunks[chunkPos][tilePos] = this.data;
                        player.breakProgress = 0;
                        player.breakingTilePos = "none";


            if player.x > rectPos[0]:
                noPlacementRect.width += tileSize;
                
            if not noPlacementRect.collidepoint(mouse.x, mouse.y):
                
                tileOnLeft = getTile(mouse.x - tileSize, mouse.y);
                tileOnRight = getTile(mouse.x + tileSize, mouse.y);
                tileOnTop  = getTile(mouse.x, mouse.y - tileSize);
                tileOnBottom = getTile(mouse.x, mouse.y + tileSize);
                allowPlace = False;

                if tileOnLeft or tileOnRight or tileOnTop or tileOnBottom:
                    allowPlace = True;

                if allowPlace:
                    if tile["type"] == "air":
                        chunks[chunkPos][tilePos] = this.data;

    def handRender(this):
        pos = (int(player.x - camera.x), int(player.y - camera.y));
        screen.blit(this.icon, pos);

class toolItem ():
    def __init__(this, breakType = "all", breakPower = 0.5, useTime = 5, icon = "multitool", itemType = "tool", holdType = "right"):

        this.breakType = breakType;
        this.breakPower = breakPower;
        this.useTime = useTime;
        this.swingTime = 15;
        this.icon = icons[icon];
        this.itemType = itemType;
        this.holdType = holdType;
        this.angle = 0;
        this.rotateDir = "right";
        this.range = 5*tileSize;

    def use(this):
        # so here's how we fix:
        """
        make a new transparent surface
        blit arm and item onto it
        rotate
        render
        yay
        """
        def swing():
            
            
            

            toolImg = pygame.Surface.copy(this.icon);
            armImg = pygame.Surface.copy(player.rightArm);

            def doAngle():
                if player.timers["swingTime"] == 0:
                    dx = player.x - mouse.x;
                    dy = player.y - mouse.y;    
                    this.angle = round(math.degrees(math.atan2(-dy, dx)));
                    this.angle -= this.swingTime * 15;
                    player.timers["swingTime"] = int(this.swingTime / timeScale);
                else:
                    this.angle -= 15 * timeScale;
            doAngle();
            
            armAndToolSurf = pygame.Surface([armImg.get_width() + toolImg.get_width(), armImg.get_height() + toolImg.get_height()*1.2], pygame.SRCALPHA);

            armAndToolSurf.blit(armImg, (0, toolImg.get_height()/2.5));
            armAndToolSurf.blit(toolImg, (armImg.get_width() - 13, toolImg.get_height()/2.5 - 8));

            armAndToolSurf = pygame.transform.flip(armAndToolSurf, False, True);
            
            pos = [int(player.x - camera.x), int(player.y - camera.y)];
            pos[0] += player.armPos[0];
            pos[1] += player.armPos[1];
           
            pygame.draw.rect(screen, yellow, (pos[0], pos[1], 5, 5))
            
            offset = [10, 10];

            armAndToolSurf, rect = rotatePoint(armAndToolSurf, this.angle, pos, pygame.math.Vector2(offset));
            
            screen.blit(armAndToolSurf, rect);
            
            

        
        if mouse.button == 1:
            print(player.breakProgress);
            swing();
            testChunk((mouse.x, mouse.y));

            chunkPos = getChunkPos(mouse.x, mouse.y);
            tilePos = getTilePos(mouse.x, mouse.y, True);

            if player.breakingTilePos == "none":
                player.breakingTilePos = getTilePos(mouse.x, mouse.y);
                player.breakProgress = 0;
            
            if player.breakingTilePos != getTilePos(mouse.x, mouse.y):
                player.breakingTilePos = "none";
                player.breakProgress = 0;

            tile = chunks[chunkPos][tilePos];

            if tile["type"] != "air":
                otherTilePos = getTilePos(mouse.x, mouse.y);
                x = otherTilePos[0];
                y = otherTilePos[1];

                if math.dist((player.x, player.y), (mouse.x, mouse.y)) < this.range:
                    
                
                    totalBreakProgress = player.breakProgress / tile["hardness"];
                    pos = (int(x - camera.x), int(y - camera.y));
                    
                    if totalBreakProgress > 0.66:
                        screen.blit(crackImgs["heavy"], pos);
                    elif totalBreakProgress > 0.33:
                        screen.blit(crackImgs["medium"], pos);
                    else:
                        screen.blit(crackImgs["light"], pos);
                    
                    if player.timers["useTime"] == 0:
                        player.breakProgress += this.breakPower;
                        

                        if tile["type"] == "grass":
                            chunks[chunkPos][tilePos] = {"type": "dirt", "hardness": 2};
                        
                        if player.breakProgress >= tile["hardness"]:
                            spawnItem(xv = random.randint(-5, 5), yv = random.randint(-5, 5), x = otherTilePos[0], y = otherTilePos[1], id = tile["type"]);
                            chunks[chunkPos][tilePos] = {"type": "air", "hardness": 0};
                            player.breakProgress = 0;
                            player.breakingTilePos = "none";
            if player.timers["useTime"] == 0:
                player.timers["useTime"] = int(this.useTime / timeScale);

    def handRender(this):

        newImage = pygame.Surface.copy(this.icon);

        pos = [int(player.x - camera.x), int(player.y - camera.y)];
        
        toolPos = pos.copy();        
        if not player.flipH:
            toolPos[0] += newImage.get_width() - 10;
            if this.angle > 200 or this.angle < 160:
                this.angle = 180;
            else:
                if this.angle > 190:
                    this.rotateDir = "left";
                if this.angle < 170:
                    this.rotateDir = "right";

                if this.rotateDir == "right":
                    this.angle += player.xv / 5;
                if this.rotateDir == "left":
                    this.angle -= player.xv / 5;
        else:
            if this.angle > 200 or this.angle < 160:
                this.angle = 180;
            else:
                if this.angle > 190:
                    this.rotateDir = "left";
                if this.angle < 170:
                    this.rotateDir = "right";

                if this.rotateDir == "right":
                    this.angle -= player.xv / 5;
                if this.rotateDir == "left":
                    this.angle += player.xv / 5;

        if player.flipH:
                newImage = pygame.transform.flip(newImage, True, False);

        
        offset = [0, 0];
        forward = 20;
     

        toolPos[0] -= math.cos(math.radians(this.angle)) * forward + 15;
        toolPos[1] += math.sin(math.radians(this.angle)) * forward + 35;


        armImg = pygame.Surface.copy(player.rightArm);
        armPos = [pos[0] + player.width/2, pos[1] + player.height/3];
        
        armImg, armRect = rotatePoint(armImg, -this.angle + 90, armPos, pygame.math.Vector2(-10, 3));

       
        
        newImage, rect = rotatePoint(newImage, -this.angle + 230, toolPos, pygame.math.Vector2(offset));
        
        screen.blit(newImage, rect);
        screen.blit(armImg, armRect);

class meleeItem ():
    def __init__(this, damage = 3, attackRange = 2, icon = "katana", imgPath = path + "animations/player/melee/katana (in hand).png", itemType = "melee",
            holdType = "both"):
        this.damage = damage;
        this.attackRange = attackRange;
        this.attackAngle = 90;
        this.icon = icons[icon];
        this.image = pygame.image.load(imgPath);
        this.itemType = itemType;
        this.angle = 0;
        scale = 3;
        this.image = pygame.transform.scale(this.image, (int(this.image.get_width() / scale), int(this.image.get_height() / scale)));
        this.holdType = holdType;
        
        this.animData = {
            "frames": 11,
            "currentFrame": 0,
            "midFrames": 3,
            "currentMidFrame": 0,
            "width": this.image.get_width() / 11,
            "height": this.image.get_height()
        }
        
    def updateThings(this, drawRect):

        pos = [int(player.x - camera.x + 13), int(player.y - camera.y + 20)];

        dx = player.x - mouse.x;
        dy = player.y - mouse.y;

        desiredAngle = round(math.degrees(math.atan2(-dy, dx)));
        
        
        this.angle = changeAngleSmoothly(this.angle, desiredAngle);
        
        if this.angle < 90 or this.angle > 270: player.flipH = True; flipV = False;
        else: player.flipH = False; flipV = True;
        
        newImage = pygame.Surface.subsurface(this.image, drawRect);
        
        flipV == this.angle < 90 and this.angle > -90;
        newImage = pygame.transform.flip(newImage, True, flipV);
        offset = [-8.5, -12];
        if not flipV:
            offset[0] += 3;
            offset[1] += 25;
        if player.state == "run":
            if player.flipH:
                pos[0] -= 5;

        newImage, rect = rotatePoint(newImage, -this.angle, pygame.math.Vector2(pos[0], pos[1]), pygame.math.Vector2(offset[0], offset[1]));
        pygame.draw.rect(screen, white, (pos[0], pos[1], 5, 5));
        return newImage, rect, pos;
    
    def use(this):
       

        x = int(this.animData["width"] * this.animData["currentFrame"]);
       
        drawRect = (x, 0, this.animData["width"], this.animData["height"]);

        newImage, rect, pos = this.updateThings(drawRect);
        
        
        this.animData["currentMidFrame"] += 1;

        if this.animData["currentMidFrame"] >= this.animData["midFrames"]:
            this.animData["currentFrame"] += 1;
            this.animData["currentMidFrame"] = 0;
            if this.animData["currentFrame"] >= this.animData["frames"]:
                this.animData["currentFrame"] = 0;

        screen.blit(newImage, rect);      

    def handRender(this):
        
        
        drawRect = (this.animData["width"] * this.animData["currentFrame"], 0, this.animData["width"], this.animData["height"]);
        newImage, rect, pos = this.updateThings(drawRect);
        

        if this.animData["currentFrame"] != 0:
            if this.animData["currentFrame"] < this.animData["frames"]:
                if this.animData["currentMidFrame"] < this.animData["midFrames"]: this.animData["currentMidFrame"] += 1;

            if this.animData["currentMidFrame"] >= this.animData["midFrames"]:
                this.animData["currentMidFrame"] = 0;
                this.animData["currentFrame"] += 1;

            if this.animData["currentFrame"] >= this.animData["frames"]:
                this.animData["currentFrame"] = 0;
        
        
        
        screen.blit(newImage, rect);
        
class rangedItem (): # NOT DONE! or even started
    def __init__(this, damage = 3):
        pass

items = {
    "grass": tileItem({"type": "grass", "hardness": 3}),
    "dirt": tileItem({"type": "dirt", "hardness": 2}),
    "stone": tileItem({"type": "stone", "hardness": 6}),
    
    "multitool": toolItem("all", 0.5, 5, "multitool"),
    "epic sword": meleeItem(5, 2),
    "starter pick": toolItem("not wood", 0.5, 5, "starter pick")
    #"crappy axe": toolItem("wood", 0.5, 5, "crappy axe")
}

class Mouse:
    def __init__(mouse):
        
        mouse.absX = 0;
        mouse.absY = 0;
        mouse.x = 0;
        mouse.y = 0;
        mouse.down = False;
        mouse.button = 1;
        mouse.pressed = False;
        mouse.pos = (0, 0);

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
        this.contents = {
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
        this.meleeRect = pygame.Rect(0, 0, 0, 0);
        this.allowDebugRects = False;
        this.itemSuckRect = (0, 0, 0, 0);
        
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
        this.fakeAngle = 0; # use this to fix rolling
        this.bHopSpeed = 0.5; # normal 0.5
        this.airTime = 0;

        this.rollDir = "right";
        this.rollAngleSpeed = 15;
        
        this.abilityToggles = {
            "slide": True,
            "doubleJump": False,
            "wallclimb": True,
            "hook": True
        };

        this.abilitesUsed = {
            "wallclimb": False,
            "doubleJump": False
        };

        this.width = tileSize;
        this.height = tileSize * 2;
        this.flipH = False;

        this.anim = "idle";
        this.state = "idle";
        this.hideArm = "none";  

        this.image = stickAnim;

        this.rightArm = pygame.image.load(path + "animations/player/right arm.png").convert_alpha();
        this.leftArm = pygame.image.load(path + "animations/player/left arm.png").convert_alpha();
        scale = 0.35;
        this.rightArm = pygame.transform.scale_by(this.rightArm, scale);
        this.leftArm = pygame.transform.scale_by(this.leftArm, scale);
        this.armPos = (0, 0);
        
        this.hotbar = Hotbar();

        this.hotbar.contents[3] = items["dirt"];
        this.hotbar.contents[1] = items["starter pick"];
        this.hotbar.contents[2] = items["stone"];
        this.hotbar.contents[0] = items["epic sword"];
       

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

        this.timers = {
            "useTime": 0,
            "swingTime": 0,
            "toolUseTime": 5,
            "rollCD": 0
        }

        this.breakingTilePos = 0; # will be "getTile" later
        this.breakPower = 0;
        this.breakProgress = 0;
        


class Grapple () :
    def __init__(this):
        this.x = 0;
        this.y = 0;
        
        this.px = 0;
        this.py = 0;
        
        this.distance = 0;
        this.distanceX = 0;
        this.distanceY = 0;
        
        this.xv = 0; # normal 0
        this.yv = 0; # normal 0
        this.angularVel = 0; # normal 0
        this.angle = 0; # normal 0
        this.strength = 0.05; # normal 0.05
        this.launchVel = 20;# normal 20
        
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
    def __init__(this, x = 0, y = 0, xv = 0, yv = 0, id = "dirt"):

        this.x = x;
        this.y = y;

        this.xv = xv;
        this.yv = yv;

        this.data = items[id];

        
        this.image = this.data.icon;
        this.image = pygame.transform.scale(this.image, (20, 20));
        this.rect = pygame.Rect(0, 0, 20, 20);

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


    if tile["type"] == "air": data = False;
    else: data = True;

    if otherInfo: data = tile;
    
    return data;

def updateCamera () :
    
    camera.offsetX = mouse.absX - screenWidth/2;
    camera.offsetY = mouse.absY - screenHeight/2;
    
    camera.px = camera.realX;
    camera.py = camera.realY;
    
    camera.realX -= round((camera.realX - (player.x + player.width/2) + screenWidth/2 - camera.offsetX) / camera.smoothness);
    camera.realY -= round((camera.realY - (player.y + player.height/2) + screenHeight/2 - camera.offsetY) / camera.smoothness);
    
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
    global timeScale, useAnim;

    previousAnim = player.anim;
    
    def updatePos():
        global timeScale;
        player.px = player.x;
        player.py = player.y;
        
        if not grapple.hooked:
            if not player.lockX: player.x += player.xv * timeScale;
            if not player.lockY: player.y += player.yv * timeScale;
        
        player.rect.x = int(player.x);
        player.rect.y = int(player.y);

        player.meleeRect.x = player.rect.x;
        player.meleeRect.y = player.rect.y;
        
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
        
        hotbarRect.x = round(screenWidth/2 - hotbarRect.width * 3);
        hotbarRect.y = 50;

        item = player.hotbar.contents[player.hotbar.slot];

        if item != "none":
            
            if mouse.down and mouse.button == 1:
                item.use();
            else:
                item.handRender();
            
                
        def drawAndUpdateX(hotbarSlot):
            
            selectedHotbarSize = 2;

            if hotbarSlot == player.hotbar.slot:
                item = player.hotbar.contents[player.hotbar.slot];
                if item != "none":
                    player.hideArm = item.holdType;
                else:
                    player.hideArm = "none";
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


            item = player.hotbar.contents[hotbarSlot];

            if item != "none":
                
                screen.blit(item.icon, hotbarRect);
                
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

        for slot, item in player.inventory.items():
            if item != "none" and slot != "open":
                if item.itemType == "tool":
                    if item.breakType == "all" or "not wood": 
                        player.breakPower = item.breakPower;
                        player.timers["toolUseTime"] = item.useTime;
                    break;
        for slot, item in player.hotbar.contents.items():
            if item != "none":
                if item.itemType == "tool":
                    if item.breakType == "all" or "not wood":
                        player.breakPower = item.breakPower;
                        player.timers["toolUseTime"] = item.useTime;
                    break;


        if keys[pygame.K_e]:
            if player.inventory["open"]: player.inventory["open"] = False;
            else: player.inventory["open"] = True;

        if player.inventory["open"]:
            hotbarRect.x = screenWidth/2 - hotbarRect.width * 3;

            def drawInventoryAndUpdate():
                for x in range(3):
                    hotbarRect.y = screenHeight/2 - hotbarRect.height * 3;
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
            player.airTime = 0;
            player.abilitesUsed["doubleJump"] = False;

        elif not grapple.hooked:
            player.yv += gravity * timeScale;
            player.airTime += timeScale;
        
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
        if player.state != "slide" and player.state != "crouch" and player.state != "wallclimb":
            
            accel = player.accel * timeScale;
            
            # left/right movement
            if right: 
                if player.xv < player.maxXV: player.xv += accel;
            if left: 
                if player.xv > -player.maxXV: player.xv -= accel;
            
            if keys[pygame.K_LCTRL] and player.state != "roll" and player.timers["rollCD"] == 0:

                player.state = "roll";
                player.anim = "roll";
                player.fakeAngle = 0;

                if right:
                    player.rollDir = "right";

                if left:
                    player.rollDir = "left";


                if player.xv == 0:

                    if player.flipH:
                        player.rollDir = "left";
                    else: 
                        player.rollDir = "right";


            # roll
            if player.state == "roll":
                if player.rollDir == "right":
                    player.xv = player.maxXV;
                    player.fakeAngle -= player.rollAngleSpeed * timeScale;
                if player.rollDir == "left":
                    player.xv = -player.maxXV;
                    player.fakeAngle += player.rollAngleSpeed * timeScale;

                if abs(player.fakeAngle) >= 450:
                    player.timers["rollCD"] = FPS * 0.5;
                    player.state = "idle";
                    if player.tiles.bottom:
                        player.anim = "idle";
                    else:
                        player.anim = "fall";
                    player.fakeAngle = 0;


            if (player.airTime < 5 and player.yv >= 0) or (not player.abilitesUsed["doubleJump"] and player.abilityToggles["doubleJump"]) and player.state != "roll":
                # jump
                if space and not down and not player.tiles.top:
                    
                    
                    if player.tiles.bottom:
                        player.yv = player.jumpPower;
                        player.anim = "jump";
                        player.image[player.anim]["currentFrame"] = 0;

                        if player.xv > 0:
                            player.xv += player.bHopSpeed;
                        if player.xv < 0:
                            player.xv -= player.bHopSpeed;

                    if not player.tiles.bottom and player.yv > player.jumpPower/5:
                        player.yv = player.jumpPower;
                        player.anim = "jump";
                        player.image[player.anim]["currentFrame"] = 0;
                        
                        player.abilitesUsed["doubleJump"] = True;
                        
                
            if player.tiles.bottom and player.yv == 0:

                # do animation checks
                if player.state != "roll":
                    if player.xv == 0:
                        player.anim = "idle";
                        player.state = player.anim;
                    elif abs(player.xv) > player.maxXV / 2: 
                        player.anim = "run";
                        player.state = player.anim;
                    else:
                        player.anim = "walk";
                        player.state = player.anim;
            else:
                if up:
                    # wallclimb
                    if not player.abilitesUsed["wallclimb"] and player.yv < 10:
                        if player.tiles.right or player.tiles.left:
                            player.lockX = True;
                            player.anim = "wallclimb";
                            player.state = "wallclimb";
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
                if abs(player.xv) > player.maxXV / 1.1:
                    if player.state != "slide":
                        player.anim = "slide (in)";
                        player.state = "slide";
                        player.y += player.width;
                        player.height = player.width;
                elif abs(player.xv) < player.maxXV / 5:
                    if player.state != "crouch":
                        player.state = "crouch";
                        player.anim = "crouch";
                        player.height /= 2;
                        player.y += player.height;
                    
                

        def doFriction():
            if player.tiles.bottom:
                if (not left and not right) or (left and right) or player.state == "slide" or abs(player.xv) > player.maxXV:
                    # friction
                    friction = player.friction;
                    if player.state == "slide": friction *= 5;
                    player.xv -= player.xv / friction * timeScale;
                    if player.xv > -0.1 and player.xv < 0.1:
                        player.xv = 0;
        doFriction();

        def doSlideThings():
            if player.state == "slide":
                def unslide():
                    if not player.tiles.top:
                        player.anim = "idle";
                        player.state = player.anim;
                        player.y -= player.width;
                        player.height = player.width * 2;

                if not player.tiles.bottom or player.tiles.right or player.tiles.left:
                    unslide();
                
                if abs(player.xv) < player.maxXV / 1.3:
                    if player.tiles.top:
                        player.anim = "slide (out, crouch)";
                    else:
                        player.anim = "slide (out, stand)";
                if abs(player.xv) < player.maxXV / 2:
                    if not player.tiles.top:
                        unslide();
                    elif player.tiles.top:
                        player.anim = "crouch";
                        player.state = player.anim;
        doSlideThings();

        def doCrouchThings():
            if player.state == "crouch":

                def uncrouch():    
                    player.anim = "idle";
                    player.state = "idle";
                    player.height = tileSize * 2;
                    player.y -= tileSize;
                
                player.xv = 0;
                player.anim = "crouch";

                if left or right:
                    player.anim = "crouch walk";

                    if left:
                        player.x -= 3 * timeScale;
                        player.flipH = True;
                        if player.tiles.left:
                            player.x = player.tilePos[0];

                    if right:
                        player.x += 3 * timeScale;
                        player.flipH = False;
                        if player.tiles.right:
                            player.x = player.tilePos[0];

                if not player.tiles.top and not down:
                    uncrouch()        
        doCrouchThings();
        
        def doWallclimb():
            if player.state == "wallclimb" or player.state == "climb up":

                def jumpOff(XV, YV = player.jumpPower):
                    player.lockX = False;
                    player.xv = XV;
                    player.yv = YV;
                    player.abilitesUsed["wallclimb"] = False;
                    player.state = "run";
                    if YV != player.jumpPower: player.anim = "jump";
                    player.angle = 0;

                unstuckPlayerX();
                if player.yv > 5: 
                    player.anim = "fall";
                    jumpOff(0, player.yv);

                
                
                grabby = False;
                
                if player.tiles.right:

                    
                    if not getTile(player.x + tileSize, player.y) and not player.tiles.top:
                        grabby = True;

                    pygame.draw.rect(screen, white, (player.tilePos[0] + player.xv + tileSize - camera.x, player.tilePos[1] - camera.y, tileSize, tileSize))
                    player.flipH = False;
                    
                    if grabby:
                        player.yv = 0;
                        if player.state != "climb up":
                            player.anim = "wallhang";
                            

                            if left: 
                                player.anim = "wallhang (reach)";

                    if space:
                        if left: jumpOff(-3);
                    if right and up and grabby:
                        player.anim = "climb up";
                        player.state = "climb up";

                if player.tiles.left:
                    pygame.draw.rect(screen, white, (player.tilePos[0] + player.xv - tileSize - camera.x, player.tilePos[1] - camera.y, tileSize, tileSize))
                    if not getTile(player.tilePos[0] - tileSize + player.xv, player.tilePos[1]) and not player.tiles.top:
                        grabby = True;

                    player.flipH = True;
                    
                    if grabby:
                        player.yv = 0;
                        if player.state != "climb up":
                            player.anim = "wallhang";
                            

                            if right:
                                player.anim = "wallhang (reach)";

                    if space:
                        if right: jumpOff(3);
                    if left and up and grabby:
                        player.anim = "climb up";
                        player.state = "climb up";
                
                        

                if player.state == "climb up" and not player.tiles.top:
                    if player.timers["climb up"] == 0:
                        player.y -= 3;
                        if player.tiles.right:
                            player.angle -= 3;
                        if player.tiles.left:
                            player.angle += 3;
                    else:
                        player.angle = 0;
                        

                if (not player.tiles.right and not player.tiles.left) or player.tiles.bottom:
                    player.lockX = False;
                    player.abilitesUsed["wallclimb"] = False;
                    player.anim = "idle"; player.state = "idle";
                    player.angle = 0;
        doWallclimb();


    if player.anim != "climb up": unstuckPlayerX();
    
    def playerDebug () :
        global timeScale;
        

        player.rect.x -= camera.x;
        player.rect.y -= camera.y;
        
        if player.allowDebugRects:

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
        
        
        player.rect.x += camera.x;
        player.rect.y += camera.y;
            
        if keys[pygame.K_i]: timeScale = 0.1;
        if keys[pygame.K_o]: timeScale = 1.0;
        if keys[pygame.K_h]: timeScale = 0.0;
        if keys[pygame.K_g]: player.allowDebugRects = True;
        if keys[pygame.K_h]: player.allowDebugRects = False;
        

    playerDebug();
    
    def playerTimers():
        for key, timer in player.timers.items():
            if timer > 0:
                timer -= 1;
    playerTimers();
    
    if player.hideArm == "both":
        try:
            player.image[player.anim + " (no arms)"];
        except:
            pass;
        else:
            player.anim += " (no arms)";
    
    if player.hideArm == "right":
        try:
            player.image[player.anim + " (no right arm)"];
        except:
            pass;
        else:
            player.anim += " (no right arm)";

    anim = player.image[player.anim];

    if player.state != "wallclimb" and player.state != "wallhang" and player.state != "roll":
        if mouse.x > player.x: player.flipH = False;
        elif mouse.x < player.x: player.flipH = True;
    
    def updateAnimation():

        player.armPos = anim["armPos"][anim["currentFrame"]];
        

        if not anim["singleFrame"]:

            playInReverse = False;

            if player.xv > 0:
                if player.flipH:
                    playInReverse = True;
            elif player.xv < 0:
                if not player.flipH:
                    playInReverse = True;

        
            if previousAnim != player.anim:
                if playInReverse:
                    anim["currentFrame"] = anim["frames"] - 1;
                else:
                    anim["currentFrame"] = 0;


            if anim["currentMidFrame"] < anim["lastMidFrame"]:
                
                anim["currentMidFrame"] += 1;
            else:
                if playInReverse:
                    anim["currentMidFrame"] = 0;
                    anim["currentFrame"] -= 1;
                
                    if anim["currentFrame"] <= 0:
                        anim["currentFrame"] = anim["frames"] - 1;
                        if not anim["repeat"]:
                            player.anim = anim["nextAnim"];
                            player.image[player.anim]["currentFrame"] = player.image[player.anim]["frames"] - 1;
                        
                else:
                    anim["currentMidFrame"] = 0;
                    anim["currentFrame"] += 1;
                    
                    if anim["currentFrame"] >= anim["frames"]:
                        anim["currentFrame"] = 0;
                        if not anim["repeat"]:
                            player.anim = anim["nextAnim"];
            
            if player.xv != 0:
                if player.anim == "walk":
                    anim["lastMidFrame"] = math.ceil(player.maxXV / 2 / abs(player.xv));
    
                
    def animate () :
        animRect = pygame.Rect(anim["currentFrame"] * anim["width"], 0, anim["width"], anim["height"]);

        image = anim["image"];
        image = pygame.Surface.subsurface(image, animRect);
        image = pygame.transform.flip(image, player.flipH, False);
        
        tilt = -player.xv / 2;
        
        if player.flipH: tilt -= player.yv;
        else: tilt += player.yv;

        index = 0;
        if player.flipH:
            index = 1;

        x = player.x + player.width/2 - camera.x;
        y = player.y + player.height/2 - camera.y;

        x += anim["posFix"][index][0];
        y += anim["posFix"][index][1];

        pivot = [x, y];
        offset = pygame.math.Vector2(0, 0);

        image, rect = rotatePoint(image, -(player.angle + tilt), pivot, offset);
        
        

        screen.blit(image, rect);
        screen.blit(image, (0, 0));
        
        if runAnims:
            updateAnimation();
    
        
    animate();
    
    
    if not player.lastChunkPos == player.chunkPos:
        print(player.chunkPos);
    player.lastChunkPos = player.chunkPos;
    
def groundItemsFrame(this):
    
    this.x += this.xv;
    this.y += this.yv;

    this.rect.x = int(this.x);
    this.rect.y = int(this.y);

    if this.xv > 0.1 or this.xv < -0.1:
        this.xv -= this.xv / 5;
    else:
        this.xv = 0;
    
    if getTile(this.x, this.y + tileSize):
        this.yv = 0;
    else:
        this.yv += gravity;
    
    # REMOVE LATER!!!
    speed = 5;
    if this.x < player.x:
        this.x += speed;
    if this.x > player.x:
        this.x -= speed;
    if this.y > player.y:
        this.y -= speed;


    if this.rect.colliderect(player.rect): 
        groundItems.remove(this);


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
            if tile["type"] != "air":
                
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
                
                #if screenRect.collidepoint(renderX, renderY):
                # hey this doesn't need to be here? probably?        
                screen.blit(tileImgs[tile["type"]], (renderX, renderY));
                    
                        
        currentChunk += 1;
              
                
                
                
running = True;
setAnimTimer();
while running: # game loop
    tempKeys = pygame.key.get_pressed();
    
    for num in range(len(tempKeys)):
        if not keys[num] and not keysPressed[num]:
            keysPressed[num] = True;

    keys = pygame.key.get_pressed();
    
    if timeScale > 0:
        screen.fill(skyblue);
        
        
        
        mousePos = pygame.mouse.get_pos();
        mouse.absX, mouse.absY = mousePos[0], mousePos[1];
        
        mouse.x = mouse.absX + camera.x;
        mouse.y = mouse.absY + camera.y;
        mouse.pos = (mouse.x, mouse.y);
        
        cameraChunk = getChunkPos(camera.x, camera.y);
        
        renderTiles(cameraChunk);

        playerFrame();
        if len(groundItems) > 400:
            groundItems.remove(0);
        i = len(groundItems) - 1;
        while i > -1:
            item = groundItems[i];
            groundItemsFrame(item);
            i -= 1;
        
        
        updateCamera();
        
        test = pygame.Rect(mouse.x-camera.x, mouse.y-camera.y, 5, 5);
        pygame.draw.rect(screen, green, test);
        
        mouse.pressed = False;
        runAnims = False;
    else:
        if keys[pygame.K_l]: timeScale = 1.0; setAnimTimer();
        if keys[pygame.K_m]:
            mousePos = pygame.mouse.get_pos();
            mouse.absX, mouse.absY = mousePos[0], mousePos[1];

            img = player.image[player.anim]["image"];
            x = mouse.absX;
            y = mouse.absY;
            print(str(x) + ", " + str(y));
            
            print(player.image[player.anim]["currentFrame"]);
            player.armPos = (x, y);
            pos = [int(player.x - camera.x), int(player.y - camera.y)];
            pos[0] += player.armPos[0];
            pos[1] += player.armPos[1];
           
            pygame.draw.rect(screen, yellow, (pos[0], pos[1], 5, 5))
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
        if event.type == pygame.MOUSEWHEEL:
            player.hotbar.slot -= event.y;
            if player.hotbar.slot <= -1:
                player.hotbar.slot = 0;
            if player.hotbar.slot >= 5:
                player.hotbar.slot = 4;

        if event.type == animEventInt and timeScale > 0:
            
            runAnims = True;
            pygame.time.set_timer(animEventInt, abs(int(1000 / FPS / timeScale) - 5));
            
    
    for num in range(len(keysPressed)):
        keysPressed[num] = False;
    
                 
    
    
    pygame.display.flip();
    clock.tick(FPS);
    

input() # stop game when it ends sometimes
