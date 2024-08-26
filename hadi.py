import tkinter as tk
import pygame
import random
import time
from PIL import Image, ImageTk
import tkinter.font as tkfont

                        #imports
##########################################################
main = tk.Tk()
bg = tk.PhotoImage(file="pozadie.png")
canvas = tk.Canvas(width=bg.width(),height=bg.height())
canvas.pack()
img_id = canvas.create_image(bg.width()/2,bg.height()/2,image = bg)
pygame.mixer.init()

                        #premenne
##########################################################
sprite_idx = 0
braid_id = canvas.create_image(320, 322)
movement = 5
moving = False
current_direction = " "
x_had = random.randrange(20, 580)
y_had = 76
movement_snake = 2.5
score_display = None
ammo_display = None
ammo_pohyb = 0
ammo_number = 0
ammo_id = None
ammo_speed = 10
snake_direction = "right"
score = 0
random_x = random.randint(166,433)
parachute_y = 2
running = True
fly = False
drop_check = False
##########################################################
shoot = pygame.mixer.Sound("vystrel.wav")
land = pygame.mixer.Sound("impact.wav")
ammozero = pygame.mixer.Sound("empty.wav")
song = pygame.mixer.Sound("song.wav")
reload = pygame.mixer.Sound("reload.wav")
sound_teleport = pygame.mixer.Sound("teleport.wav")
drop = pygame.mixer.Sound("drop.wav")



def drop_sound():
    drop.set_volume(0.3)
    drop.play()
def teleport_sound():
    sound_teleport.set_volume(0.3)
    sound_teleport.play()
def shoot_sound():
    shoot.set_volume(0.3)
    shoot.play()

def land_sound():
    land.set_volume(0.2)
    land.play()
def ammozero_sound():
    ammozero.set_volume(0.3)
    ammozero.play()

def song_sound():
    song.play()
    song.set_volume(0.1)
    canvas.after(389000,song_sound)
def reload_sound():
    reload.set_volume(0.3)
    reload.play()
                        #zvuky
##########################################################

parachute = tk.PhotoImage(file="rsz_parachute_real.png")
parachute_id = canvas.create_image(random_x,200,image = parachute)

board_im = tk.PhotoImage(file="board1.png")
board_id = canvas.create_image(338,28,image = board_im)

ammo_board = tk.PhotoImage(file="board.png")
board_ammo_id = canvas.create_image(501,490,image = ammo_board)

snake_image_right = tk.PhotoImage(file="snake1_right.png")
snake_id = canvas.create_image(x_had, y_had, anchor=tk.NW, image=snake_image_right)
snake_image_left = tk.PhotoImage(file="snake1_left.png")

game_over_img = tk.PhotoImage(file="game_over.png")
                        #objekty
##########################################################
def load_sprites(file_path, rows, cols):
    global sprites
    sprite_img = tk.PhotoImage(file=file_path)
    sprites = []


    height = sprite_img.height()//rows
    width = sprite_img.width()//cols

    for row in range(rows):
        for col in range(cols):
            l = col*width
            t = row*height
            r = (col+1)*width
            b = (row+1)*height
            subimage = create_sub_image(sprite_img, l, t, r, b)
            sprites.append(subimage)
    return sprites
def create_sub_image(img, left, top, right, bottom):
    subimage = tk.PhotoImage()
    subimage.tk.call(subimage, 'copy', img, '-from',
                      left, top, right, bottom, '-to', 0, 0)
    return subimage
sprites_right = load_sprites("braid_right25.png",4,7)
sprites_left = load_sprites("braid_left25.png",4,7)
                        #sprite_loader
##########################################################
def animate():
    global sprites,sprite_idx,braid,sprites_right,sprites_left
    if current_direction == "right":
        sprite_idx = (sprite_idx + 1 ) % 27
        braid = canvas.itemconfig(braid_id,image = sprites_right[sprite_idx])
    elif current_direction == "left":
        sprite_idx = (sprite_idx + 1) % 27
        braid = canvas.itemconfig(braid_id, image=sprites_left[sprite_idx])
    canvas.after(20,animate)

def move_braid(event):
    global movement,current_direction
    if event.keysym == "Right":
        current_direction = "right"
        canvas.move(braid_id,movement,0)
    elif event.keysym == "Left":
        current_direction = "left"
        canvas.move(braid_id,-movement,0)

def teleport():
    global braid_id
    braid_coords = canvas.coords(braid_id)
    if braid_coords[0] >= 620:
        teleport_sound()
        canvas.move(braid_id,-600,0)
    elif braid_coords[0] == 0:
        teleport_sound()
        canvas.move(braid_id,590,0)
    canvas.after(10,teleport)

def respawn_snake():
    global snake_id, snake_direction
    canvas.delete(snake_id)
    snake_direction = "right"
    x_had = random.randint(20,580)

    snake_id = canvas.create_image(x_had, y_had, anchor=tk.NW, image=snake_image_right)

def snakes():
    global snake_id,snake_direction,snake_coords

    snake_coords = canvas.coords(snake_id)


    if snake_direction == "right":
        canvas.move(snake_id,movement_snake,0)


        if snake_coords[0] >= 560:
            snake_direction = "left"
            canvas.itemconfig(snake_id,image = snake_image_left)

    elif snake_direction == "left":
        canvas.move(snake_id,-movement_snake,0)

        if snake_coords[0] <= 40:
            snake_direction = "right"
            canvas.itemconfig(snake_id,image = snake_image_right)
    canvas.after(25, snakes)

def ammo_text():
    global ammo_number,ammo_display
    canvas.delete(ammo_display)
    ammo_display = canvas.create_text(500,450,text=f"Ammo :{ammo_number}",font=("Arial", 25, "bold"),fill="gold")



def ammo_shoot(event):
    global ammo_number, ammo_id,ammo_image
    ammo_image = tk.PhotoImage(file="rsz_ammo1.png")
    if ammo_number == 0:
        ammozero_sound()
    if ammo_number > 0:
        if ammo_id is not None:
            canvas.delete(ammo_id)
        coords_braid = canvas.coords(braid_id)
        ammo_id = canvas.create_image(coords_braid[0]+5, coords_braid[1]-7,image = ammo_image)
        ammo_number -= 1

        shoot_sound()
        ammo_text()
        move_ammo()

def move_ammo():
    global ammo_id, ammo_speed,coords_ammo,snake_coords,score,ammo_number,land_sound
    coords_ammo = canvas.coords(ammo_id)

    if (snake_coords[0] < coords_ammo[0] < snake_coords[0] + 45 and
            snake_coords[1] < coords_ammo[1] < snake_coords[1] + 45):
        score += 10
        respawn_snake()
        score_text()
        canvas.delete(ammo_id)
        land_sound()
        check_for_drop()
        return
    if coords_ammo[1] > 0:
        canvas.move(ammo_id, 0, -ammo_speed)
        canvas.after(20, move_ammo)

def score_text():
    global score, score_display

    canvas.delete(score_display)
    score_display = canvas.create_text(300, 19, text=f"Score : {score}", font="western", fill="gold")

def game_over():
    global score,ammo_number,drop_check
    if drop_check == False and ammo_number == 0 and score %50 != 0:
        game_over_id = canvas.create_image(320,240,image=game_over_img)
        score_display_end = canvas.create_text(365, 331, text=f"{score}", font=("Arial", 25, "bold"), fill="red")
        delete()
    canvas.after(5000,game_over)

def animate_parachute():
    global parachute_y,braid_id,ammo_number,parachute_coords,parachute_id,drop_check

    parachute_coords = canvas.coords(parachute_id)
    braid_id_coords = canvas.coords(braid_id)

    if parachute_coords[1] <= 300:
        canvas.move(parachute_id,0,parachute_y)
        drop_check = True

    if (parachute_coords[0]-45 < braid_id_coords[0] < parachute_coords[0]-20 + 64 and
        parachute_coords[1]-20 < braid_id_coords[1] < parachute_coords[1]+20 +  64):
            ammo_number += 7
            ammo_text()
            reload_sound()
            canvas.delete(parachute_id)
            drop_check = False
    canvas.after(50,animate_parachute)

def check_for_drop():
    global score,parachute_id,parachute_y,drop_sound,movement_snake,movement
    if score % 50 == 0:
        parachute_id = canvas.create_image(random_x,0,image =parachute )
        drop_sound()
        animate_parachute()
        movement_snake += 0.5
        parachute_y += 0.5


    if score > 0 and score % 100 == 0 and score < 1000: #braid boost
        movement += 0.4
    if score > 0 and score % 50 == 0 and score < 1000: #had boost
        movement_snake += 0.1

def delete():
    canvas.delete(snake_id)
    canvas.delete(parachute_id)
    canvas.delete(board_id)
    canvas.delete(ammo_id)
    canvas.delete(braid_id)
    drop.set_volume(0)
    shoot.set_volume(0)
    sound_teleport.set_volume(0)
    land.set_volume(0)
    ammozero.set_volume(0.0)
    song.set_volume(0)
    reload.set_volume(0)

                        #objekty
#########################################################

animate()
ammo_text()
snakes()
score_text()
teleport()
animate_parachute()
song_sound()
game_over()
                        #funkcie
##########################################################

main.bind("<KeyPress>", move_braid)
canvas.bind("<Button-1>",ammo_shoot)

                        #bindy
##########################################################
canvas.mainloop()
