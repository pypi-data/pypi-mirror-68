# mmuda_distributions: Calculate Distributions with Python

### About this package

This package is part of my Data Science course at Udacity. 

It is useful to calculate the mean and the standard deviation of Gaussian and Binomial Distributions. Furthermore it includes methods to calculate the probability density function and to plot barplots. 


### File description

* Generaldistribution.py:  Generic distribution class for calculating and visualizing a probability distribution.
* Gaussiandistribution.py: Gaussian distribution class for calculating and visualizing a Gaussian distribution.
* Binomialdistribution.py: Binomial distribution class for calculating and visualizing a Binomial distribution.


### Installation

This package relies on the `math` and `matplotlib` packages for calculation and plotting.

It can be installed the following way: 
```python
pip using pip install mmuda-distribution.
```

Then, the module can be imported and applied the following way: 
```python
from mmuda_distribution import Gaussian, Binomial
print(Gaussian(10, 7))
print(Binomial(0.4, 25))
```

### Acknowledgments

I would like to thank Udacity (and especially Juno and Andrew) who sure enough introduced already a lot of students to the field of object-oriented programming. 


### Author

Maximilian Müller, Business Development Manager in the Renewable Energy sector. Now diving into the field of data analysis.
GitHub: https://github.com/muellermax/