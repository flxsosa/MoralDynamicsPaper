# MoralDynamicsPaper

This repo contains all material for the paper "Moral Dynamics: Grounding Moral Judgment in Intuitive Physics and Intuitive Psychology" by Sosa, FA, et al. Please contact me if you have any questions.

### Abstract

When holding others morally responsible, we care about what they did, and what they thought. Traditionally, research in moral psychology has relied on vignette studies, in which a protagonist's actions and thoughts are explicitly communicated. While this research has revealed what variables are important for moral judgment, such as actions and intentions, it is limited in providing a more detailed understanding of exactly how these variables affect moral judgment. Using visual stimuli that allow for a more fine-grained experimental control, recent studies have proposed a direct mapping from visual features to moral judgments. We embrace the use of visual stimuli in moral psychology, but question the plausibility of a feature-based theory of moral judgment. We propose that the connection from visual features to moral judgments is mediated by an inference about what the observed action reveals about the agent's mental states. We present a computational model that formalizes moral judgments of agents in visual scenes, as computations over an intuitive theory of physics combined with an intuitive theory of mind. Knowing what mental states lead to actions, and that these actions are constrained by physics, allows an observer to make powerful inferences about moral responsibility. Two experiments show that this model captures moral judgments about visual scenes, both qualitatively and quantitatively.

![Banner](figures/banner.png)

# Repo Structure

```bash
├── code
│   ├── Blender
│   ├── R
│   ├── javascript
│   │   ├── experiment_1
│   │   ├── experiment_2
│   │   └── experiment_3
│   ├── om
│   └── python
├── data
│   ├── empirical
│   ├── json
│   │   ├── experiment_1
│   │   ├── experiment_2
│   │   └── experiment_3
│   └── model
├── figures
│   └── plots
│       ├── experiment_1
│       ├── experiment_2
│       └── experiment_3
└── videos
    ├── experiment_1
    ├── experiment_2
    └── experiment_3
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
* ```handlers.py``` contains necessary collision handlers for the physics engine
* ```record.py``` contains functions for recording predictions from our model
* ```convert_to_json.py``` contains methods for converting physics data from our simulation into a JSON
* ```moral_kinematics_scenarios.py``` contains the defined simulations we used in our paper
* ```features.py``` contains all of the functions for computing kinematic features from simulation JSON data
* ```video.py``` contains all of the functions for recording the simulations as videos

### Javascript

Contains all of the code for our MTurk experiments.
* ```experiment_1``` contains all code used for our first behavioral experiment
* ```experiment_2``` contains all code used for our second behavioral experiment
* ```experiment_3``` contains all code used for our third behavioral experiment

### Blender

Contains the code used to render our physical simulations into videos using Blender.

## Data

This directory contains all of the emirical and model data related to the project.
* ```empirical``` contains all empirical data from experiments 1 and 2
* ```model``` contains all model predictions
* ```json``` contains JSON files containing positional data of the agents within our simulations

## Figures

This directory contains all of the figures used in the paper "Moral Dynamics".
* ```plots``` contains the plots used to create our paper figures.
* ```videos``` contains all of the video stimuli created and used for the experiments.
