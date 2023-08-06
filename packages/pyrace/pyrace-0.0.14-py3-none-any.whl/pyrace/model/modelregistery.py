
class ModelRegistery:

	METADATA = {

		'car_v1' : {
			'model_name' : 'car_v1',
			'description' : 'In this model the car have 5 sensors and a discret action space',
			'observation_space' : {'name' : 'basic_sensor',
										'observer_type' : 'Camera',
										'dimension' : (5,),
										'values_type' : 'float',
										'values_range' : [0, 20]
			},
			'action_space' : {'descritpion' : 'Discret orientation and discret acceleration',
								'type': 'discret',
								'dimension' : (3,),	
								'actioner_names' : ['accelerator', 'breaks', 'wheel_orientation'],
								'actioner_types' : {'accelerator': 'int', 'breaks': 'int', 'wheel_orientation': 'int'},
								'actioner_ranges' :  {'accelerator': {0, 1, 2, 5}, 'breaks': {0, 1, 2, 5}, 'wheel_orientation':{-70, -50, -20, 0, 20, 50, 70}}

			}
		},

		'car_v2' : {
			'model_name' : 'car_v2',
			'description' : 'In this model the car have 5 sensors and a continuous action space',
			'observation_space' : {'name' : 'basic_sensor',
										'observer_type' : 'Camera',
										'dimension' : (5,),
										'values_type' : 'float',
										'values_range' : [0, 20]
			},
			'action_space' : {'descritpion' : 'Discret orientation and discret acceleration',
								'type': 'discret',
								'dimension' : (3,),	
								'actioner_names' : ['accelerator', 'breaks', 'wheel_orientation'],
								'actioner_types' : {'accelerator': 'float', 'breaks': 'float', 'wheel_orientation': 'float'},
								'actioner_ranges' :  {'accelerator': [0, 1], 'breaks': [0, 1], 'wheel_orientation':[-90, 90]}


			}
		},
		'QL' : {
			'model_name' : 'QL',
			'description' : 'In this model the car have 5 sensors and a continuous action space',
			'observation_space' : {'name' : 'binary_sensor',
										'observer_type' : 'Camera',
										'dimension' : (3,),
										'values_type' : 'binary',
										'values_range' : [0, 15]
			},
			'action_space' : {'descritpion' : 'Discret orientation and discret acceleration',
								'type': 'discret',
								'dimension' : (3,),	
								'actioner_names' : ['accelerator', 'breaks', 'wheel_orientation'],
								'actioner_types' : {'accelerator': 'float', 'breaks': 'float', 'wheel_orientation': 'float'},
								'actioner_ranges' :  {'accelerator': [0, 10], 'breaks': [0, 10], 'wheel_orientation':[-90, 90]}


			}
		}
		

	}