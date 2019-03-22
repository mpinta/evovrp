# evovrp
Solving multi-depot vehicle routing problem (_MDVRP_) using evolutionary algorithms.

## Requirements
* Python 3.6+
* Pip

### Dependencies in order for the project to run are:
`numpy, imageio, matplotlib and NiaPy==2.0.0rc4`

You can install them using the `setup.py` script:
```
$ git clone https://github.com/karakatic/evovrp
$ cd evovrp
$ python setup.py install
```

## Usage
In `main.py` import any evolutionary algorithm from the NiaPy library and set the input parameters of the `main` function:
* `file_name` - directory of a dataset file,
* `algorithm` - imported evolutionary algorithm from the NiaPy library,
* `generations` - number of generations,
* `population_size` - number of instances inside one generation,
* `phenotype_coding` - genotype-to-phenotype coding method; `method.Method.FIRST` for the first and `method.Method.SECOND` for the second method.

### Example
The following code solves `pr01` MDVRP case from the `C-mdvrp` dataset using a `genetic algorithm` of `10` generations, population size of `5` and `first genotype-to-phenotype` coding method:
```python
from NiaPy.algorithms.basic.ga import GeneticAlgorithm

if __name__ == '__main__':
    main('C-mdvrp/pr01', GeneticAlgorithm, 10, 5, method.Method.FIRST)
```

### Output
Once the evaluation finishes, program returns information about the instance with the best fitness value into the console. It creates `.png` format images and associated `.gif` animations for each instance, solving the MDVRP case. Program also creates gif animation of best instances from each generation and a bar graph, showing all fitness values through generations.

## Datasets
Used datasets are taken from the University of Málaga - Networking and Emerging Optimization Groups [website about vehicle routing problem](http://neo.lcc.uma.es/vrp/):
* [Multi-depot VRP Instances](http://neo.lcc.uma.es/vrp/vrp-instances/multiple-depot-vrp-instances/)
* [Multiple Depot VRP with Time Windows Instances](http://neo.lcc.uma.es/vrp/vrp-instances/multiple-depot-vrp-with-time-windows-instances/)

Both used datasets are designed by **Cordeau**.

#### Disclaimer
_The goal of the project is not optimization of evolutionary algorithms, but the use of different algorithms to solve the multi-depot vehicle routing problem._
