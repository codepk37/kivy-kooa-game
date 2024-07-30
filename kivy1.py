import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse, Line
import math as m
from kivy.clock import Clock  # Import Clock for scheduling GUI updates
import threading #run parallet 2 programs 1)take runtime input form user 2)update lis[] acc to input and take actions
from kivy.core.window import Window

buffer=[]

CROW  =(0,255,0)
EAGLE= (255,0,0)
SKIN=(232, 190, 172)



class StarPoint:
    
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.color = col
    
    def info(self):
        print(self.x,"  ",self.y,"  ",self.color)

#used image circle mapping to deteermine, scaled and translated
ori_star_points = [(245,900- 222), (301,900- 67), (357,900- 222),
                          (523,900- 228), (392,900- 331), (438,900- 490),
                          (301,900- 397), (163,900- 490), (209,900- 331), (79,900- 228)]

pseudopos=( Window.width*(500-30)/900,Window.height* (800-30)/900 )
star_points = [(Window.width * x / 900, Window.height * y/ 900) for x, y in ori_star_points]

lis=[] #all infor of points
for x,y in star_points:
    tem=StarPoint(x,y,SKIN)
    lis.append(tem)

for i in lis:
    i.info()

###########################################################33







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




############################################################333
#frotnted
class Star(Widget):
    global star_points,lis,crowseaten,out_crows,out_vulture,todisplay,displayplayer
    

    inner_connections = [(0, 2), (2, 4), (4, 6), (6, 8), (8, 0)]

    # text = 2  # Define text as a class attribute

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_rect, pos=self.update_rect)
        self.draw_star()
        Clock.schedule_interval(self.update_display, 1.0 / 60.0)  # Update display 60 times per second

    def draw_star(self):
        with self.canvas:
            Color(3/255, 5/255, 54/255)  # Set background color to DARK_BLUE
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
            Color(1, 1, 1)
            for i in range(len(star_points)):
                start_point = star_points[i]
                end_point = star_points[(i + 1) % len(star_points)]
                Line(points=[start_point[0],start_point[1], end_point[0], end_point[1]], width=2)

            for connection in self.inner_connections:
                start_point = star_points[connection[0]]
                end_point = star_points[connection[1]]
                Line(points=[start_point[0], start_point[1], end_point[0], end_point[1]], width=2)
                
            # Color(232/255, 190/255, 172/255)  # Set the SKIN color
            for point in lis:
                Color(point.color[0]/255,point.color[1]/255,point.color[2]/255)
                Ellipse(pos=(point.x - 30,point.y -30 ), size=(60, 60))
            
            Color(255/255,100/255,0)
            if(out_crows>0):
                Ellipse(pos=pseudopos, size=(60, 60)) #psedo ,click first, while taking bird first time ,if out_crows are 0 makes no sense to display it
        
        # label1_pos = (50, self.height - 80)  # Position of label1 (top left)
        # label2_pos = (50, self.height - 110)  # Position of label2 (below label1)
        label1_pos = (Window.width * 0.05, Window.height * 0.9)  # 5% from left, 90% from bottom
        label2_pos = (Window.width * 0.05, Window.height * 0.85)  # 5% from left, 85% from bottom

        # Create and add the label widget
        self.label1 = Label(text=todisplay, font_size=24, pos=label1_pos)
        self.add_widget(self.label1)

        self.label2 = Label(text=displayplayer, font_size=24, pos=label2_pos)
        self.add_widget(self.label2)
        
        if(len(buffer)==1):
            self.label3 = Label(text="intial pos selected", font_size=27, pos=(Window.width*0.30,Window.height*0.35))
            self.add_widget(self.label3)
        



    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def update_display(self, dt):
        # Function to update the display
        self.label1.text = todisplay
        self.label2.text = displayplayer
        # self.canvas.clear()  # Clear the canvas
        self.draw_star()     # Redraw the star with updated colors
      
    
    def on_touch_down(self, touch):
        # if touch.button == 'left'  :
            print(f"Mouse left click at ({touch.x}, {touch.y})")
            for i in range(len(star_points)):
                if m.pow((touch.x-star_points[i][0]),2)+m.pow((touch.y-star_points[i][1]),2)<=m.pow(60,2): 
                    # lis[i].color=(140,0,255)
                    print("ind:  ",i)
                    buffer.append(i)
                    # self.text = i  # Update self.text
                    # self.label.text = f"Hello, Kivy!{self.text}"  # Update the label text
            
            if out_crows>0 and m.pow((touch.x-pseudopos[0]),2)+m.pow((touch.y-pseudopos[1]),2)<=m.pow(60,2): 
                    # lis[i].color=(140,0,255)
                    print("ind:  -1")
                    buffer.append(-1)

            if(len(buffer) == 2):
                print(buffer)
                # Clock.schedule_once(lambda dt: self.update_display, 0)  # Schedule GUI update
#########################################################################













class StarApp(App):
    def build(self):
        # return Star()
        star_widget = Star()
        Clock.schedule_interval(star_widget.update_display, 0.1)  # Schedule display update every 0.1 seconds
        return star_widget



# class StarAppThread(threading.Thread):
#     def run(self):
#         StarApp().run()
#         print("below run ")
#         global stop
#         stop=True#after pygame stopped



if __name__ == '__main__':
    threading.Thread(target=main).start()
    # star_app_thread = StarAppThread()
    # star_app_thread.start()
    StarApp().run()
    stop=True #after pygame stopped
    