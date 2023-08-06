from pyrace.setting import Setting
from pyrace.model.modelregistery import ModelRegistery
from pyrace.model.car import Car
import numpy

class Model:
    def __init__(self, model_name, vue):

        self.metadata = ModelRegistery.METADATA[model_name]

        self.vue = vue
        self.car = Car(self.vue.metadata, self.metadata)
        
        self.progress = 0
        self.idx_proj = 0
        
        self.state = self.car.get_state(self.vue)
        self.reward = 0
        self.done = False
        self.info = {'status' : 'racing'}
        self.history = [(self.state, self.reward, self.done, self.info)]


    def step(self, action):
        
        if self.car.step(action) :

            self.state = self.car.get_state(self.vue)

            progress, idx_proj = self.vue.get_progress(self.car.position)
            

            if (self.idx_proj==0) and (idx_proj==len(self.vue.schema)-2):
                self.done = True
                self.info['status'] = 'false departure'

            if not self.vue.is_road(self.car.position):
                self.done = True
                self.info['status'] = 'crached'

            if self.idx_proj > len(self.vue.schema)-2:
                self.done = True
                self.info['status'] = 'completed'

            if numpy.abs(progress - self.progress) < 200 :  # sometime the projection is not right.........
                self.reward = progress - self.progress
                self.progress = progress
            else :
                self.progress += self.reward

            self.idx_proj = idx_proj
            
            self.history.append((self.state, self.reward, self.done, self.info))
            return self.state, self.reward, self.done, self.info

        else :
            return None







    
