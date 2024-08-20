import pygame
import math
pygame.init()

from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
    K_q,
    K_e,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
    K_f,
    K_r,
    K_g,
)

TURN_MOVES=6
PLAYER_LEFT=0
PLAYER_RIGHT=1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FLOOR_HEIGHT=40
WALL_HEIGHT=150
WALL_WIDTH=50
FLOOR_COLOUR=(101, 186, 45)
WALL_COLOUR=(128, 128, 128)
BG_COLOUR=(0,0,0)
PROMPT=pygame.Rect(200,200,400,200)
PROMPT_BUTTON=pygame.Rect((SCREEN_WIDTH/2)-(80/2),360,80,30)
FLOOR=pygame.Rect(0,SCREEN_HEIGHT-FLOOR_HEIGHT,SCREEN_WIDTH,FLOOR_HEIGHT)
WALL=pygame.Rect((SCREEN_WIDTH/2)-(WALL_WIDTH/2),SCREEN_HEIGHT-FLOOR_HEIGHT-WALL_HEIGHT,WALL_WIDTH,WALL_HEIGHT)
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
prompt_font1 = pygame.font.SysFont(None, 25)
prompt_font2 = pygame.font.SysFont(None, 40)
PLAYER_HEIGHT=64
PLAYER_WIDTH=32
game_loser=None
game_running=True
turn=0
COLOR = (255, 100, 98)
BULLETCOLOR=(255,255,255)
COLORS=[(255,0,0),(0,0,255),(0,255,0)]
SPELLS=["Crucio","Stupefy","Disillusionment Charm"]
showinfos=False
showcontrols=True
def game_done(side):
    global game_loser
    game_loser=side
wantmessage=False
def outputing(out):
    if wantmessage:
        print(out)
def draw_bg():
    window.fill(BG_COLOUR)
    pygame.draw.rect(window,FLOOR_COLOUR,FLOOR)
    pygame.draw.rect(window,WALL_COLOUR,WALL)
    text3 = prompt_font1.render("MADE BY VED AND ADITYA - 10th GRADE                                                          G to see controls", True, (0, 0, 0))
    window.blit(text3, (10,SCREEN_HEIGHT-20))
    if game_loser!=None:
        if game_loser==0:
            name="Player right"
        else:
            name="Player left"
        message_box(["Game Over",f"{name} won!"])


def message_box(message):
    pygame.draw.rect(window, WALL_COLOUR, PROMPT)
    pygame.draw.rect(window, (0, 0, 0), PROMPT_BUTTON)
    count=210
    for item in message:
        window.blit( prompt_font1.render(item, True, (255, 255, 255)), (210, count))
        count+=30
    text3 = prompt_font1.render("EXIT", True, (255, 255, 255))
    window.blit(text3, ((SCREEN_WIDTH / 2) - (80 / 2) + 10, 360 + 7))
Left_player_image=pygame.image.load("pixelbald.png")
Right_player_image=pygame.image.load("pixel-wizard-games-applications-260nw-675648199.png")
class Player(pygame.sprite.Sprite):


    def __init__(self,colour,side):
        super(Player, self).__init__()
        self.colour=colour
        self.side=side
        self.image=pygame.Surface((PLAYER_WIDTH,PLAYER_HEIGHT))
        self.rect=self.image.get_rect()
        if side==PLAYER_LEFT:
            self.image.blit(Left_player_image, (0, 0))
            self.rect.x=30
        elif side==PLAYER_RIGHT:
            self.image.blit(Right_player_image, (0, 0))
            self.rect.x=SCREEN_WIDTH-30-PLAYER_WIDTH
        self.rect.y = SCREEN_HEIGHT - FLOOR_HEIGHT - PLAYER_HEIGHT
        self.start_x=self.rect.x
        self.health=4
        self.disappear=False

    def update(self,key):
        global turn,HIT,showinfos,showcontrols
        if self.disappear:
            outputing("kill me pls")
            self.image.blit(pygame.image.load("Untitled.png"), (0, 0))
        else:
            if self.side == PLAYER_LEFT:
                self.image.blit(Left_player_image, (0, 0))

            elif self.side == PLAYER_RIGHT:
                self.image.blit(Right_player_image, (0, 0))




        if FIRING:
            return
        if key==K_RETURN:
            self.start_x = self.rect.x
            return
        if turn%2==self.side:
            if key==K_a:
                self.rect.x-=10
                if pygame.Rect.colliderect(self.rect,WALL):
                    self.rect.x+=10
                if abs(self.start_x-self.rect.x) > TURN_MOVES*10 :
                    self.rect.x += 10
            if key==K_d:
                self.rect.x+=10
                if pygame.Rect.colliderect(self.rect,WALL):
                    self.rect.x-=10
                if abs(self.start_x-self.rect.x) > TURN_MOVES*10 :
                    self.rect.x -= 10
            if key==K_r:
                if showinfos:
                    showinfos=False
                else:
                    showinfos=True
            if key==K_g:
                if showcontrols:
                    showcontrols=False
                else:
                    showcontrols=True
        if key=="hit" and turn%2==self.side:
            spells(self)
            if self.health==0:
                game_done(self.side)
            HIT = False
            outputing(self.health)
        self.change_turn()


    def change_turn(self):
        self.start_x=self.rect.x

class HealthBar(pygame.sprite.Sprite):

    def __init__(self, connection):
        super(HealthBar, self).__init__()
        self.connection=connection
        self.side = connection.side
        self.image = pygame.Surface((64, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x=connection.rect.x-16
        self.rect.y =connection.rect.y-20
        self.start_x = self.rect.x


    def update(self):
        self.rect.x=self.connection.rect.x-16
        self.rect.y =self.connection.rect.y - 20
        self.image.fill((128, 128, 128))
        pygame.draw.rect(self.image, (255, 0, 0), pygame.Rect(0, 0, 64 * (self.connection.health / 4), 10))
        if self.connection.disappear:
            self.image.fill((0, 0, 0))



class Gun(pygame.sprite.Sprite):

    def __init__(self, connection, message):
        super(Gun, self).__init__()
        self.connection=connection
        outputing(self.connection.side)
        self.side=connection.side
        if self.side == PLAYER_LEFT:
            self.x_difference = 32
            self.pivot = (0, 1)
        else:
            self.x_difference = 0
            self.pivot = (0, 1)
        self.y_difference=34
        self.origin=(connection.rect.x + self.x_difference,connection.rect.y + self.y_difference)
        self.message=message
        self.side = connection.side
        self.image = pygame.Surface((30, 3))
        self.image.set_colorkey((0,0,0))
        self.image.fill((150,75,0))
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=(self.origin[0] - self.pivot[0], self.origin[1] - self.pivot[1]))
        self.update()



    def update(self):
        if self.side == PLAYER_LEFT:
            self.angle = self.message.a
            outputing(self.connection.side)

        else:
            self.angle = 180 - self.message.a
            outputing(self.connection.side)
        self.origin=(self.connection.rect.x + self.x_difference,self.connection.rect.y + self.y_difference)
        self.image.fill((150, 75, 0))

        # offset from pivot to center
        image_rect = self.original_image.get_rect(topleft=(self.origin[0] - self.pivot[0], self.origin[1] - self.pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(self.origin) - image_rect.center

        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-self.angle)

        # roatetd image center
        rotated_image_center = (self.origin[0] - rotated_offset.x, self.origin[1] - rotated_offset.y)

        # get a rotated image
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=rotated_image_center)
        if self.connection.disappear:
            outputing("ba;;s")
            self.image.fill((0, 0, 0))
        # self.angle += 10





class Message(pygame.sprite.Sprite):

    def __init__(self,message_side):
        super(Message, self).__init__()
        self.image=pygame.Surface((250,100))
        self.rect = self.image.get_rect()
        self.font1 = pygame.font.SysFont(None, 25)
        self.a=60
        self.v=100
        self.spellno=0
        self.side=message_side
        m=[f"angle: {self.a}",f"velocity: {self.v}",f"spell: {SPELLS[self.spellno]}"]
        text1= self.font1.render(m[0], True, (255, 255, 255))
        text2 = self.font1.render(m[1], True, (255, 255, 255))
        text3 = self.font1.render(m[2], True, (255, 255, 255))
        self.image.blit(text1,(0,0))
        self.image.blit(text2, (0, 20))
        self.image.blit(text3, (0, 40))
        if message_side==PLAYER_LEFT:
            self.rect.x=10
            self.rect.y=10
        else:
            self.rect.x = SCREEN_WIDTH-250-10
            self.rect.y = 10

    def update(self,key):
        global SPELLNO
        if FIRING:
            return
        if turn%2==self.side:
            if key==K_q and self.a>10:
                self.a-=5
            elif key==K_e and self.a<85:
                self.a+=5
            elif key==K_w and self.v<100:
                self.v+=5
            elif key==K_s and self.v>5:
                self.v-=5
            elif key==K_f:
                if self.spellno==2:
                    self.spellno=0
                else:
                    self.spellno+=1
        m = [f"angle: {self.a}", f"speed: {self.v}", f"spell: {SPELLS[self.spellno]}"]
        text1 = self.font1.render(m[0], True, (255, 255, 255))
        text2 = self.font1.render(m[1], True, (255, 255, 255))
        text3 = self.font1.render(m[2], True, (255, 255, 255))
        self.image.fill((0,0,0))
        self.image.blit(text1, (0, 0))
        self.image.blit(text2, (0, 20))
        self.image.blit(text3, (0, 40))

    def get_values(self):
        return[self.a,self.v]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, height, width,start_x,start_y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.width = width
        self.color = color
        self.image.fill((0,0,0))
        self.image.set_colorkey(COLOR)
        pygame.draw.circle(self.image, color, [width / 2, width / 2], width / 2)

        self.rect = self.image.get_rect()
        self.rect.x=start_x
        self.rect.x=start_y
        self.time = 0
        self.startRect = self.image.get_rect()
        self.startRect.x=start_x
        self.startRect.y = start_y
        outputing(f"start : , {self.startRect.x}, {self.startRect.y}")

    def update(self,info):
        global FIRING,HIT
        if turn%2!=PLAYER_LEFT:
            angle,speed=info
            angle=math.radians(angle)
            if self.rect.y <= SCREEN_HEIGHT-FLOOR_HEIGHT-20:
                self.time += 0.05
                velx = math.cos(angle) * speed
                vely = math.sin(angle) * speed
                dx = velx * self.time
                dy = (vely * self.time) + ((-9.81 * (self.time ** 2)) / 2)
                self.rect.x = self.startRect.x + dx
                self.rect.y = self.startRect.y - dy
                if  pygame.Rect.colliderect(self.rect,WALL) or self.rect.x>=SCREEN_WIDTH:
                    FIRING = False
                    bullets.empty()
                elif pygame.Rect.colliderect(self.rect, player1.rect):
                    outputing("Hit!")
                    HIT = True
                    FIRING = False
                    bullets.empty()
            else:
                FIRING = False
                bullets.empty()
        else:
            angle, speed = info
            angle = math.radians(angle)
            if self.rect.y<=SCREEN_HEIGHT-FLOOR_HEIGHT-20:
                self.time+=0.05
                velx=math.cos(angle)*speed
                vely=math.sin(angle)*speed
                dx=  velx*self.time
                dy=(vely*self.time)+((-9.81*(self.time**2))/2)
                self.rect.x=self.startRect.x-dx
                self.rect.y=self.startRect.y-dy
                if pygame.Rect.colliderect(self.rect, WALL) or self.rect.x<=0:
                    FIRING = False
                    bullets.empty()
                elif pygame.Rect.colliderect(self.rect, player2.rect):
                    outputing("Hit!")
                    HIT=True
                    FIRING = False
                    bullets.empty()
            else:
                bullets.empty()
                FIRING=False

clock = pygame.time.Clock()
HIT=False
player=True
FIRING=False
bullets= pygame.sprite.Group()

def spells(player):
    global turn

    if player.side==PLAYER_RIGHT:
        outputing("his:" + str(message2.spellno))
        if message2.spellno==0:
            player1.health-=1

        elif message2.spellno==1:
            outputing("bald")
            turn+=1
        elif message2.spellno==2:
            player1.disappear=True
            player1.update("bald")
            gun1.update()

    else:
        outputing("hir:" + str(message1.spellno))
        if message1.spellno==0:
            player2.health-=1
        elif message1.spellno==1:
            outputing("balder")
            turn+=1
        elif message1.spellno==2:
            player2.disappear=True
            player2.update("bald")
            gun2.update()


def show_info():
    message_box(["Spell Information", "Crucio - deals damage to opponent","Stupefy - stuns opponent for one turn","Disillusionment Charm - makes opponent lose","track of their position"])

def show_controls():
    message_box(["A/D - Move left/right", "W/S - increase/decrease speed of projectile",
                 "Q/E - increase/decrease angle of projectile","Enter - shoot", "F - rotate through spells", "R - see spell info"])
def shoot():
    global player
    outputing(turn)
    outputing(player)
    player1.disappear,player2.disappear=[False,False]
    player1.update("awa")
    player2.update("uwu")

    if player:
        if message2.spellno!=3:
            start_x, start_y=[gun2.rect.midleft[0],gun2.rect.midleft[1]]
            bullet = Bullet(COLORS[message2.spellno], 18, 18, start_x, start_y)
            bullets.add(bullet)
    else:
        if message1.spellno != 3:
            start_x, start_y = [gun1.rect.midright[0], gun1.rect.midright[1]]
            bullet = Bullet(COLORS[message1.spellno], 18, 18, start_x, start_y)
            bullets.add(bullet)





players=pygame.sprite.Group()
messages=pygame.sprite.Group()
healthbars=pygame.sprite.Group()
guns=pygame.sprite.Group()

player1=Player((0,255,255),PLAYER_RIGHT)
player2=Player((255,0,255),PLAYER_LEFT)

healthbar1=HealthBar(player1)
healthbar2=HealthBar(player2)

message1=Message(PLAYER_RIGHT)
message2=Message(PLAYER_LEFT)

gun1=Gun(player1,message1)
gun2=Gun(player2,message2)

players.add(player1)
players.add(player2)

messages.add(message1)
messages.add(message2)

healthbars.add(healthbar1)
healthbars.add(healthbar2)

guns.add(gun1)
guns.add(gun2)

while game_running:
    player=(turn%2)==PLAYER_LEFT
    if HIT:
        if player:
            player2.update("hit")
        else:
            player1.update("hit")

    for event in pygame.event.get():
        if event.type==KEYDOWN and game_loser==None:
            if event.key==K_ESCAPE:
                game_running=False
            else:
                if event.key==K_RETURN and not FIRING:
                    turn+=1
                    FIRING = True
                    shoot()
                messages.update(event.key)
                players.update(event.key)
                guns.update()

        elif event.type==QUIT:
            game_running=False

        elif event.type==pygame.MOUSEBUTTONDOWN:
            (x,y)=pygame.mouse.get_pos()
            if (x>=(SCREEN_WIDTH / 2) - (80 / 2) and x<=((SCREEN_WIDTH / 2) - (80 / 2))+80) and (y>=360 and y<=360+30) and game_loser!=None:
                game_running = False
            if (x>=(SCREEN_WIDTH / 2) - (80 / 2) and x<=((SCREEN_WIDTH / 2) - (80 / 2))+80) and (y>=360 and y<=360+30) and showinfos:
                showinfos=False
            if (x>=(SCREEN_WIDTH / 2) - (80 / 2) and x<=((SCREEN_WIDTH / 2) - (80 / 2))+80) and (y>=360 and y<=360+30) and showcontrols:
                showcontrols=False
    draw_bg()
    if showinfos:
        show_info()

    if showcontrols:
        show_controls()


    if player:
        clock.tick(100)
        bullets.update(message1.get_values())
        bullets.draw(window)
    else:
        clock.tick(100)
        bullets.update(message2.get_values())
        bullets.draw(window)
    players.draw(window)
    guns.draw(window)
    messages.draw(window)
    healthbars.update()
    healthbars.draw(window)

    pygame.display.flip()
