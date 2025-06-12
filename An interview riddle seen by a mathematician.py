#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[179]:


# For plotting
try:
    get_ipython().run_line_magic('matplotlib', 'inline')
except NameError:
    import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize'] = (12, 6)

# For simulations
import random
random.seed(42)

# For data handling
import numpy as np
import pandas as pd

# For flattening lists through itertools.from_iterable.chain()
import itertools


# # Solve the riddle

# ##### To know which trader presses which bulb, we need to know the number of divisors of each number between 1 and 100

# In[26]:


# From https://stackoverflow.com/questions/171765/what-is-the-best-way-to-get-all-the-divisors-of-a-number
# 3rd answer

def divisors(n):
    """Optimized divisor calculation using square root approach - O(√n) complexity"""
    divisors_list = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors_list.append(i)
            if i != n // i:
                divisors_list.append(n // i)
    return sorted(divisors_list)

def count_divisors_bulk(max_n):
    """Count divisors for all numbers 1 to max_n efficiently using sieve approach"""
    divisor_counts = [0] * (max_n + 1)
    for i in range(1, max_n + 1):
        for j in range(i, max_n + 1, i):
            divisor_counts[j] += 1
    return divisor_counts


# In[32]:


bulbs_switched_by_traders = {bulb: list(divisors(bulb)) for bulb in range(1,101)}


# In[38]:


# Which traders press the switch of light bulb number 4. Note that the number of traders is odd: the bulb is turned on.
bulbs_switched_by_traders[4]


# In[41]:


# Which traders press the switch of light bulb number 85. The number of traders is even. The bulb is turned off.
bulbs_switched_by_traders[85]


# In[79]:


# See which bulbs are turned on, which are turned off
bulbs_turned_on = {bulb: len(traders) % 2 == 1 for (bulb, traders) in bulbs_switched_by_traders.items()}
# x % 2 == 1 tests whether x is odd. It means "does x % 2 equal 1?", where % is the modulo operator
bulbs_turned_on


# In[89]:


# Finding the actual number of bulbs turned on
sum(bulbs_turned_on.values())


# # Bringing randomness into the game

# ##### Now the probability to switch the light is p, where 0 ≤ p ≤ 1

# In[52]:


# Instead of working on which traders presses which bulb, we count the number of traders by bulb who would press its switch
count_traders_by_bulb = {bulb: len(traders) for (bulb, traders) in bulbs_switched_by_traders.items()}


# In[53]:


# How many traders press the switch of light bulb number 4 with probability p
count_traders_by_bulb[4]


# In[54]:


# How many traders press the switch of light bulb number 85 with probability p
count_traders_by_bulb[85]


# ### Execute simulations with several values of p

# ##### The number of traders pressing the switch of a bulb follows a Binomial probability law, since pressing the switch follows a Bernoulli law

# In[58]:


def simulate_riddle(p):
    return {bulb: sum(np.random.binomial(count_traders, p, 1)) % 2 == 1 
            for (bulb, count_traders) in count_traders_by_bulb.items()}


# In[121]:


# Check that we find the same results than before when p = 1.
simulation = simulate_riddle(1)
print("Number of bulbs turned on: "+ str(sum(simulation.values())))
simulation


# In[120]:


# Check with p = 0 that all bulbs are turned OFF of course
simulation = simulate_riddle(0)
print("Number of bulbs turned on: "+ str(sum(simulation.values())))
simulation


# In[119]:


# Test with p = 0.5, or whatever you want. For easier use of Jupyter notebook, use Ctrl + Enter to run several simulations
simulation = simulate_riddle(0.5)
print("Number of bulbs turned on: "+ str(sum(simulation.values())))
simulation


# In[133]:


def distribution(p, n_simulations=500):
    return pd.DataFrame([sum(simulate_riddle(p).values()) for i in range(n_simulations)])


# In[181]:


# Get the distribution of the number of turned on light bulbs with p = 0.5
distribution(0.5, 1000).hist(bins=100)


# In[231]:


# Get the distribution with p varying from 0 to 1 incrementally. It should take less than 20 seconds
distribution_3D = [distribution(p, n_simulations=200) for p in [x/100 for x in range(101)]]
df_distribution_3D = pd.concat(distribution_3D, axis=1).T.reset_index(drop=True)


# In[174]:


# Empirically, look at how the number of turned on light bulbs evolve from 
# The synthax below uses "chaining" which is made possible in pandas library
df_number_of_turned_on_bulbs = df_distribution_3D.mean(axis=1).reset_index() \
    .rename(columns={0: 'Average number of turned on light bulbs', 'index': 'p'}) \
    .assign(p = [x/100 for x in range(101)])


# In[175]:


# Empirically, look at how the number of turned on light bulbs evolve from 
df_number_of_turned_on_bulbs


# In[182]:


# Let's plot the result
df_number_of_turned_on_bulbs.plot(x='p', y='Average number of turned on light bulbs')


# # Get the results mathematically

# In[192]:


# If n traders should press the switch a light bulb, the probability that an even number of them press the switch is:
# 0.5 * [1 + (1 - 2p)^n]
def probability_odd_number_traders(n, p):
    return 1 - 0.5 * (1 + (1 - 2*p)**n)


# In[219]:


def probabilitiy_by_bulb(p):
    return {bulb: probability_odd_number_traders(count_traders, p) 
            for (bulb, count_traders) in count_traders_by_bulb.items()}


# In[224]:


# Check the probability for p = 0.5, or whatever p
probabilitiy_by_bulb(0.5)


# In[230]:


plot = pd.DataFrame({'p': [x/100 for x in range(101)], 
                     'Average number of turned on light bulbs': [sum(probabilitiy_by_bulb(x/100).values()) for x in range(101)]}) \
    .plot(x='p', y='Average number of turned on light bulbs')
plot.axhline(y=50, color='grey')
# The maximum number of turned on light bulbs is reached only at p = 0.5!

