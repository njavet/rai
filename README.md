# Important
Sorry I started with my own project and therefore I didn't extend
the notebooks, I hope this is ok

# Installed pip packages

```
[tool.poetry.dependencies]
python = "^3.12"
pandas = "^2.2.3"
numpy = "^2.1.2"
jupyter = "^1.1.1"
matplotlib = "^3.9.2"
tqdm = "^4.66.6"
seaborn = "^0.13.2"
gymnasium = "^1.0.0"
pygame = "^2.6.1"
```

# Setup
I used poetry for the virtual environment 
`python rl/frozen_lake.py`


# Hyper parameters:
* learningrate = 0.05
 
slower training execution, but (hopefully?) better learning

* epsilon = 0.2
 
because of the argmax problems, I set it a bit higher
(argmax function in helpers.py)

* gamma = 0.98
 
to prefer long term advantage, I set the discounting factor high

* episodes = 10000
 
more than the initial value, again slower for training, but more "data"


# Algorithms
* MC random 
 
slow convergence, random and no temporal delta updates

* MC inc
 
improvement over the random version in terms of speed and estimation

* Q-Learning
 
better results and faster convergence (though I didn't try the 11x11 grid yet)

