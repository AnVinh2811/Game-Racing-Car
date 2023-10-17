#Thư viện
import pygame,sys
from pygame.locals import *
from pygame import mixer
import random
from pygame.sprite import Group
pygame.init()

#Màu nền
gray=(100,100,100)
green=(76,208,56)
yellow=(255,232,0)
red=(200,0,0)
white=(255,255,255)
black=(0,0,0)

#Tạo cửa sổ game
width=500
height=500
screen_size=(width,height)
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption("Xe Vượt Chướng Ngại Vật")
mixer.music.load('music/BackgroundMusic.wav')
mixer.music.play()

#Khởi tạo biến
gameover=False
speed=2
score=0
kmh=40 #Km/h

#Đường xe chạy
road_width=300
street_width=10
street_height=50

#Lane đường
lane_left=150
lane_center=250
lane_right=350
lanes=[lane_left,lane_center,lane_right]
lane_move_Y=0

#Đường và biên đường
road=(100,0,road_width,height)
left_edge=(95,0,street_width,height)
right_edge=(395,0,street_width,height)

#Vị trí ban đầu của người chơi
player_x=250
player_y=400

#Đối tượng xe công cộng
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image,x,y):
        pygame.sprite.Sprite.__init__(self)

        #Chỉnh hình cho phù hợp
        image_scale= 45 / image.get_rect().width
        new_width= image.get_rect().width * image_scale
        new_height=image.get_rect().height*image_scale
        self.image=pygame.transform.scale(image,(new_width,new_height))
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

#Đối tượng xe người chơi
class Player_vehicle(Vehicle):
    def __init__(self,x,y):
        image=pygame.image.load('images/car.png')
        super().__init__(image,x,y)

#Sprite groups
player_group = pygame.sprite.Group()
vehicle_group=pygame.sprite.Group()

#Tạo xe người chơi
player=Player_vehicle(player_x,player_y)
player_group.add(player)

#Tạo xe công cộng
image_name=['pickup_truck.png','semi_trailer.png','taxi.png','van.png']
Vehicle_image=[]
for name in image_name:
    image=pygame.image.load('images/'+name)
    Vehicle_image.append(image)

#Tạo va chạm
crash=pygame.image.load('images/crash.png')
crash_rect=crash.get_rect()

#Cài đặt khung hình/s (FPS)
clock=pygame.time.Clock()
fps=120

# Tạo màn hình dừng
def show_start_screen():
    # Vẽ nền màn hình dừng

    #Vẽ địa hình cỏ
    screen.fill(green)

    #Vẽ mặt đường
    pygame.draw.rect(screen,gray,road)

    #Vẽ biên đường
    pygame.draw.rect(screen,yellow,left_edge)    
    pygame.draw.rect(screen,yellow,right_edge)

    #Vẽ lane đường
    for y in range(street_height * -2,height,street_height*2):
        pygame.draw.rect(screen,white,(lane_left + 45,y + lane_move_Y, street_width,street_height))
        pygame.draw.rect(screen,white,(lane_center + 45,y + lane_move_Y, street_width,street_height))

    #Vẽ xe người chơi
    player_group.draw(screen)
    
    # Vẽ các đối tượng, văn bản, hình ảnh cần thiết trên màn hình dừng
    font=pygame.font.Font(pygame.font.get_default_font(),15)
    font1=pygame.font.Font(pygame.font.get_default_font(),16)    
    font2=pygame.font.Font(pygame.font.get_default_font(),20)

    text = font1.render('Press "Space" to play', True, white)
    text_rect = text.get_rect(center=(240,480))
    ###################################
    text_guide=font2.render("HOW TO PLAY", True, black)
    text_guide_rect = text.get_rect(center=(250,60))
    ###################################
    text_guide1=font.render("Control the vehicle using the left and right keys on the keyboard.", True, black)
    text_guide1_rect = text.get_rect(center=(100,90))
    ###################################
    text_guide2=font.render("Passing traffic cars will give you 1 point.", True, black)
    text_guide2_rect = text.get_rect(center=(185,110))
    ###################################
    text_guide3=font.render("If score divisible by 10 the vehicle's speed will increase.", True, black)
    text_guide3_rect = text.get_rect(center=(140,130))
    ###################################
    text_guide4=font.render("The game will end if there is a collision", True, black)
    text_guide4_rect = text.get_rect(center=(185,150))
    ###################################
    screen.blit(text, text_rect)
    screen.blit(text_guide,text_guide_rect)
    screen.blit(text_guide1,text_guide1_rect)
    screen.blit(text_guide2,text_guide2_rect)
    screen.blit(text_guide3,text_guide3_rect)
    screen.blit(text_guide4,text_guide4_rect)


    # Cập nhật màn hình
    pygame.display.flip()
    
    # Chờ người chơi nhấn phím để bắt đầu trò chơi
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key==K_SPACE:
                    waiting = False

# Hiển thị màn hình dừng trước khi bắt đầu trò chơi
show_start_screen()

##Vòng lặp xử lý game
running=True
while running:
    #Chỉnh khung hình/s
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==QUIT:
            running=False

        #Điều khiển xe
        if event.type==KEYDOWN:
            if event.key==K_LEFT and player.rect.center[0]>lane_left:
                player.rect.x -=100
            if event.key==K_RIGHT and player.rect.center[0]<lane_right:
                player.rect.x +=100

        #Kiểm tra va chạm khi điều khiển 
        for verhicle in vehicle_group:
            if pygame.sprite.collide_rect(player,vehicle):
                gameover=True
                pygame.mixer.music.load('music/Loser.wav')
                pygame.mixer.music.play()

    #Kiểm tra va chạm khi xe đứng yên
    if pygame.sprite.spritecollide(player,vehicle_group,True):
        gameover=True
        crash_rect.center=[player.rect.center[0],player.rect.top]
        pygame.mixer.music.load('music/Loser.wav')
        pygame.mixer.music.play()

    #Vẽ địa hình cỏ
    screen.fill(green)

    #Vẽ mặt đường
    pygame.draw.rect(screen,gray,road)

    #Vẽ biên đường
    pygame.draw.rect(screen,yellow,left_edge)    
    pygame.draw.rect(screen,yellow,right_edge)

    #Vẽ lane đường
    lane_move_Y+=speed * 2
    if lane_move_Y >= street_height * 2:
        lane_move_Y=0
    for y in range(street_height * -2,height,street_height*2):
        pygame.draw.rect(screen,white,(lane_left + 45,y + lane_move_Y, street_width,street_height))
        pygame.draw.rect(screen,white,(lane_center + 45,y + lane_move_Y, street_width,street_height))

    #Vẽ xe người chơi
    player_group.draw(screen)

    #Vẽ xe công cộng chạy
    if len(vehicle_group) < 2:
        add_verhicle= True
        for verhicle in vehicle_group:
            if verhicle.rect.top < verhicle.rect.height * 1.5:
                add_verhicle = False
        if add_verhicle:
            lane=random.choice(lanes)
            image=random.choice(Vehicle_image)
            verhicle=Vehicle(image,lane,height/-2)
            vehicle_group.add(verhicle)

    #Cho xe công cộng chạy
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        #Xóa xe công cộng
        if vehicle.rect.top >= height:
            vehicle.kill()
            score +=1

            #Tăng tốc độ chạy
            if score > 0 and score % 10 == 0:
                speed += 1
                kmh += 10

    #Vẽ xe công cộng
    vehicle_group.draw(screen)

    #Hiển thị điểm
    font=pygame.font.Font(pygame.font.get_default_font(),16)
    text=font.render('Score: '+str(score),True,white)
    text_rect=text.get_rect()
    text_rect.center=(50,40)
    text_speed=font.render('Speed: '+str(kmh)+' Km/h',True,red)
    text_speed_rect=text.get_rect()
    text_speed_rect.center=(220,480)
    screen.blit(text,text_rect)
    screen.blit(text_speed,text_speed_rect)

    if gameover:
        screen.blit(crash,crash_rect)
        pygame.draw.rect(screen,red,(0,50,width,100))
        font=pygame.font.Font(pygame.font.get_default_font(),16)
        text=font.render('Game Over! Play again? (Y / N)',True,white)
        text_rect=text.get_rect()
        text_rect.center=(width/2,100)
        screen.blit(text,text_rect)

    pygame.display.update()
    
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type==QUIT:
                gameover=False
                running=False
            if event.type==KEYDOWN:
                if event.key==K_y:
                    #reset game
                    show_start_screen()
                    gameover=False
                    score=0
                    kmh=40
                    speed=2
                    vehicle_group.empty()
                    player.rect.center=[player_x,player_y]
                    mixer.music.load('music/BackgroundMusic.wav')
                    mixer.music.play()
                elif event.key==K_n:
                    #quit game
                    gameover=False
                    running=False
pygame.quit()