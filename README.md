# MoralDynamicsPaper

This repo contains all material for the paper "Moral Dynamics: Grounding Moral Judgment in Intuitive Physics and Intuitive Psychology" by Sosa, FA, et al. Please contact me if you have any questions.

![Banner](figures/banner.png)

# Repo Structure

```bash
├── code
│   ├── Blender
│   ├── R
│   ├── javascript
│   │   ├── experiment_1
│   │   └── experiment_2
│   ├── om
│   └── python
├── data
│   ├── empirical
│   ├── json
│   └── model
├── figures
│   └── plots
│       ├── experiment_1
│       └── experiment_2
└── videos
    ├── experiment_1
    └── experiment_2
```

## Code

This directory contains all code related to the project.

### R

Contains all of the code used to analyze and visualize our data.
* ```analysis.R``` contains all analyses used on the data and the model
* ```analysis.html``` is a markdown file of ```analysis.R```

### Python

Contains all of the code used to develop the physical simulations for our experiments and model.
* ```agents.py``` contains base classes for the agents in our simulations
* ```environment.py``` contains base classes for the simulation environments
* ```handlers.py``` contains necessary collsion handlers for the physics engine
* ```record.py``` contains methods for recording predictions from our model
* ```convert_to_json.py``` contains methods for converting physics data from our simulation into a JSON
* ```moral_kinematics_scenarios.py``` contains the defined simulations we used in our paper

### Javascript

Contains all of the code for our MTurk experiments.
* ```experiment_1``` contains all code used for our first behavioral experiment
* ```experiment_2``` contains all code used for out second behavioral experiment

### Blender

Contains the code used to render our physical simulations into videos using Blender.

## Data

This directory contains all of the emirical and model data related to the project.
* ```empirical``` contains all empirical data from experiments 1 and 2
* ```model``` contains all model predictions
* ```json``` contains JSON files containing positional data of the agents within our simulations*

## Figures

This directory contains all of the figures used in the paper "Moral Dynamics".
* ```plots``` contains the plots used to create our paper figures.
* ```videos``` contains all of the video stimuli created and used for the experiments.
