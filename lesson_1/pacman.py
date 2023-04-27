ALLOWED_EVENT = 'allowed'
FORBIDDEN_EVENT = 'forbidden'

allowed_actions = []


def movement_history(event_type: str = FORBIDDEN_EVENT):
    def decorator(func):
            print(f"Loading available game actions: {func.__name__}")
            if event_type == ALLOWED_EVENT:
                allowed_actions.append(func.__name__)
            def wrapper(*args, **kwargs):
                if func.__name__ in allowed_actions:
                        return func(*args, **kwargs)
                else:
                    print('Action not allowed. Ignoring')
            return wrapper
    return decorator


print(f"Allowed acions: {allowed_actions}")


@movement_history(ALLOWED_EVENT)
def move_forward(steps: int):
    print(f'Moving forward {steps} steps...')


@movement_history(ALLOWED_EVENT)
def turn_left():
    print(f'Turning left')


@movement_history(ALLOWED_EVENT)
def turn_right():
    print(f'Turning right')


@movement_history(ALLOWED_EVENT)
def move_back(steps: int):
    print(f'Moving back {steps} steps...')

@movement_history()
def look_arround():
    print('Just looking around...')


print(f"Allowed acions: {allowed_actions}")

move_forward(5)
move_forward(3)
turn_left()
look_arround()
move_forward(2)
look_arround()
move_back(2)
