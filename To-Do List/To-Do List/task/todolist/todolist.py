# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
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
            today_tasks(session)
        elif action == 2:
            week_tasks(session)
        elif action == 3:
            all_tasks(session)
        elif action == 4:
            add_task(session)
        else:
            break


def ask_action():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Add task")
    print("0) Exit")
    return int(input())


def today_tasks(session):
    today = datetime.today().date()
    rows = session\
        .query(TaskTable)\
        .filter(TaskTable.deadline == today)\
        .all()
    print_tasks(rows)


def week_tasks(session):
    today = datetime.today()
    for n in range(7):
        date = (today + timedelta(days=n)).date()
        rows = session\
            .query(TaskTable)\
            .filter(TaskTable.deadline == date)\
            .all()
        print(date.strftime("%A %d %b"), ":")
        print_tasks(rows)


def all_tasks(session):
    rows = session\
        .query(TaskTable)\
        .all()
    print_tasks(rows)


def print_tasks(rows):
    if len(rows) == 0:
        print('Nothing to do!')
    else:
        for n in range(len(rows)):
            row = rows[n]
            dl = row.deadline
            dl_str = f'{dl.day} {dl.strftime("%b")}'
            print(f'{n + 1}. {row.task} {dl_str}')
    print()


def add_task(session):
    print("Enter task")
    task = input()
    print("Enter deadline")
    deadline = input()
    dl = datetime.strptime(deadline, "%Y-%m-%d")
    row = TaskTable(task=task, deadline=dl)
    session.add(row)
    session.commit()
    print('The task has been added!')
    print()


main()
