import pyray as rl
from textureHandler import TextureHandler
#from Settings import *
import Settings

def drawButton(text, font_size, height, isSelected, rect_height = 100):
    text_width = rl.measure_text(text, font_size)
    center_x = (Settings.width - text_width) / 2
    center_y = height
    color = (64,74,120, 255) if isSelected else (0, 0, 0, 255)
    rl.draw_rectangle(int(center_x-10), int(center_y-10), text_width+20, rect_height, color)  # Black text
    rl.draw_text(text, int(center_x), int(center_y), font_size, (156,155,135, 255))  # Black text

class UI:
    def __init__(self) -> None:
        self.font = rl.get_font_default()
        self.isOn = True
        self.deadPlayer = False
        self.nItems = 3
        self.selected = 1
        self.currPage = 0
    def update(self):
        #print(self.selected)
        if rl.is_key_pressed(rl.KEY_ENTER):
            if self.deadPlayer and self.selected == 0:
                self.deadPlayer = False
                return
            if self.deadPlayer:
                self.deadPlayer = False
                self.selected = 0
            if (self.selected == 0):
                self.isOn = False
            if self.currPage == 1 and self.selected == 2:
                self.currPage = 0
                rl.close_window()
                TextureHandler.unbind()
                Settings.width = int(Settings.width)
                Settings.height = int(Settings.height)
                rl.init_window(Settings.width, Settings.height, "Infinite doppelganger")
                TextureHandler.bind()
                return -1
            else:
                self.currPage = self.selected
            return self.currPage

        if rl.is_key_pressed(rl.KEY_UP):
            self.selected = self.nItems-1 if self.selected <= 0 else self.selected-1
        if rl.is_key_pressed(rl.KEY_DOWN):
            self.selected = 0 if self.selected >= self.nItems-1 else self.selected+1
        if self.currPage == 1 and rl.is_key_down(rl.KEY_LEFT):
            if self.selected == 0:
                Settings.width -= 0.1
            if self.selected == 1:
                Settings.height -= 0.1
        if self.currPage == 1 and rl.is_key_down(rl.KEY_RIGHT):
            if self.selected == 0:
                Settings.width += 0.1
            if self.selected == 1:
                Settings.height += 0.1


        return -1
    def drawText(self, text, font_size = 100, text_height = Settings.height/8):
        text_width = rl.measure_text(text, font_size)
        center_x = (Settings.width - text_width) / 2
        center_y = text_height
        #rl.draw_rectangle(int(center_x-10), int(center_y-10), text_width+20, 100, color)  # Black text

        rl.draw_text(text, int(center_x), int(center_y), font_size, (156,155,135, 255))  # Black text



    def drawSettings(self):
        text = "Settings"
        font_size = 100 # Adjust as needed

        text_width = rl.measure_text(text, font_size)
        center_x = (Settings.width - text_width) / 2
        center_y = Settings.height / 8  

        rl.draw_texture_pro(TextureHandler.get("background"), (0, 0, 1024, 1024), (0, 0, Settings.width, Settings.height), (0, 0), 0, (255, 255, 255, 255))
        rl.draw_rectangle(int(center_x-10), int(center_y-10), text_width+20, 120, (64,74,120, 255))  # Black text
        self.drawText(text)

        drawButton("Width: " + str(int(Settings.width)), 50, Settings.height/8 + 200, self.selected == 0, 80)
        drawButton("Height: " + str(int(Settings.height)), 50, Settings.height/8 + 300, self.selected == 1, 80)
        drawButton("Apply", 50, Settings.height/8 + 400, self.selected == 2, 80)


        #self.drawText(text, 50, height/8 + 200)
    def drawMain(self):
        font = rl.get_font_default()
        text = "Infinite doppleganger"
        font_size = 100 # Adjust as needed

        text_width = rl.measure_text(text, font_size)
        center_x = (Settings.width - text_width) / 2
        center_y = Settings.height / 8  

        # Draw background
        rl.draw_texture_pro(TextureHandler.get("background"), (0, 0, 1024, 1024), (0, 0, Settings.width, Settings.height), (0, 0), 0, (255, 255, 255, 255))
        rl.draw_rectangle(int(center_x-10), int(center_y-10), text_width+20, 120, (64,74,120, 255))  # Black text
        # Draw centered text
        rl.draw_text(text, int(center_x), int(center_y), font_size, (156,155,135, 255))  # Black text
        scale = 140
        center_y += 200 
        drawButton("Start", 60, center_y+scale*1, self.selected == 0)
        drawButton("Settings", 60, center_y+scale*2, self.selected == 1)
        drawButton("Exit", 60, center_y+scale*3, self.selected == 2)
    def drawDeathScreen(self):
        font = rl.get_font_default()
        text = "You're dead"
        font_size = 100 # Adjust as needed

        text_width = rl.measure_text(text, font_size)
        center_x = (Settings.width - text_width) / 2
        center_y = Settings.height / 8  

        rl.draw_text(text, int(center_x), int(center_y), font_size, (156,155,135, 255))  # Black text
        scale = 140
        center_y += 200 
        drawButton("Go to settings", 60, center_y+scale*1, self.selected == 0)
        drawButton("Restart", 60, center_y+scale*2, self.selected == 1)



    def draw(self):
        if self.deadPlayer == True:
            self.drawDeathScreen()
        elif self.currPage == 0:
            self.drawMain()
        elif self.currPage == 1:
            self.drawSettings()



        


