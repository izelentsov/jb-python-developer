# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class TaskTable(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date)

    def __repr__(self):
        return f'{str(id)} - {self.task}'


def main():
    engine = create_engine('sqlite:///todo.db?check_same_thread=False')
    Base.metadata.create_all(engine)
    make_session = sessionmaker(bind=engine)
    session = make_session()

    while True:
        action = ask_action()
        if action == 1:
            print_tasks(session)
        elif action == 2:
            add_task(session)
        else:
            break


def ask_action():
    print("1) Today's tasks")
    print("2) Add task")
    print("0) Exit")
    return int(input())


def print_tasks(session):
    rows = session.query(TaskTable).all()
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for n in range(len(rows)):
            task = rows[n].task
            print(f'{n + 1}. {task}')
    print()


def add_task(session):
    print("Enter task")
    task = input()
    row = TaskTable(task=task, deadline=datetime.today())
    session.add(row)
    session.commit()
    print('The task has been added!')
    print()


main()
