
from pyrace.setting import Setting
from pyrace.vue.mapregistery import MapRegistery

from PIL import Image
import numpy


def proj(x, x_1, x_2):
    scal = numpy.dot(x-x_1, x_2-x_1)/numpy.dot(x_2-x_1, x_2-x_1)
    p = x_1 + scal*(x_2-x_1)
    return p.astype(int)

def edist(x_1, x_2):
    return numpy.sqrt(numpy.sum((x_2-x_1)**2))


def inter_dist(p, x_1, x_2, e=0.001, K=10):
    alpha = edist(p, x_1)
    beta = edist(p, x_2)
    d = edist(x_1, x_2)

    x = numpy.max([(numpy.abs(alpha-beta)/d)-1+e, 0])
    return numpy.exp((K/e)*x)


class Vue:
    def __init__(self, map_name):

        self.metadata = MapRegistery.METADATA[map_name]
        sub_path = "data/"+map_name+".jpg"

        self.map_img = Image.open(Setting.CWD / sub_path)
        self.map_img_rgb = self.map_img.convert('RGB')

        self.car_img = Image.open(Setting.CAR_IMG_PATH)

        self.marker_img = Image.open(Setting.MARKER_IMG_PATH).resize((Setting.MARKER_SIZE, Setting.MARKER_SIZE))

        self.schema = self.metadata['schema']
        self.schema_numpy = numpy.array(self.schema)
        self.cum_dist_schema = numpy.cumsum([edist(self.schema_numpy[i], self.schema_numpy[i+1]) for i in range(len(self.schema)-1)])

        self.projection = (490, 520) # for plot purpose -> remove

    def is_road(self, position):
        try :
            r, g, b = self.map_img_rgb.getpixel(tuple(position))
        except IndexError :
            r, g, b = 250, 250, 250
        except :
            raise
        r_road , g_road, b_road = self.metadata['road_rgb']
        if (r-r_road)+(g-g_road)+(b-b_road) < 50 :
            return True
        else :
            return False


    def trace(self, car):

        render_car_img = self.car_img.rotate(angle=car.orientation, resample=Image.NEAREST, expand=True)
        render_img = self.map_img.copy()

        # paste with pos on upper left corner -> adjust pos
        car_img_size = numpy.array(render_car_img.size)
        car_pos = car.position
        render_pos =  (car_pos - car_img_size/2).astype(int)
        render_img.paste(render_car_img, tuple(render_pos), render_car_img)

        if car.observation_space.description['observer_type'] == 'Camera' :
                
            cursor_positions = [(x[0] + Setting.MARKER_SIZE//2 - car_img_size[0]//2, x[1] + Setting.MARKER_SIZE//2 - car_img_size[1]//2) for x in car.observer.cursor_positions]
            cursor_images = [self.marker_img.rotate(angle=theta, resample=Image.NEAREST, expand=True) for theta in car.observer.thetas]

        for point_ in self.metadata['schema'] :
            render_img.paste(self.marker_img, point_, self.marker_img)

        render_img.paste(self.marker_img, tuple(self.projection), self.marker_img)

        # elif car.observation_space.description['observer_type'] == 'GPS' :
        #     # coming soon

        # elif car.observation_space.description['observer_type'] == '360_Sensor' :
        #     # Coming soon

        return render_img



    def get_progress(self, position):

        projections = [proj(position, self.schema_numpy[i], self.schema_numpy[i+1]) for i in range(len(self.schema_numpy)-1)]
        self.projections = projections

        distproj = [edist(projections[i], position)*inter_dist(projections[i], self.schema_numpy[i], self.schema_numpy[i+1]) for i in range(len(projections))]
        idx_proj = numpy.argmin(distproj)
        projection = projections[idx_proj]

        self.projection = projection


        if idx_proj == 0 :
            dist_segment = 0
        else :
            dist_segment = self.cum_dist_schema[idx_proj - 1]


        segment = self.schema_numpy[idx_proj]

        dist_last = edist(segment, projection)
        output_dist = dist_last + dist_segment

        return output_dist, idx_proj










