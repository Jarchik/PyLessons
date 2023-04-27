STORE_EVENT = 'log'
IGNORE_EVENT = 'ignore'

history = ()

def movement_history(event_type: str = IGNORE_EVENT):
        def decorator(func):
                if event_type == STORE_EVENT:
                        history.append(func)
                print('Inside decorator func')
                def wrapper(*args, **kwargs):
                        print('Inside inner func')
                        return func(*args, **kwargs)
                return wrapper

print(f"History on start: {history}")


@movement_history(event_type=STORE_EVENT)
def move_forward(steps: int):
    print(f'Moving forward {steps} steps...')


@movement_history(event_type=STORE_EVENT)
def turn_left():
    print(f'Turning left')


@movement_history(event_type=STORE_EVENT)
def turn_left():
    print(f'Turning right')


@movement_history(event_type=STORE_EVENT)
def move_back(steps: int):
    print(f'Moving back {steps} steps...')

@movement_history()
def look_arround():
    print('Just looking around...')

print(f"Final history: {history}")

move_forward(5)
move_forward(3)
turn_left()
look_arround()
move_forward(2)
look_arround()
move_back(2)


def replay_history():
       (action() for action in history)
