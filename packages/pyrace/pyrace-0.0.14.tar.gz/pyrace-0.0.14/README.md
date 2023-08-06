
<h1> pyrace </h1>
This library provides a flexible environment to practice different Reinforcment learning models.
</br>
<h3> Import </h3>

```sh
from pyrace import Env
```
<h3> Creat an environment </h3>

```sh
env = Env()
```

<h3> Env class </h3>
The methods of this class are pretty similar to the environments provided by the gym library.
</br>
<b>render</b> : print an image of the current state of the environment. please make sure to turn the backend of matplotlib to auto (%matplotlib Auto)
</br>
<b>reset</b> : reset the environment and output tu initial state.
</br>
<b>step</b> : takes an action as input. An action is an array, the size and types in this array are defined by the environment's action space.This method outputs the new state.
</br>
<b>load</b> : Input the name of a map and it reset the environment with this new map loaded. Currently only one map is ready (map_1).So, this method is not that useful currently.
</br>
<b>sample_action</b> : no input, it output a random sample of the current environement's action space.
</br>
<b>get_model_info</b> : print the current environment's metadata. This metadata gives a description of the action space and the observation space.
</br>
<b>get_model_list</b> : gives the list of the names of the different available models.
</br>
<b>get_map_list</b> : gives the list of the names of the maps available.