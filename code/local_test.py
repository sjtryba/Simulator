value = 1234567

value_array = [int(i) for i in str(value)]

# Separate the last four digits from the rest of the array
right_values = value_array[-4:]
left_values = value_array[:(len(value_array) - 4)]

# Convert the arrays into integers
right_values = int(''.join(map(str, right_values)))
left_values = int(''.join(map(str, left_values)))

print(value_array)
print("Right: ", right_values)
print("Left: ", left_values)
