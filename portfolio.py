import numpy as np
import pandas as pd
from typing import Callable

def previous_best(past_weights: np.ndarray, past_price_relatives: np.ndarray) -> np.ndarray:
  '''
  Greedy strategy that places all of the weight on the best past_price_relative..
  '''
  new_weights = np.zeros_like(past_weights)
  new_weights[np.argmax(past_price_relatives)] = 1.0
  return new_weights

def constant_weights(past_weights: np.ndarray, past_price_relatives: np.ndarray) -> np.ndarray:
  '''
  Constant weights
  '''
  return past_weights

def softmax(logits: np.ndarray) -> np.ndarray:
  '''
  Input logits are (N,)
  '''
  exp_logits = np.exp(logits - logits.max())
  return exp_logits / exp_logits.sum()

class ExponentiatedGradient:
  '''
  Exponentiated gradient optimizer
  '''

  def __init__(self, learning_rate: float = 0.05):
    self.learning_rate = learning_rate

  def step(self, past_weights: np.ndarray, past_price_relatives: np.ndarray) -> np.ndarray:
    '''
    Inputs
        past_weights is (N,)
        past_price_relatives is (N,)
    Outputs
        new_weights is (N,)
    '''
    return softmax(np.log(past_weights) + self.learning_rate * past_price_relatives / np.inner(past_weights, past_price_relatives))

  def __call__(self, past_weights: np.ndarray, past_price_relatives: np.ndarray) -> np.ndarray:
    return self.step(past_weights, past_price_relatives)

class Portfolio:
  '''
  Constantly-rebalancing portfolio
  '''
  def __init__(self, wealth: float,
               weights: pd.Series,
               update_rule: Callable):
    self.wealth = wealth
    self.weights = weights
    self.update_rule = update_rule
    self.log_wealth_factor = 0.0
    self.price_relatives = None
    self.timestamp = None
    return None

  def update(self, new_price_relatives: pd.Series):
    '''
    Move forward to the next day and update portfolio.
    Inputs:
      new_price_relatives -- pd.Series of the price relatives revealed at the close of the day
    '''
    # step 1: update portfolio weights
    if self.price_relatives is not None:
      new_weights = self.update_rule(self.weights.to_numpy(), self.price_relatives.to_numpy())
      self.weights = pd.Series(data = new_weights, index = self.weights.index)

    # step 2: update current price relatives and log wealth factor
    self.log_wealth_factor += np.log( np.inner(self.weights.to_numpy(), new_price_relatives.to_numpy()) )
    self.timestamp = new_price_relatives.name
    self.price_relatives = new_price_relatives
    return None

  def get_current_wealth(self) -> float:
    return self.wealth * self.get_wealth_factor()

  def get_wealth_factor(self) -> float:
    return np.exp(self.log_wealth_factor)

# class OraclePortfolio:
#   '''
#   Constantly-rebalancing portfolio that sees the future before it happens
#   '''
#   def __init__(self, wealth: float,
#                weights: pd.Series):
#     self.wealth = wealth
#     self.weights = weights
#     self.log_wealth_factor = 0.0
#     self.price_relatives = None
#     self.timestamp = None
#     return None

#   def update(self, new_price_relatives: pd.Series):
#     '''
#     Move forward to the next day and update portfolio.
#     Inputs:
#       new_price_relatives -- pd.Series of the price relatives revealed at the close of the day
#     '''
#     # step 1: update portfolio weights
#     # the oracle uses the new_price_relatives to choose weights

#     new_weights = np.zeros((len(self.weights),))
#     new_weights[new_price_relatives.argmax()] = 1.0
#     self.weights = pd.Series(data = new_weights, index = self.weights.index)

#     # step 2: update current price relatives and log wealth factor
#     self.log_wealth_factor += np.log( np.inner(self.weights.to_numpy(), new_price_relatives.to_numpy()) )
#     self.timestamp = new_price_relatives.name
#     self.price_relatives = new_price_relatives
#     return None

#   def get_current_wealth(self):
#     return self.wealth * self.get_wealth_factor()

#   def get_wealth_factor(self):
#     return np.exp(self.log_wealth_factor)