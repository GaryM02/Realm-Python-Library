import time
startTime = time.time()

from RealmPython import *


"""
The following is a very basic script to display some of the CRUD functionality.
"""

class ToDo(ObjectModel):
    def __init__(self, task='', priority=0, finished=False):
        self.task = task
        self.priority = priority
        self.finished = finished

realm = Realm()

choice = 0
while choice != 5:

    print('1. Add Task')
    print('2. Get Tasks')
    print('3. Update Tasks')
    print('4. Delete Tasks')
    print('5. Exit')

    choice = int(input('Please choose an option. '))

    if choice == 1:

        task = input('Please enter a new task. ')
        priority = int(input('Please specify the priority. '))
        new_task = ToDo(task, priority, False)
        realm.add(new_task)

    elif choice == 2:

        object_to_get = int(input("would you like to get 1. finished or 2. unfinished tasks? "))
        if object_to_get == 1:
            print(realm.objects(ToDo).filter("finished==true"))
        else:
            print(realm.objects(ToDo).filter("finished==false"))

    elif choice == 3:
        task_to_update = input('Which task? ')
        realm.objects(ToDo).filter_for_update(f"task=='{task_to_update}'", priority=1, finished=True)

    elif choice == 4:
        task_to_delete = input('Which task? ')
        realm.objects(ToDo).delete(f"task=='{task_to_delete}'")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
 