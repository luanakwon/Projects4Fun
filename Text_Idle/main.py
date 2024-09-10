import time
from player import User
from action import Dig, IdleAction

if __name__=='__main__':
    print("Welcome to the Text-Idle")
    try:
        user = User.load_data()
    except FileNotFoundError:
        print("No savedata found, starting a new game")
        user = User()
    try:
        while True:
            commands = input().split(' ')
            
            if commands[0] == 'dig':
                action = user.actions.get('dig',None)
                if action is None:
                    print("new action added : dig")
                    action = Dig()
                    user.actions['dig'] = action
                if "--setIdle" in commands[1:]:
                    action.setIdleAct()
                else:
                    action.act(user)
            elif commands[0] == 'status':
                if "--update" in commands[1:]:
                    for action in user.actions.values():
                        if isinstance(action,IdleAction):
                            action.updateIdleAct(user)
                user.status()
    except KeyboardInterrupt as err:
        print(err)
    finally:
        print("Saving data...")
        user.save_data()
        print("Data successfully saved. See you soon")
        