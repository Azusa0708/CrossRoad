import pgzrun
import random
import time

WIDTH = 800
HEIGHT = 1000
CARNUM = 8              #车数量
SPEEDMIN = 3
SPEEDMAX = 4
SCORE = 8           #分数
FINALSCORE = 0
HEART = 3           #生命
Isblowup = 0
Isshield = 0
healboxflag = 0
shieldsflag = 0
fasterflag = 0
bananaflag = 0
game_start = 0

player_x = WIDTH/2
player_y = HEIGHT
list = []       #车列表
toollist = []   #道具列表

background = Actor('bk')  #背景
title = Actor('title')
title.pos = WIDTH/2,250
background.pos = WIDTH/2,HEIGHT/2

heartimage0 = Actor('heart')
heartimage1 = Actor('heart')
heartimage2 = Actor('heart')
heartimage0.pos = 650,20
heartimage1.pos = 710,20
heartimage2.pos = 770,20
heart = [heartimage0,heartimage1,heartimage2]
start_button = Actor('start_button')
go_home_button = Actor('go_home')
start_button.pos = 400,700
go_home_button.pos = 400,650
finalscore = Actor('finalscore')
finalscore.pos = WIDTH/2,180
road = Actor('road')
road.pos = WIDTH/2,HEIGHT/2
protect = Actor('circle')

playerimages = [Actor('l1'),Actor('l2'),Actor('l3'),
          Actor('r1'),Actor('r2'),Actor('r3'),
          Actor('d1'),Actor('d2'),Actor('d3'),
          Actor('u1'),Actor('u2'),Actor('u3')]      #操作行人

blowup = Actor('blowup')

numAnims = len(playerimages)

for i in range(numAnims):
    playerimages[i].x = player_x
    playerimages[i].y = player_y

#玩家类
class player:
    def __init__(self,images,player_x,player_y):
        self.actor = images
        self.player_x = player_x
        self.player_y = player_y
        self.life = HEART
        self.animIndex = 9
        self.speed = 5
        self.animSpeed = 0
        self.image = images[0]
        self.blowup = blowup

    def draw(self):
        self.image = self.actor[self.animIndex]
        self.image.draw()
        if Isblowup == 1:
            self.blowup.draw()
    def update(self):
        if keyboard.left:
            self.player_x -= self.speed
            for i in range(numAnims):
                self.actor[i].x = self.player_x
                if self.player_x <= 0:
                    self.player_x = 0
            self.animSpeed += 1
            if self.animSpeed % 5 == 0:
                self.animIndex += 1
                if self.animIndex > 2:
                    self.animIndex = 0
        if keyboard.right:
            self.player_x += self.speed
            for i in range(numAnims):
                self.actor[i].x = self.player_x
                if self.player_x >= WIDTH:
                    self.player_x = WIDTH
            self.animSpeed += 1
            if self.animSpeed % 5 == 0:
                self.animIndex += 1
                if self.animIndex < 3 or self.animIndex > 5:
                    self.animIndex = 3
        if keyboard.down:
            self.player_y += self.speed
            for i in range(numAnims):
                self.actor[i].y = self.player_y
                if self.player_y >= HEIGHT:
                    self.player_y = HEIGHT
            self.animSpeed += 1
            if self.animSpeed % 5 == 0:
                self.animIndex += 1
                if self.animIndex < 6 or self.animIndex > 8:
                    self.animIndex = 6
        if keyboard.up:
            self.player_y -= self.speed
            for i in range(numAnims):
                self.actor[i].y = self.player_y
                if self.player_y <= 0:
                    self.player_y = 0
            self.animSpeed += 1
            if self.animSpeed % 5 == 0:
                self.animIndex += 1
                if self.animIndex < 9 or self.animIndex > 11:
                    self.animIndex = 9
        self.blowup.x = self.player_x
        self.blowup.y = self.player_y

#小汽车类
class car:
    def __init__(self,car_x,car_speed,car_lane,direction):
        self.flag = 0
        self.lane = car_lane
        if direction == 0:
            self.actor = Actor('carleft')
        else:
            self.actor = Actor('carright')
        self.actor.x = car_x
        self.actor.y = 150 + (self.lane-1)*100
        self.speed = car_speed
    def update(self):
        self.actor.x += self.speed            #speed为矢量
    def draw(self):
        self.actor.draw()

#面包车类
class van:
    def __init__(self,van_x,van_speed,van_lane,direction):
        self.flag = 0
        self.lane = van_lane
        if direction == 0:
            self.actor = Actor('vanleft')
        else:
            self.actor = Actor('vanright')
        self.actor.x = van_x
        self.actor.y = 150 + (self.lane-1)*100
        self.speed = van_speed
    def update(self):
        self.actor.x += self.speed
    def draw(self):
        self.actor.draw()
        
#货车类
class truck:
    def __init__(self,truck_x,truck_speed,truck_lane,direction):
        self.flag = 0
        self.lane = truck_lane
        if direction == 0:
            self.actor = Actor('truckleft')
        else:
            self.actor = Actor('truckright')
        self.actor.x = truck_x
        self.actor.y = 150 + (self.lane-1)*100
        self.speed = truck_speed
    def update(self):
        self.actor.x += self.speed
    def draw(self):
        self.actor.draw()

#火车类
class train:
    def __init__(self,train_x,train_speed,train_lane,direction):
        self.flag = 0
        self.lane = train_lane
        if direction == 0:
            self.actor = Actor('trainleft')
        else:
            self.actor = Actor('trainright')
        self.actor.x = train_x
        self.actor.y = 150 + (self.lane-1)*100
        self.speed = train_speed
    def update(self):
        self.actor.x += self.speed
    def draw(self):
        self.actor.draw()

#飞机类
class plane:
    def __init__(self,plane_x,plane_speed,plane_lane,direction):
        self.flag = 0
        self.lane = plane_lane
        if direction == 0:
            self.actor = Actor('planeleft')
        else:
            self.actor = Actor('planeright')
        self.actor.x = plane_x
        self.actor.y = 150 + (self.lane-1)*100
        self.speed = plane_speed
    def update(self):
        self.actor.x += self.speed
    def draw(self):
        self.actor.draw()

#消防车水弹类
class Bullet:
    def __init__(self, x, y, direction):
        self.actor = Actor('bullet')
        self.actor.x = x
        self.actor.y = y
        self.speed = 6
        self.direction = direction
        
    def update(self):
        if self.direction == 1:
            self.actor.x += self.speed
            self.actor.y += self.speed
        elif self.direction == 2:
            self.actor.x += self.speed
            self.actor.y -= self.speed
        elif self.direction == 3:
            self.actor.x -= self.speed
            self.actor.y -= self.speed
        else:
            self.actor.x -= self.speed
            self.actor.y += self.speed
            
    
    def draw(self):
        self.actor.draw()


#消防车类
class firetruck:
    def __init__(self,firetruck_x,firetruck_speed,firetruck_lane,direction):
        self.flag = 1
        self.lane = firetruck_lane
        if direction == 0:
            self.actor = Actor('firetruckleft')
        else:
            self.actor = Actor('firetruckright')
        self.actor.x = firetruck_x
        self.actor.y = 150 + (self.lane-1)*100
        self.speed = firetruck_speed
        clock.schedule_interval(self.set_bullet, 0.7)
        self.bullets = []
    def update(self):
        self.actor.x += self.speed
        
        for bullet in self.bullets:
            bullet.update()
        
        #清除离开屏幕的子弹
        self.bullets = [bullet for bullet in self.bullets if 0 < bullet.actor.x < WIDTH and 0 < bullet.actor.y < HEIGHT]
        
    def draw(self):
        self.actor.draw()
        
        for bullet in self.bullets:
            bullet.draw()
    def set_bullet(self):
        for bulletdirection in range(0,4):
            x = self.actor.x
            y = self.actor.y 
            newbullet = Bullet(x ,y ,bulletdirection)
            self.bullets.append(newbullet)
            

                
                
#医疗箱
class healbox:
    def __init__(self,x,y):
        self.actor = Actor('healbox')
        self.actor.x = x
        self.actor.y = y
        self.name = 0
    def draw(self):
        self.actor.draw()

#加速
class faster:
    def __init__(self,x,y):
        self.actor = Actor('faster')
        self.actor.x = x
        self.actor.y = y
        self.name = 1
    def draw(self):
        self.actor.draw()

#香蕉皮类
class banana:
    def __init__(self,x,y):
        self.actor = Actor('banana')
        self.actor.x = x
        self.actor.y = y
        self.name = 2
    def draw(self):
        self.actor.draw()

#护盾
class shields:
    def __init__(self,x,y):
        self.actor = Actor('shields')
        self.actor.x = x
        self.actor.y = y
        self.name = 3
    def draw(self):
        self.actor.draw()

#创建新车   
def createcar():
    global list, WIDTH, CARNUM, SPEEDMIN, SPEEDMAX, SCORE

    if len(list) < CARNUM:
        lane = random.randint(1, 8)
        if SCORE <= 1:
            vehicle_class = random.randint(0, 1)
        elif SCORE <= 3:
            vehicle_class = random.randint(0, 2)
        elif SCORE <= 5:
            vehicle_class = random.randint(0, 3)
        elif SCORE <= 7:
            vehicle_class = random.randint(0, 4)
        else:
            vehicle_class = random.randint(0, 5)
        if vehicle_class == 0:
            if lane == 1 or lane == 3 or lane == 5 or lane == 7:  # 由左向右四车道
                carspeed = random.uniform(SPEEDMIN, SPEEDMAX)
                newcar = car(0, carspeed, lane, 0)
            else:
                carspeed = random.uniform(-SPEEDMAX, -SPEEDMIN)
                newcar = car(WIDTH, carspeed, lane, 1)
            # 检查新车辆与该车道上已有车辆是否发生碰撞
            while any(item.lane == lane and newcar.actor.colliderect(item.actor) for item in list):
                newcar.actor.x = random.uniform(0, WIDTH)
            list.append(newcar)

        elif vehicle_class == 1:
            if lane == 1 or lane == 3 or lane == 5 or lane == 7:  # 由左向右四车道
                vanspeed = random.uniform(SPEEDMIN, SPEEDMAX)
                newvan = van(0, vanspeed, lane, 0)
            else:
                vanspeed = random.uniform(-SPEEDMAX, -SPEEDMIN)
                newvan = van(WIDTH, vanspeed, lane, 1)
            # 检查新车辆与该车道上已有车辆是否发生碰撞
            while any(item.lane == lane and newvan.actor.colliderect(item.actor) for item in list):
                newvan.actor.x = random.uniform(0, WIDTH)
            list.append(newvan)

        elif vehicle_class == 2:
            if lane == 1 or lane == 3 or lane == 5 or lane == 7:  # 由左向右四车道
                truckspeed = random.uniform(SPEEDMIN, SPEEDMAX)
                newtruck = truck(0, truckspeed, lane, 0)
            else:
                truckspeed = random.uniform(-SPEEDMAX, -SPEEDMIN)
                newtruck = truck(WIDTH, truckspeed, lane, 1)
            # 检查新车辆与该车道上已有车辆是否发生碰撞
            while any(item.lane == lane and newtruck.actor.colliderect(item.actor) for item in list):
                newtruck.actor.x = random.uniform(0, WIDTH)
            list.append(newtruck)
            
        elif vehicle_class == 3:
            if lane == 1 or lane == 3 or lane == 5 or lane == 7:  # 由左向右四车道
                trainspeed = random.uniform(SPEEDMIN, SPEEDMAX)
                newtrain = train(0, trainspeed, lane, 0)
            else:
                trainspeed = random.uniform(-SPEEDMAX, -SPEEDMIN)
                newtrain = truck(WIDTH, trainspeed, lane, 1)
            # 检查新车辆与该车道上已有车辆是否发生碰撞
            while any(item.lane == lane and newtrain.actor.colliderect(item.actor) for item in list):
                newtrain.actor.x = random.uniform(0, WIDTH)
            list.append(newtrain)
        elif vehicle_class == 4:
            if lane == 1 or lane == 3 or lane == 5 or lane == 7:  # 由左向右四车道
                planespeed = random.uniform(8, 10)
                newplane = plane(0, planespeed, lane, 0)
            else:
                planespeed = random.uniform(-8, -10)
                newplane = truck(WIDTH, planespeed, lane, 1)
            # 检查新车辆与该车道上已有车辆是否发生碰撞
            while any(item.lane == lane and newplane.actor.colliderect(item.actor) for item in list):
                newplane.actor.x = random.uniform(0, WIDTH)
            list.append(newplane)
        elif vehicle_class == 5:
            if lane == 1 or lane == 3 or lane == 5 or lane == 7:  # 由左向右四车道
                firetruckspeed = random.uniform(SPEEDMIN, SPEEDMAX)
                newfiretruck = firetruck(0, firetruckspeed, lane, 0)
            else:
                firetruckspeed = random.uniform(-SPEEDMAX, -SPEEDMIN)
                newfiretruck = firetruck(WIDTH, firetruckspeed, lane, 1)
            # 检查新车辆与该车道上已有车辆是否发生碰撞
            while any(item.lane == lane and newfiretruck.actor.colliderect(item.actor) for item in list):
                newfiretruck.actor.x = random.uniform(0, WIDTH)
            list.append(newfiretruck)


#实例化
gamer = player(playerimages,player_x,player_y)

#画车
def drawcar():
    global list
    for item in list:
        item.draw()

#车辆更新
def updatecar():
    global list, WIDTH, HEART, gamer,Isblowup, Isshield
    items_to_remove = []
    for item in list:
        if item.actor.x > WIDTH + 10 or item.actor.x < -10:
            items_to_remove.append(item)
        if item.actor.colliderect(gamer.image):
            items_to_remove.append(item)
            if Isshield == 0:
                HEART -= 1 
            Isblowup = 1
            clock.schedule_unique(initIsblowup,0.5)
    for item in items_to_remove:
        list.remove(item)

    for item in list:
        item.update()

#去除爆炸特效   
def initIsblowup():
    global Isblowup
    Isblowup = 0

#判断生命归0或得分
def loseorgetscore():
    global SCORE, HEART, SPEEDMIN, SPEEDMAX, FINALSCORE, game_start, gamer, player_x, player_y, playerimages
    if gamer.player_y <= 50:
        SCORE += 1
        SPEEDMIN += 0.3
        SPEEDMAX += 0.3
        gamer.player_y = HEIGHT
    if HEART <= 0:
        game_start = -1
        HEART = 3
        FINALSCORE = SCORE
        SCORE = 0
        player_x = WIDTH/2
        player_y = HEIGHT
        SPEEDMIN = 3
        SPEEDMAX = 4
        gamer = player(playerimages,player_x,player_y)

#画生命爱心
def drawheart():
    global HEART,heart
    i = 0
    while i < HEART:
        heart[i].draw()
        i += 1

#道具创建
def createtool():
    global shieldsflag,fasterflag,healboxflag,bananaflag,toollist
    if shieldsflag == 0 and fasterflag == 0 and healboxflag == 0 and bananaflag == 0:
        if random.randint(-1,1) == 0:
            toolclass = random.randint(0,3)
            if toolclass == 0:
                newhealbox = healbox(random.randint(50,750),random.randint(200,800))
                toollist.append(newhealbox)
                healboxflag = 1
            elif toolclass == 1:
                newfaster = faster(random.randint(50,750),random.randint(200,800))
                toollist.append(newfaster)
                fasterflag = 1
            elif toolclass == 2:
                newbanana = banana(random.randint(50,750),random.randint(200,800))
                toollist.append(newbanana)
                bananaflag = 1
            elif toolclass == 3:
                newshields = shields(random.randint(50,750),random.randint(200,800))
                toollist.append(newshields)
                shieldsflag = 1
            
        clock.schedule_unique(deletetool,5)

#道具绘制
def drawtool():
    global toollist
    for item in toollist:
        item.actor.draw()
        
#删除道具
def deletetool():
    global toollist,fasterflag,shieldsflag,healboxflag,bananaflag
    toollist = []
    fasterflag = 0
    shieldsflag = 0
    healboxflag = 0
    bananaflag = 0

#拾取道具
def eattool():
    global toollist,fasterflag,shieldsflag,healboxflag,bananaflag,gamer,HEART,Isshield
    if len(toollist) > 0:
        for item in toollist:
            if item.actor.colliderect(gamer.image):
                if item.name == 0:
                    if HEART <= 2:
                        HEART += 1
                elif item.name == 1:
                    gamer.speed = 10
                    clock.schedule_unique(initspeed,5)
                elif item.name == 2:
                    gamer.speed = 2
                    clock.schedule_unique(initspeed,5)
                elif item.name == 3:
                    Isshield = 1
                    clock.schedule_unique(initshields,5)
                toollist = []

#消除护盾
def initshields():
    global Isshield
    Isshield = 0

#恢复初始速度 
def initspeed():
    global gamer
    gamer.speed = 5

def update():
    global HEART
    if SCORE < 10:
        HEART = 3
    gamer.update()
    loseorgetscore()
    createcar()
    updatecar()
    createtool()
    eattool()

#游戏按键
def on_mouse_down(pos):
    global game_start, go_home_button
    if start_button.collidepoint(pos):
        game_start = 1
    if go_home_button.collidepoint(pos):
        game_start = 0
    
def draw():
    #开始界面
    if game_start == 0:
        background.draw()
        title.draw()
        start_button.draw()
    #游戏进行界面
    elif game_start == 1:
        road.draw()
        gamer.draw()
        drawtool()
        drawcar()
        screen.draw.text(str(SCORE), (10, 10),fontsize=50,color='white')
        drawheart()
        if Isshield == 1:
            protect.pos = gamer.player_x,gamer.player_y
            protect.draw()
    #失败界面
    elif game_start == -1:
        screen.clear()
        background.draw()
        finalscore.draw()
        screen.draw.text(str(FINALSCORE),midtop=(WIDTH//2, 380), fontsize=200,color='yellow')
        go_home_button.draw()

pgzrun.go()
