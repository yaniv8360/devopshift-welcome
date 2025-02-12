# def something(a,b):
#     return a*b*3


# something2= lambda a,b: a*3*b

# x = something(9, 10)
# y=something2(9, 10)

# print(x)
# print(y)

# print(something)
# print(something2)


from typing import Callable


def logging_wrapper(func: Callable):
    def new_function(*args, **kwargs):
        print(f"{func.__name__} was called")
        result = func(*args, **kwargs)
        return result
    return new_function


@logging_wrapper
def add(a: int, b: int) -> int:
    return a+b


@logging_wrapper
def mul(a: int, b: int) -> int:
    return a*b


def power2(a: int) -> int:
    return a*a


@logging_wrapper
def int_as_str(a: int) -> str:
    return str(a)


def do_math(a: int, b: int, operation_function: Callable):
    if len(operation_function.__annotations__) == 2:
        result = operation_function(a)
    else:
        result = operation_function(a, b)
    return result


op_map = {
    "plus": add,
    "sub": lambda a, b: a-b,
    "multiply": mul,
    "power2": power2
}


op_str = "power2"
x = 10
y = 20

result = do_math(x, y, op_map[op_str])

op_str = "sub"
result = do_math(x, y, op_map[op_str])

op_str = "plus"
result = do_math(x, y, op_map[op_str])

op_str = "multiply"
result = do_math(x, y, op_map[op_str])
# if op == "plus":
#     result = do_math(x,y,add)
# elif op == "multiply":
#     result=do_math(x,y,mul)
# elif op == "sub":
#     result=do_math(x,y,lambda a,b: a-b)
# else:
#     raise ValueError("I dont know enything else")
print(result)
