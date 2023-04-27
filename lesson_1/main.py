def decorator(func):
    print('Inside decorator func')
    def wrapper(*args, **kwargs):
        print('Inside inner func')
        return func(*args, **kwargs)
        # print('After func was invoked')
    return wrapper


@decorator
def sum_of_two(first, second):
    summ = first + second
    print(f'Sum: {summ}')

    return summ


# wrap = decorator(sum_of_two)

print(sum_of_two(4, 5))
print(decorator(sum_of_two)(5, 5))

