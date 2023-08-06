
from pyrace.model import Model
from pyrace.vue import Vue
from pyrace.setting import Setting
from pyrace.model.modelregistery import ModelRegistery
from pyrace.vue.mapregistery import MapRegistery
import matplotlib.pyplot as plt
import numpy
import pprint
pp = pprint.PrettyPrinter(indent=4)

import sys,tty,termios
class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
                return "up"
        elif k=='\x1b[B':
                return "down"
        elif k=='\x1b[C':
                return "right"
        elif k=='\x1b[D':
                return "left"
        else:
                return "exit"



class Env:
    def __init__(self, model_name=''):

        self.vue = Vue(Setting.MAP_INIT)
        try :
            self.model = Model(model_name, self.vue)
            self.model_name = model_name
        except KeyError :
            print('Please enter a valide model name. Select one of the following model en reload Environment\n')
            self.get_model_list()
            self.model = Model(Setting.MODEL_INIT, self.vue)
            self.model_name = Setting.MODEL_INIT
        except :
            raise 

        self.action_space = self.model.car.action_space
        self.observation_space = self.model.car.observation_space

     

    def load(self, new_map_name=''):
        if new_map_name in list(MapRegistery.METADATA.keys()) :
            self.vue = Vue(new_map_name)
            print ('Map {} loaded and a new enviroment ready !'.format(new_map_name))
            _ = self.reset()
        else :
            print('Please type a valide map name : \n')
            self.get_map_list()
        return None


    def sample_action(self):
        return self.model.car.action_space.sample()


    def step(self, action):
        output = self.model.step(action)
        return output

    def render(self):
        if not plt.fignum_exists(1) :
            self.fig, self.ax = plt.subplots()
            self.render_img = self.ax.imshow(self.vue.map_img)

        built_img = self.vue.trace(self.model.car)
        self.render_img.set_data(built_img) 
        self.fig.canvas.draw_idle()
        plt.axis('off')
        plt.pause(1/Setting.FRAME_FREQ)


    def reset(self):
        plt.close()
        self.model = Model(self.model_name, self.vue)
        self.action_space = self.model.car.action_space
        self.observation_space = self.model.car.observation_space
        return self.model.state


    def control(self):
        exit = False
        self.render()
        self.step([0, 0, 0])
        score = 0
        while not exit :
            key = get()
            if key == "up":
                a = [5, 0, 0]
            elif key == "down":
                a = [0, 1, 0]
            elif key == "right":
                a = [0, 0, -20]
            elif key == "left":
                a = [0, 0, 20]
            else :
                exit = True
            _, reward, _, info = self.step(a)
            score += reward
            print(score, info)
            self.render()




    def get_model_info(self):
        pp.pprint(ModelRegistery.METADATA[self.model_name])


    def get_model_list(self):
        print(ModelRegistery.METADATA.keys())

    def get_map_list(self):
        print(MapRegistery.METADATA.keys())



