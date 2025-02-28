# 100% working
#######################################################################################
#fronted with buffer[]
import pygame
import math as m
import threading #run parallet 2 programs 1)take runtime input form user 2)update lis[] acc to input and take actions


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SKIN=(232, 190, 172)
DARK_BLUE = (3, 5, 54)
WHITE = (255, 255, 255)
CROW  =(0,255,0)
EAGLE= (255,0,0)

class StarPoint:
    
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.color = col
    
    def info(self):
        print(self.x,"  ",self.y,"  ",self.color)

#used image circle mapping to deteermine, scaled and translated
star_points = [(245, 222), (301, 67), (357, 222),
                          (523, 228), (392, 331), (438, 490),
                          (301, 397), (163, 490), (209, 331), (79, 228)]

lis=[] #all infor of points
for x,y in star_points:
    tem=StarPoint(x,y,SKIN)
    lis.append(tem)

for i in lis:
    i.info()


inner_connections = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 0)] #inner point connection for line draw

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Star")



buffer=[] #lock -> take(_ ,_ ) make it empty ->unlock  :logic 
          #lock -> if empty or 1 elemnt add another ->unlock : front

def fro():

    # Main Loop
    done = False
    while not done:
        # Handle user-input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            elif event.type ==pygame.MOUSEBUTTONDOWN:
                if(event.button==1):  #left mouse button
                    mouse_pos= pygame.mouse.get_pos() #get button position

                    # print("  mouse pos  ",mouse_pos)
                    if out_crows>0 and m.pow((mouse_pos[0]-500),2)+m.pow((mouse_pos[1]-100),2)<=m.pow(25,2): #pseudo point has ind -1, if outcrows are 0 , makes no sense to append it
                            print(" ind =- 1")
                            buffer.append(-1)

                            if(len(buffer)==2):
                                print(buffer)
                                # buffer.clear()
                    
                    for i in range(len(lis)):
                        if m.pow((mouse_pos[0]-lis[i].x),2)+m.pow((mouse_pos[1]-lis[i].y),2)<=m.pow(30,2): 
                            # lis[i].color=(140,0,255)
                            print("ind:  ",i)
                            buffer.append(i)

                            if(len(buffer)==2):
                                print(buffer)
                                # buffer.clear()
                        
                        # else:
                            # lis[i].color=(255,140,0)
                    


        # Re-draw the window
        window.fill(DARK_BLUE)  # Fill background color
        if(out_crows>0):
            pygame.draw.circle(window,(255,100,0),(500,100),25) #psedo ,click first, while taking bird first time ,if out_crows are 0 makes no sense to display it

        ##font
        font = pygame.font.Font('freesansbold.ttf', 36) 
        text = font.render(todisplay, True, (0,100,0),(0,0,200))
        textRect = text.get_rect()
        window.blit(text,textRect)

        font2 = pygame.font.Font('freesansbold.ttf', 30) 
        text2 = font2.render(displayplayer, True, (0,100,0),(0,0,200))
        window.blit(text2,text.get_rect().bottomleft)

        font3 = pygame.font.Font('freesansbold.ttf', 30) 
        text3 = font3.render("intial pos selected", True, (0,100,0),(0,0,200))
        if(len(buffer)==1):
            window.blit(text3,(300,530))

        for i in range(len(lis)):
            start_poi = lis[i]
            end_poi = lis[(i + 1) % len(lis)]  # Wrap around for last point
            pygame.draw.line(window, WHITE, (start_poi.x,start_poi.y), (end_poi.x,end_poi.y), 2)
        

        # Draw lines connecting specific inner points
        for connection in inner_connections:
            start_point = lis[connection[0]]
            end_point = lis[connection[1]]
            pygame.draw.line(window, WHITE, (start_point.x, start_point.y), (end_point.x, end_point.y), 2)

        # Draw circles at each star point
        for point in lis:
            pygame.draw.circle(window, point.color, (point.x, point.y), int(30))

        pygame.display.flip()  # Update the display

        

    pygame.quit()




   


#######################################################################################









import threading


occupied=[0,0,0,0,0,0,0,0,0,0]  #common for crow and vulture

Vulture=-1

#crow possible move: a->b 
#adjacent for Crow moving adjacent
adjaList={
    # -1:[0,1,2,3,4,5,6,7,8,9] #all from start
    0:[1,2,8,9],
    1:[0,2],
    2:[0,1,3,4],
    3:[2,4],
    4:[2,3,5,6],
    5:[4,6],
    6:[4,5,7,8],
    7:[6,8],
    8:[6,7,9,0],
    9:[0,8]
    }

# print(adjaList[4])


jumpEagle={
    0:[[0,2,3],[0,8,7]],
    1:[[1,0,8],[1,2,4]],
    2:[[2,4,5],[2,0,9]],
    3:[[3,2,0],[3,4,6]],
    4:[[4,2,1],[4,6,7]],
    5:[[5,4,2],[5,6,8]],
    6:[[6,4,3],[6,8,9]],
    7:[[7,6,4],[7,8,0]],
    8:[[8,6,5],[8,0,1]],
    9:[[9,8,6],[9,0,2]],

}

print(jumpEagle[1])



out_crows =7
out_vulture=1
CurrEagleposn =-1
crowseaten=0
it=0
todisplay=f'Crows eaten: {crowseaten}'
displayplayer="Player1: Crow"
def func(bcopy): #later send as [i1,i2]
    global crowseaten,i,out_crows,out_vulture,CurrEagleposn,it,todisplay,displayplayer

    # while True:
    if(crowseaten>=4):
        print("Vulture Wins game")
        todisplay="Vulture Wins game"
        exit(0)
    # i+=1
    

    if(it%2==0):
        print("crow")
        if(out_crows>0):
            # flag=True
            # while(flag):
            p= bcopy[1] # int(input("put where crow, 0 index:  "))#ind #
            if(occupied[p]==0 and bcopy[0]==-1):
                occupied[p]=1
                lis[p].color= CROW  #--
                it+=1  #placed correctly therefore, eagle gets next chance
                # flag=False
                out_crows-=1
                displayplayer="Player2: Vulture"  #coz vulture has next move
                print("putted corect ,color it")
            else:
                print("choose again")
            # print("place a new crow")
        
        elif(out_crows==0): #move crow

            # flag=True
            # while(flag):
            p1= bcopy[0]  #int(input("put from where 0 index:  "))
            p2= bcopy[1] #int(input("put to   where 0 index:  "))

            if(occupied[p1]==1 and occupied[p2]==0 and  (p2 in adjaList[p1]) and p1 != CurrEagleposn):
                
                print("valid moved crow")
                occupied[p1]=0  #remove color
                lis[p1].color= SKIN
                occupied[p2]=1  #give color
                lis[p2].color= CROW
                # flag=False
                it+=1   #placed correctly therefore, eagle gets next chance
                print("change pos of crow")
                displayplayer="Player2: Vulture"
            else:

                print("try again")


            


    else: #eagle
        print("eagle:   ")

        if(out_vulture>0): #one time
            # flag=True
            # while(flag):
            p= bcopy[1]  #int(input("put where eagle, 0 index:  "))
            if(occupied[p]==0 and bcopy[0]==-1):
                occupied[p]=1
                lis[p].color= EAGLE
                flag=False
                CurrEagleposn=p #
                out_vulture-=1
                it+=1     #placed correctly therefore, crow gets next chance
                print("putted corect ,color it")
                displayplayer="Player1: Crow"
            else:
                print("choose again")

        
        
        # 2)  jump a crow and capture it. Jumps are only allowed in a straight line
        #Captured crows are removed from play
        #must jump a crow if the opportunity presents itself. 
        #find all  1+ jump posn possible (where crow is at middle)
        else:
            possiblejump=0

            #---- code to check possible
            jump1= jumpEagle[CurrEagleposn][0]  #[1,0,8]
            end1=-1
            crow1=-1
            if(occupied[jump1[1]]==1 and occupied[jump1[2]]==0 ):  #jump[0] is eagle(occupied) ,[1] if exist crow, [2] should ve vacant             
                possiblejump=1
                end1=jump1[2]
                crow1=jump1[1]
            
            end2=-1
            crow2=-1
            jump2= jumpEagle[CurrEagleposn][1]  #[1,2,4]
            if(occupied[jump2[1]]==1 and occupied[jump2[2]]==0 ): 
                possiblejump=1
                end2=jump2[2]
                crow2=jump2[1]

            #---- code
            if(possiblejump==1):

                print("Eagle should jump")

                # flag=True  #loop untill eagle jumps
                # while(flag):
                p= bcopy[1] #int(input("jump eagle to 0 index:  "))
                

                if(p == end1):  #valid jump

                    occupied[CurrEagleposn]=0  #also remove color  old pos  
                    lis[CurrEagleposn].color= SKIN   

                    occupied[end1]=1  #also give color of eagle
                    lis[end1].color= EAGLE

                    occupied[crow1]=0  #remove crow color,
                    lis[crow1].color= SKIN

                    crowseaten+=1
                    
                    CurrEagleposn=end1

                    # flag=False
                    it+=1
                    displayplayer="Player1: Crow" #next crow plays
                    
                    print("Eagle jumped")
                    print("crows eaten:  ",crowseaten)
                    todisplay=f'Crows eaten: {crowseaten}'
                


                elif(p==end2):  #valid jump
                    occupied[CurrEagleposn]=0  #also remove color  old pos 
                    lis[CurrEagleposn].color= SKIN    

                    occupied[end2]=1  #also give color of eagle
                    lis[end2].color= EAGLE

                    occupied[crow2]=0  #remove crow color,
                    lis[crow2].color= SKIN
                    crowseaten+=1
                    CurrEagleposn=end2

                    # flag=False
                    it+=1
                    print("Eagle jumped")
                    displayplayer="Player1: Crow" #next crow player
                    print("crows eaten:  ",crowseaten)
                    todisplay=f'Crows eaten: {crowseaten}'
                    


                else:

                    print("Eagle can jump here,make it jump")

                


                # print(" jump eagle ") #reduce crow, make middle posn/occupied vacant, change middle color 

            elif(possiblejump==0):

                #did crow win TEST at Visually###
                didcrowwin=0
                # print(CurrEagleposn,"    ",adjaList[CurrEagleposn])
                for zz in adjaList[CurrEagleposn]:
                    # print(zz,"       ",occupied[zz])
                    if(occupied[zz]==0):
                        didcrowwin=1
                if(didcrowwin==0):
                    print("Crow win")
                    todisplay="CROWS WIN"
                    exit(0)
                ############################3333333

                #if not possible jump, ->allow to adjacent move

                # 3) adjacent move,move to unocuppeid position like crow
                # flag=True
                # while(flag):
                p1= CurrEagleposn
                p2= bcopy[1] #int(input(f"put eagle form {CurrEagleposn} to 0 index:  "))

                

                if(occupied[p1]==1 and occupied[p2]==0 and  (p2 in adjaList[p1]) and CurrEagleposn==bcopy[0]):
                    
                    print("valid moved eagle")
                    occupied[p1]=0  #remove color
                    lis[p1].color= SKIN

                    occupied[p2]=1  #give color
                    lis[p2].color= EAGLE

                    # flag=False
                    it+=1
                    CurrEagleposn= p2
                    displayplayer="Player1: Crow"
                else:

                    print("try again")


            # print("change pos of crow")
    if(crowseaten>=4):
        print("Vulture Wins game")
        todisplay="Vulture Wins game"
        exit(0)       



    ##############3333 repeated code to update wining status instantenasly before even Vulture makes move
    if(it>3): #at it=0 ,CurrEaglepos =-1, resulting in error, anyhow in 3 moves crows cant win
        possiblejum=0
        #---- code to check possible
        jump1= jumpEagle[CurrEagleposn][0]  #[1,0,8]
        end1=-1
        crow1=-1
        if(occupied[jump1[1]]==1 and occupied[jump1[2]]==0 ):  #jump[0] is eagle(occupied) ,[1] if exist crow, [2] should ve vacant             
            possiblejum=1
            end1=jump1[2]
            crow1=jump1[1]
        
        end2=-1
        crow2=-1
        jump2= jumpEagle[CurrEagleposn][1]  #[1,2,4]
        if(occupied[jump2[1]]==1 and occupied[jump2[2]]==0 ): 
            possiblejum=1
            end2=jump2[2]
            crow2=jump2[1]
        didcrowwin_=0
        # print(CurrEagleposn,"    ",adjaList[CurrEagleposn])
        for zz in adjaList[CurrEagleposn]:
            # print(zz,"       ",occupied[zz])
            if(occupied[zz]==0):
                didcrowwin_=1
        if(didcrowwin_==0 and possiblejum==0):
            print("Crow win")
            todisplay="CROWS WIN"
            exit(0)
    ####################################33       


        
    print(occupied)










######################################3
stop=False

def main():
    global stop
    while not stop:
        # ind =int(input("enter index:  "))
        if(len(buffer)==2):
            bcopy=buffer
            if bcopy[1]!=-1: #dont sent if arg[1]==-1
                print("bcopy  ",bcopy)
                func(bcopy)
            buffer.clear()
            print("OUT EAGLE POS DISP ",CurrEagleposn)











if __name__ == "__main__":
   threading.Thread(target=main).start()
   fro()   #threading of only pygame func not possible
   stop=True #after pygame stopped



   
