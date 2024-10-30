import matplotlib.pyplot as plt
import seaborn as sns

# Example of a basic line plot using Matplotlib
plt.plot([1, 2, 3], [4, 5, 6])
plt.title('Basic Line Plot')
plt.show()

# Example of a bar plot using Seaborn
sns.barplot(x=['A', 'B', 'C'], y=[5, 7, 9])
plt.title('Bar Plot Example')
plt.show()