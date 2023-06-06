# TODO What is a List - 1
#A Python list is similar to an array in other languages. 
# In Python, an empty list can be created in the following ways.
# They can contain any type of variable, 
# and they can contain as many variables as you wish. 
# Lists can also be iterated over in a very simple manner. Here is an example of how to build a list.

data = []

data.append(1)
data.append(2)
data.append(3)
data.append("hello")

print(data)
print(data[0])
# print(data[6])

# Nested lists and extends
a = [1, 2, 3]
b = [4, 5, 6]

# extends
# a.extend(b)
d = b+ a
print(d)
# print(a)

c = [a, b]
print(c)
print(d)

# Sorting
d.sort()
print(d)

# Slicing
e = d[0:3]
print(e)
# TODO 2Dimensional List - 2
a = [[55, 33, 22], [11, 66, 99], [33, 81, 232]]
print(a[0][2])

# TODO What is a tuple - 3
# TUPLES
# A tuple is similar to a list, but you create them with parentheses instead of square brackets. 
# You can also use the tuple built-in.
# The main difference is that a tuple is immutable while the list is mutable. Let’s take a look at a few examples:

my_tuple = (1, 2, 3, 4, 5)
t = my_tuple[0:3]
print(t)
another_tuple = tuple()
abc = tuple([1, 2, 3])
# list(abc)
print(abc)

# TODO What is a Dictionnary - 4
# A Python dictionary is basically a hash table or a hash mapping. 
# In some languages, they might be referred to as associative memories or associative arrays. 
# They are indexed with keys, which can be any immutable type. For example, a string or number can be a key. 
# You need to be aware that a dictionary is an unordered set of key:value pairs and the keys must be unique. 
# You can get a list of keys by calling a dictionary instance’s keys method.

# A dictionary is a data type similar to arrays, but works with keys and values instead of indexes. 
# Each value stored in a dictionary can be accessed using a key, which is any type of object (a string, a number, a list, etc.)
#  instead of using its index to address it.

phonebook = {
    "John" : 44422233,
    "doe" : 12334223,
    "jane" : 5523221    
}

# phonebook = {}

# phonebook['John'] = 231423
# phonebook['doe'] = 3234

removed = phonebook.pop("John")

print(phonebook)
print(removed)

if "jake" in phonebook:
    print("Jane is in the phonebook")
