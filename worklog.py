#!/usr/bin/env python3

from peewee import *
import datetime
import os
import sys

from collections import OrderedDict

db = SqliteDatabase('worklog.db')


class BaseModel(Model):
    '''A base model that will use our sqlite database'''

    class Meta:
        database = db


class Log(BaseModel):
    '''Model for representing a single worklog entry in the database'''

    task_name = CharField(max_length=255)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    time_spent = IntegerField()
    notes = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now())


class Worklog:
    pass


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def search_entries():
    '''Search entries'''
    view_entries()


def view_entries(search_query=None, search_type=None):
    '''View previous entries'''
    entries = Log.select()

    if search_type:
        if search_type == 'employee':
            entries = entries.where((Log.first_name.contains(search_query)) | (
                Log.last_name.contains(search_query)))
        elif search_type == 'date':
            entries = entries.where(
                Log.timestamp.date() == search_query)
        elif search_type == 'time_spent':
            entries = entries.where(Log.time_spent.contains(search_query))

    clear()
    for entry in entries:
        fullname = '{} {}'.format(entry.first_name, entry.last_name)

        print('=' * 20)
        print('Date: {}\n'
              'Task Name: {}\n'
              'Employee Name:{}\n'
              'Time Spent: {}\n'
              'Notes: {}\n'.format(entry.timestamp.date(),
                                   entry.task_name, fullname,
                                   entry.time_spent, entry.notes))
        print('=' * 20)
        print('[n] Next Entry')
        print('[d] Delete Entry')
        print('[q] Main Menu')
        print('=' * 20)
        action = input('Please make a selection: ').lower().strip()

        if action == 'q':
            clear()
            break


def search_by_name():
    '''Search by name'''


def menu_loop():
    '''Show the main menu'''
    choice = None
    current_date = datetime.datetime.now()

    while choice != 'q':
        clear()
        print(current_date.strftime('%A %B %d, %Y %I:%M%p'))
        print('=' * 40)
        for key, value in MAIN_MENU.items():
            print('[{}] {}'.format(key, value.__doc__))
        print('=' * 40)
        choice = input(
            'Please select an option \nor enter q to quit: ').lower().strip()

        if choice in MAIN_MENU:
            clear()
            MAIN_MENU[choice]()


def initialize():
    db.connect()
    db.create_tables([Log], safe=True)


MAIN_MENU = OrderedDict([
    ('a', search_by_name),
    ('s', search_entries)
])

if __name__ == '__main__':
    initialize()
    menu_loop()
