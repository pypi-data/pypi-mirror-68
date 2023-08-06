
import numpy
import random

class Space:
    def __init__(self, model_metadata, space_type):
        self.description = model_metadata[space_type+'_space']
        self.space_type = space_type

    def sample(self):
        sample = numpy.zeros(self.description['dimension'])
        for i, actioner in enumerate(self.description['actioner_names']):
        	actioner_type, actioner_range = self.description['actioner_types'][actioner], self.description['actioner_ranges'][actioner]
        	if actioner_type == 'int':
        		sample[i] = random.choice(list(actioner_range))
        	elif actioner_type == 'float':
        		sample[i] = actioner_range[0] + (actioner_range[1]-actioner_range[0])*random.random()
        return sample


    def check(self, input_):
        flag = True
        try :
            for i, actioner in enumerate(self.description['actioner_names']):
            	actioner_type, actioner_range = self.description['actioner_types'][actioner], self.description['actioner_ranges'][actioner]
            	if actioner_type == 'int':
            		if int(input_[i]) != input_[i] or input_[i] not in actioner_range :
            			flag = False
            			break
            	elif actioner_type == 'float':
            		if input_[i] < actioner_range[0] or input_[i] > actioner_range[1]:
            			flag = False
            			break
        except :
            flag = False
        return flag


