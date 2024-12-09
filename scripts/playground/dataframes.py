# Importing pandas as pd
from pandas import DataFrame

# Creating a data frame
cart = {'Product': ['Mobile', 'AC', 'Laptop', 'TV', 'Football'],
		'Type': ['Electronic', 'HomeAppliances', 'Electronic',
				'HomeAppliances', 'Sports'],
		'Price': [10000, 35000, 50000, 30000, 799]
	}

#df = DataFrame(cart, columns = ['Product', 'Type', 'Price'])
df = DataFrame(cart)

# Print original data frame
print("Original data frame:\n")
print(df)

# Selecting the product of Electronic Type
select_prod = df.loc[df['Type'] == 'Electronic']

print("\n")

# Print selected rows based on the condition
print("Selecting rows:\n")
print (select_prod)
