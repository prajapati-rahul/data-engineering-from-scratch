#NumPy 🚀
#NumPy (Numerical Python) is a Python library used for fast numerical operations on large amounts of data. The core of NumPy is the ndarray, a fast and space-efficient multidimensional array that allows you to perform mathematical operations on entire arrays without the need for explicit loops. NumPy also provides a wide range of mathematical functions, random number generation, and tools for integrating with other libraries.

import numpy as np
prices = np.array([100, 200, 300, 400, 500])
#Note you can't do this with a list, but you can do this with a numpy array. This is because numpy arrays are designed for numerical operations, while lists are more general-purpose data structures.
print(prices * 1.1)  # Increase prices by 10%

#output:
# [110. 220. 330. 440. 550.]


#NumPy Array vs Python List
num = [1, 2, 3, 4, 5] #List
num_np = np.array([1, 2, 3, 4, 5]) #NumPy Array

print(type(num))  #output: <class 'list'>
print(type(num_np))  #output: <class 'numpy.ndarray'>

num_2dnp = np.array([[1, 2, 3], [4, 5, 6]]) #2D NumPy Array
print(num_2dnp.shape)  #output: (2, 3)



#Useful Array Creation Functions


#np.zeros()
#creates an array filled with zeros. You can specify the shape of the array as a tuple.

arr = np.zeros(5)
print(arr)     #output: [0. 0. 0. 0. 0.]

arr_2d = np.zeros((2, 3))
print(arr_2d)  #output: [[0. 0. 0.]
               #         [0. 0. 0.]]    


#np.ones()
#creates an array filled with ones. You can specify the shape of the array as a tuple
arr = np.ones(5)
print(arr)     #output: [1. 1. 1. 1. 1.]


#np.arange()
#creates an array with evenly spaced values within a given range. You can specify the start, stop, and step size.
arr = np.arange(0, 10, 2)
print(arr)     #output: [0 2 4 6 8]

arr = np.arange(5)
print(arr)     #output: [0 1 2 3 4]

#Syntex : np.arange(start, stop, step)   #stop is excluded.


#np.linspace()
#creates an array with evenly spaced values over a specified range. You can specify the start, stop, and the number of values you want in the array.
arr = np.linspace(0, 1, 5)
print(arr)     #output: [0.   0.25 0.5  0.75 1.  ]

#Syntax : np.linspace(start, stop, num)   #stop is included.



#Important Array Properties

arr = np.array([
    [10, 20, 30],
    [40, 50, 60]
])

#shape
print(arr.shape)  #output: (2, 3)


#size
print(arr.size)  #output: 6


#ndim
print(arr.ndim)  #output: 2


#dtype
print(arr.dtype)  #output: int64 (or int32 depending on your system)


#Indexing and Slicing
#postive indexing is as same as other programming languages, but negative indexing is also supported in NumPy. Negative indexing allows you to access elements from the end of the array.

arr = np.array([10, 20, 30, 40, 50])
print(arr[-1]) #output: 50 (last element)
print(arr[-3:-1]) #output: 30 40 (elements at index -3 and -2)
print(arr[-1:0:-1]) #output: 50 40 30 20 10 (elements from last to first in reverse order)

#2D slicing
arr = np.array([
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
])

print(arr[1:, 1:])  #output: [[50 60]
                    #         [80 90]]
print(arr[:2])  #output: [[10 20 30]
                #         [40 50 60]]
#Syntax : arr[row_start:row_end, col_start:col_end]  #row_end and col_end are excluded.



#Vectorized Operations



#this is one of the most powerful features of NumPy. It allows you to perform operations on entire arrays without the need for explicit loops. This leads to more concise and efficient code.
prices = np.array([100, 200, 300])

print(prices + 50)  #output: [150 250 350]
print(prices * 1.1)  #output: [110. 220. 330.]

print(np.sum(prices))   #output: 600
print(np.mean(prices))  #output: 200.0
print(np.max(prices))   #output: 300
print(np.min(prices))   #output: 100
print(np.std(prices))   #output: 81.64965809277261
print(np.median(prices))  #output: 200.0
print(np.var(prices))     #output: 6666.666666666667
print(np.percentile(prices, 50))  #output: 200.0

#axis
arr_2d = np.array([
    [10, 20, 30],
    [40, 50, 60]
])
print(np.sum(arr_2d, axis=0))  #output: [50 70 90]
print(np.sum(arr_2d, axis=1))  #output: [60 150]

# axis=0 → down the rows → column result
# axis=1 → across the columns → row result

# Reshape
arr = np.arange(1, 7)

print(arr)   #output: [1 2 3 4 5 6]
arr_reshaped = arr.reshape((2, 3))
print(arr_reshaped)  #output: [[1 2 3]
                    #         [4 5 6]]


# Boolean Filtering
prices = np.array([100, 500, 200, 1000, 300])
print(prices > 300)  #output: [False  True False  True False]

filtered_prices = prices[prices > 300]
#this is called boolean indexing or boolean masking. It allows you to filter elements of an array based on a condition.
print(filtered_prices)  #output: [ 500 1000]


#another example of boolean filtering
sales = np.array([1000, 5000, 2000, 8000, 3000])
high_sales = sales[sales > 3000]
print(high_sales)    #output: [5000 8000]



#Handling Missing Values

#NumPy provides functions to handle missing values (NaN - Not a Number)
arr = np.array([1, 2, np.nan, 4, 5])
print(arr)  #output: [ 1.  2. nan  4.  5.]

# Check for NaN values
print(np.isnan(arr))  #output: [False False  True False False]

# Remove NaN values
cleaned_arr = arr[~np.isnan(arr)]
print(cleaned_arr)  #output: [1. 2. 4. 5.]

#normal mean
print(np.mean(arr))  #output: nan
#mean without NaN
print(np.nanmean(arr))  #output: 3.0

#similarly, you can use np.nanstd(), np.nanvar(), etc. to calculate standard deviation, variance, etc. while ignoring NaN values.
np.nansum(arr)   #output: 12.0
np.nanmin(arr)   #output: 1.0
np.nanmax(arr)   #output: 5.0



#Practical Data Engineering Example



transections = np.array([100, 200, np.nan, 400, 500, np.nan, 700])
# Remove NaN values
cleaned_transections = transections[~np.isnan(transections)]
# Calculate total and average
total = np.sum(cleaned_transections)   #output: 1900.0
average = np.mean(cleaned_transections)   #output: 380.0

high_transections = cleaned_transections[cleaned_transections > 300]
print(high_transections)   #output: [400. 500. 700.]


#NumPy vs Pandas
#You'll use both heavily.

#Numpy
#best for numerical arrays and mathematical operations, matrix operations and ml calculations, and when you need to perform operations on entire arrays without explicit loops.

#Pandas
#best for tabular data, data cleaning, manipulation, and analysis, and when you need to work with labeled data (rows and columns) and perform operations like filtering, grouping, and aggregating.
