from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from kivy.clock import Clock
from kivy.core.window import Window
import threading
from utils import imagecreation 
Window.size = (480,320)

class CarouselApp(App):
    def build(self, *args):
        self.title = "Egg, Inc. Display"
        self.fuck = 0 
        self.refreshClock = None
        self.updateImageClock = None
        #Clock.schedule_once(self.create)
        if not self.refreshClock:
            self.refreshClock = Clock.schedule_interval(self.changeWidget, 10)
        if not self.updateImageClock:
            self.updateImageClock = Clock.schedule_interval(self.startImageUpdate, 10)
        self.carosel = self.create()
        return self.carosel

    def startImageUpdate(self, *args):
        threading.Thread(target=imagecreation.genImages).start()
    
    def create(self, *args, mini = False):
        print("updating ui")
        #imagecreation.genImages()
        miniReturn = []
        carousel = Carousel(direction='right')
            #src = "http://placehold.it/480x320.png&text=slide-%d.png" % i
            #image = AsyncImage(source=src, fit_mode="contain")
        carousel.loop = True
        image = Image(source="assets/output/home.png")
        if mini:
            miniReturn.append(image)
        else:
            carousel.add_widget(image)

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for i in range(100):
            btn = Button(text=str(i), size_hint_y=None, height=40)
            layout.add_widget(btn)
        
        
        
        root = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        root.add_widget(layout)
        if mini:
            miniReturn.append(root)
        else:
            carousel.add_widget(root)
        if mini: 
            return miniReturn
        else:
            return carousel
    
    def changeWidget(self, *args):
        self.fuck += 1
        currentTab = self.root.index
        self.root.clear_widgets()
        for wid in self.create(mini=True):
            self.root.add_widget(wid)
        self.root.index = currentTab


CarouselApp().run()