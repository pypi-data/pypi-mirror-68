from pyrace.model.space import Space
from pyrace.model.camera import Camera
from pyrace.setting import Setting
import numpy

import pprint
pp = pprint.PrettyPrinter(indent=4)



class Car:
    def __init__(self, vue_metadata, model_metadata):
        self.model_metadata = model_metadata

        self.action_space = Space(model_metadata, 'action')
        self.observation_space = Space(model_metadata, 'observation')

        self.position = vue_metadata['init']['position']
        self.orientation = vue_metadata['init']['orientation']

        self.speed = numpy.array([0, 0])
        self.acceleration = numpy.array([0, 0])

        self.car_actioners = {'accelerator' : 0, 'breaks' : 0, 'wheel_orientation' : 0}

        self.accelerator_sensitivity = Setting.ACCELERATIOR_SENSITIVITY
        self.breaks_sensitivity = Setting.BREAKS_SENSITIVITY


        self.observer = self.init_observer()


    def init_observer(self):
        observer_description = self.observation_space.description

        if observer_description['observer_type'] == 'Camera' :
            return Camera(observer_description)

        elif observer_description['observers_type'] == 'GPS':
            print('Coming soon !')
            return None

        elif observer_description['observers_type'] == '360_Sensor':
            print('Coming soon !')
            return None



    def get_state(self, vue):
        state = self.observer.get_value(vue, self.position, self.orientation)
        return state


    def step(self, action):
        if self.action_space.check(action):
            idx = 0
            for actioner in self.car_actioners.keys() :
                if actioner in self.action_space.description['actioner_names'] :
                    self.car_actioners[actioner] = action[idx]
                    idx += 1

            # update acceleration
            alpha = self.car_actioners['wheel_orientation']
            alpha_rad = numpy.pi*alpha/180
            accelerator_effect = self.car_actioners['accelerator']*numpy.array([-numpy.sin(alpha_rad), numpy.cos(alpha_rad)])
            breaks_effect = self.car_actioners['breaks']*numpy.array([numpy.sin(alpha_rad), -numpy.cos(alpha_rad)])
            
            self.acceleration = self.accelerator_sensitivity*accelerator_effect + self.breaks_sensitivity*breaks_effect

            # update speed
            self.speed = self.speed + Setting.TIC*self.acceleration

            # from car referential to map referential
            theta = self.orientation
            theta_rad = numpy.pi*theta/180
            rot_mat = numpy.array([[numpy.cos(theta_rad), -numpy.sin(theta_rad)], [-numpy.sin(theta_rad), -numpy.cos(theta_rad)]])
            speedxy = numpy.matmul(rot_mat, self.speed)

            # Drift effect pending dev !

            # update position and orientation
            self.position = self.position + Setting.TIC*speedxy
            self.orientation = alpha + theta

            return True
        else :
            print('Input action does not match action space : \n')
            pp.pprint(self.action_space.description)
            return False





