#TODO > Hello world
# Python is a very simple language, 
# and has a very straightforward syntax. 
# It encourages programmers to program without boilerplate (prepared) code. 
# The simplest directive in Python is the "print" directive - it simply prints out a line 
# (and also includes a newline, unlike in C).
print("hello world")

# Python supports two types of numbers - integers(whole numbers) 
# and floating point numbers(decimals). (It also supports complex numbers, 
# which will not be explained in this tutorial).
#TODO > Declare variables (int, float, string) - 2

value = 3
print(value)
decimal = 8.5 # or float(2)
print(value)
# for string you can single or double quotes
word = "hello" # or 'hello'
print(word)

#TODO > Simples operations on variables - 3

value1 = 2
value2 = 4
# value = value1 + value2
# value = value1 - value2
# value = value1 / value2
# value = value1 * value2
# value = 2 % 3
print(value)

# Adding two strings 
a = "hello"
b = 'world'
d = 3000
c = a+ " " + b
print(c)

# inline declarations
name, age = 'joseph', 23
print(name)
print(age)
# Conversion


#TODO > String Concatenation, methods - 4
a = 3000
b = "love you"

print(b + str(b))
print(f"{b} {a}") # OR print("{} {}".format(b, a))
# print("{1} {0}".format(b, a))

#TODO > String Slicing , Formating - 5
# String Slicing
word = "Hello"
a = word[0]
print(a)
print(help(word))

