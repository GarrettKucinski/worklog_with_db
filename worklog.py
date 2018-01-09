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
    time_spent = IntegerField(default=0)
    notes = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)


class Worklog:
    pass


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def search_entries():
    '''Search entries'''
    menu_loop(menu=SEARCH_MENU)


def view_entries(entries):
    '''View previous entries'''

    for entry in entries:
        clear()
        fullname = '{} {}'.format(entry.first_name, entry.last_name)

        print(entry.timestamp.strftime('%A %B %d, %Y %I:%M%p'))
        print('=' * 20)
        print('Task Name: {}\n'
              'Employee Name:{}\n'
              'Time Spent: {}\n'
              'Notes: {}\n'.format(entry.task_name, fullname,
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


def search_by_employee():
    '''Search by Employee'''

    search_query = input('Please enter an employee name to search for: ')
    entries = Log.select().where((Log.first_name.contains(search_query)) |
                                 (Log.last_name.contains(search_query)))
    view_entries(entries)


def search_by_date():
    '''Search by Date'''

    search_query = input(
        'Please enter a date to search for (format YYYY-MM-DD): ')
    entries = Log.select().where(Log.timestamp.contains(search_query))
    view_entries(entries)


def search_by_term():
    '''Search by custom term'''

    search_query = input('Please enter a term to search for: ')
    entries = Log.select().where((Log.task_name.contains(search_query)) |
                                 (Log.notes.contains(search_query)))
    view_entries(entries)


def search_by_time_spent():
    '''Search by Time Spent'''

    search_query = int(input(
        'Please enter an amount of time spent to search for: ').strip())
    entries = Log.select().where(Log.time_spent == search_query)
    view_entries(entries)


def add_entry():
    '''Add Entry'''

    name = input("Enter a name for this task: ")
    user_fname = input("Enter your first name: ")
    user_lname = input("Enter your last name: ")
    task_time = input("Enter the time spent completing this task: ")
    task_notes = input("Enter any additional notes: ")

    Log.create(task_name=name, first_name=user_fname,
               last_name=user_lname, time_spent=task_time, notes=task_notes)

    clear()
    input('Entry Saved Successfully [press enter to continue]')


MAIN_MENU = OrderedDict([
    ('a', add_entry),
    ('s', search_entries)
])

SEARCH_MENU = OrderedDict([
    ('e', search_by_employee),
    ('d', search_by_date),
    ('t', search_by_time_spent),
    ('m', search_by_term)
])


def menu_loop(menu=MAIN_MENU):
    '''Show the current menu'''

    choice = None
    current_date = datetime.datetime.now()
    exit_menu = ('Please select an option \nor enter q to quit: ' if menu ==
                 MAIN_MENU else 'Enter q to return the the main menu: ')

    while choice != 'q':
        clear()
        print(current_date.strftime('%A %B %d, %Y %I:%M%p'))
        print('=' * 40)
        for key, value in menu.items():
            print('[{}] {}'.format(key, value.__doc__))
        print('=' * 40)
        choice = input(exit_menu).lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def initialize():
    db.connect()
    db.create_tables([Log], safe=True)


if __name__ == '__main__':
    initialize()
    menu_loop()
