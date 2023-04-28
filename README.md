# scicomp-p1-ant-model
## Model Introduction
This model is a simulation of ant behavior based off of two papers.
1. Watmough, James, and Leah Edelstein-Keshet. "Modelling the formation of trail networks by foraging ants." Journal of Theoretical Biology 176.3 (1995): 357-371.
2. Sumpter, D. J. T. and Beekman, M. (2003). From nonlinearity to optimality: pheromone trail foraging by ants. Anim. Behav. 66, 273-280
This agent based model is an extension of the model from Watmough et al. and includes pheromone trail forming and following as well as food gathering. In particular, this model aims to recreate foraging ant behaviors by using differential pheromone deposition. It includes negative feedback, where ant will deposit less pheromone on more sautrated trails, and positive feedback, where an ant will deposit more pheromone when retuning from a foodsource. These feedback systems were meant to recreate the food-source visiting behavior shown in Sumpter et al. 

## Running the Code
The V2 directory contain the most up to date code for this model (V1 code will run but its features are not complete.) The code only requires `matplotlib`, `pandas`, and `numpy` to be installed as all other dependencies come pre-installed in python. To run the model simply run `model.py` in the V2 folder. `model.py` will display the final pheromone trails once it has completed running. 

`model.py` will create a csv file called `data.csv`. Once this file is create you can run `data_processing.py` to view a graph of the number of visits to each food source per minute. This is intended to be analogous to Figure 1 from Sumpter et al., although it does not (yet) include averaging over multple trial that the original paper did. 

## Assumtions and Limitations of the Model
This model is an intentionally limited model which was intended to try to reporduce way that ant optimize their foraging to not send to many ants to limited food sources. It included very limited pheromone and food sensing capabilitilies (ants could only detect pheromone and food that was in the three cells in front of them) which is not accurate to real ant abilities as they can actually sense food meter or even kilometers away(Sumpter et al.) It also had numerous other assumptions including the ants move at a constant speed, infinite ant can exist on the same space, all spaces are inhabitable, ant never get lost returning to the nest, etc. Instead this model mainly focused on pheromone deposting behaviors and tweaking simply feedback system to try to recreate real world behviors. 