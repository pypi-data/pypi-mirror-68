import numpy
from pyrace.setting import Setting

class Camera:
        def __init__(self, observer_metadata):

            self.metadata = observer_metadata
            self.nb_cams = observer_metadata['dimension'][0]
            self.cams_range = observer_metadata['values_range'][1]
            self.thetas = [int(180/self.nb_cams*i) for i in range(-(self.nb_cams//2), 1+self.nb_cams//2)]


        def get_value(self, vue, position, orientation):
            x, y = position
            cursor_orientations = [orientation+theta for theta in self.thetas]
            self.cursor_positions = [(x-int(self.cams_range*numpy.sin(numpy.pi*(angle)/180)), y-int(self.cams_range*numpy.cos(numpy.pi*(angle)/180))) for angle in cursor_orientations]
            # values = [vue.map_img_rgb.getpixel(cursor_position)[2] for cursor_position in self.cursor_positions]
            values = []
            for cursor_position in self.cursor_positions :
                try :
                    value = vue.map_img_rgb.getpixel(cursor_position)[2]
                except IndexError :
                    value = 240
                except :
                    raise
                
                if self.metadata['values_type']=='binary':
                    if numpy.abs(value - Setting.ROAD_COLOR) < 20 :
                        value = 1
                    else :
                        value = 0

                values.append(value)
            return values