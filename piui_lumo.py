'''
lumo piui interface
KGARMIRE JUN.26.2016
'''

execfile("/home/pi/lumo/lumo.py");
from piui import PiUi

class LumoUi:
    def __init__(self):
        self.title = None
        self.txt = None
        self.ui = PiUi()
        self.pattern = None
    
    def page_menu(self):
        self.page = self.ui.new_ui_page(title="LUMO Smart Lamp")
        self.list = self.page.add_list()
        self.list.add_item("Combo", chevron=True, onclick=self.page_patterns)
        self.list.add_item("Mode", chevron=True, onclick=self.page_modes)
        self.list.add_item("Turn Off", chevron=False, onclick=partial(self.uMode, "off"))
        self.ui.done()
        
    
    def page_modes(self):
        self.page = self.ui.new_ui_page(title="Mode")
        self.list = self.page.add_list()
        for mode in _modes.keys().sort():
            self.list.add_item(mode, chevron=False, onclick=partial(self.uMode, mode))
    
    def page_patterns(self):
        self.page = self.ui.new_ui_page(title="Pattern")
        self.list = self.page.add_list()
        for pattern in _patterns.keys().sort():
            self.list.add_item(pattern, chevron=True, onclick=partial(self.uPattern, pattern))
            
    def page_colors(self):
        self.page = self.ui.new_ui_page(title="Color")
        self.list = self.page.add_list()
        for color in _colors.keys().sort():
            self.list.add_item(color, chevron=False, onclick=partial(self.uColor, color))
            
    def uMode(self, c):
        goMode(c)
        self.page_menu()
        
    def uPattern(self, c):
        self.pattern = c
        self.page_colors()
        
    def uColor(self, c):
        goCombo(self.pattern, c)
        self.page_menu()
    
    def main(self):
        self.menu_page()
        self.ui.done()
        
def main():
    lumo = LumoUi()
    lumo.main()

if __name__ == "__main__":
    main();