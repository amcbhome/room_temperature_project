import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Parameters
mean = 0
std_dev = 1
x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
y = norm.pdf(x, mean, std_dev)

# Plot the curve
plt.figure(figsize=(10,6))
plt.plot(x, y, color='black', linewidth=2)

# Shade 68% region (μ ± 1σ)
x_fill = np.linspace(mean - std_dev, mean + std_dev, 500)
plt.fill_between(x_fill, norm.pdf(x_fill, mean, std_dev), alpha=0.3, color='skyblue', label='68% of data')

# Shade 95% region (μ ± 2σ)
x_fill = np.linspace(mean - 2*std_dev, mean + 2*std_dev, 500)
plt.fill_between(x_fill, norm.pdf(x_fill, mean, std_dev), alpha=0.3, color='lightgreen', label='95% of data')

# Shade 99.7% region (μ ± 3σ)
x_fill = np.linspace(mean - 3*std_dev, mean + 3*std_dev, 500)
plt.fill_between(x_fill, norm.pdf(x_fill, mean, std_dev), alpha=0.3, color='lightcoral', label='99.7% of data')

# Lines for mean and ±σ
plt.axvline(mean, color='black', linestyle='--', label='Mean')
for i in range(1, 4):
    plt.axvline(mean - i*std_dev, color='gray', linestyle='--')
    plt.axvline(mean + i*std_dev, color='gray', linestyle='--')

# Labels
plt.title("Normal Distribution with Empirical Rule", fontsize=16)
plt.xlabel("Value")
plt.ylabel("Probability Density")
plt.legend()
plt.grid(True)
plt.show()
