# STATINF

## 1. Installation
[![Downloads](https://pepy.tech/badge/statinf)](https://pepy.tech/project/statinf)
[![PyPI version](https://badge.fury.io/py/statinf.svg)](https://pypi.org/project/statinf/)

You can get statinf from [PyPI](https://pypi.org/project/statinf/) with:

```bash
pip install statinf
```

`statinf` is a library for statistics and causal inference.
It provides main the statistical models ranging from the traditional OLS to Neural Networks.

The library is supported on Windows, Linux and MacOs.



## 2. Documentation

You can find the full documentation at [https://www.florianfelice.com/statinf](https://www.florianfelice.com/statinf?orgn=github).


## 3. Regressions

You can find the below examples and many more on [https://www.florianfelice.com/statinf](https://www.florianfelice.com/statinf?orgn=github).

### 3.1. OLS

`statinf` comes with the OLS regression implemented with the analytical formula:

![(X'X)^{-1}X'Y](https://latex.codecogs.com/svg.latex?\Large&space;x=(X'X)^{-1}X'Y)



```python
from statinf.regressions.LinearModels import OLS
from statinf.data.GenerateData import generate_dataset

# Generate a synthetic dataset
data = generate_dataset(coeffs=[1.2556, -6.465, 1.665414, 1.5444], n=1000, std_dev=1.6)

# We set the OLS formula
formula = "Y ~ X0 + X1 + X2 + X3"
# We fit the OLS with the data, the formula and without intercept
ols = OLS(formula, df, fit_intercept=True)

ols.summary()
```

The output:

```bash
=========================================================================
                               OLS summary                               
=========================================================================
| R² = 0.99129                  | Adjusted-R² = 0.99126
| n  =   1000                   | p =     4
| Fisher = 37790.52477                         
=========================================================================
Variables  Coefficients  Standard Errors    t values  Probabilites
       X0      1.234759         0.020300   60.824688           0.0
       X1     -6.475338         0.009052 -715.327289           0.0
       X2      1.662661         0.020141   82.552778           0.0
       X3      1.519622         0.020319   74.787592           0.0
```


### 3.2. Logistic regression

The logistic regression can be used for binary classification where ![Y](https://latex.codecogs.com/svg.latex?\Large&space;Y) follows a Bernoulli distribution. With ![X](https://latex.codecogs.com/svg.latex?\Large&space;X) being the matrix of regressors, we have:

![p=\mathbb{P}(Y=1)=\dfrac{1}{1+e^{-X\beta}}](https://latex.codecogs.com/svg.latex?\Large&space;p=\mathbb{P}(Y=1)=\dfrac{1}{1+e^{-X\beta}})


We then implement the regression with:

```python
from statinf.regressions.glm import GLM
from statinf.data.GenerateData import generate_dataset

# Generate a synthetic dataset
data = generate_dataset(coeffs=[1.2556, -6.465, 1.665414, -1.5444], n=2500, std_dev=10.5, binary=True)

# We split data into train/test/application
train = data.iloc[0:1000]
test = data.iloc[1001:2000]


# We set the linear formula for Xb
formula = "Y ~ X0 + X1 + X2 + X3"
logit = GLM(formula, train, test_set=test)

# Fit the model
logit.fit(plot=True, epochs=1000, verbose=True)

logit.get_weights()
```

The ouput:

```python
{'weights': array([ 0.00999791, -0.03512158,  0.00404969, -0.01669436]), 'bias': array(-0.12849798)}
```


### 3.3. Multi Layer Perceptron

You can train a Neural Network using the `MLP` class.
The below example shows how to train an MLP with 1 single linear layer. It is equivalent to implement an OLS with Gradient Descent.

```python
from statinf.data.GenerateData import generate_dataset
from statinf.ml.neuralnetwork import MLP, Layer

# Generate the synthetic dataset
data = generate_dataset(coeffs=[1.2556, -6.465, 1.665414, 1.5444], n=1000, std_dev=1.6)

Y = ['Y']
X = [c for c in data.columns if c not in Y]

# Initialize the network and its architecture
nn = MLP()
nn.add(Layer(4, 1, activation='linear'))

# Train the neural network
nn.train(data=data, X=X, Y=Y, epochs=1, learning_rate=0.001)

# Extract the network's weights
print(nn.get_weights())
```

Output:

```python
{'weights 0': array([[ 1.32005564],
       [-6.38121934],
       [ 1.64515704],
       [ 1.48571785]]), 'bias 0': array([0.81190412])}
```