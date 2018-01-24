#!/usr/bin/env python3

from peewee import *
import datetime
import os
import sys

from collections import OrderedDict

import validation

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


def clear():
    '''Clear the screen'''

    os.system('cls' if os.name == 'nt' else 'clear')


def quit_program():
    '''Quit'''
    sys.exit()


def search_entries():
    '''Search entries'''
    while True:
        clear()
        print_menu(menu=SEARCH_MENU)
        print("Press [R] to return to the main menu.")
        print('=' * 40)
        choice = get_user_choice()

        if choice:
            if choice == 'r':
                break

            execute_menu_selection(choice, menu=SEARCH_MENU)


def display_entries(entries):
    '''View previous entries'''

    if entries:
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
            print('[q] Search Menu')
            print('=' * 20)
            action = input('Please make a selection: ').lower().strip()

            if action == 'q':
                clear()
                break
    else:
        clear()
        input('No results found. [press enter to continue]')


def search_by_employee():
    '''Search by Employee'''

    search_query = input('Please enter an employee name to search for: ')

    if search_query == '':
        clear()
        input(
            'You must enter a value to search by. [press enter to continue]')
    else:
        entries = Log.select().where((Log.first_name.contains(search_query)) |
                                     (Log.last_name.contains(search_query)))
        display_entries(entries)


def search_by_date():
    '''Search by Date'''

    search_query = input(
        'Please enter a date to search for (format YYYY-MM-DD): ')

    if validation.validate_date_input(search_query):
        entries = Log.select().where(Log.timestamp.contains(search_query))
        display_entries(entries)
    else:
        clear()
        input("You must enter a date in the format YYYY - MM - DD."
              "[press enter to continue]")


def search_by_term():
    '''Search by Custom Term'''

    search_query = input('Please enter a term to search for: ')

    if search_query == '':
        clear()
        input(
            'You must enter a value to search by. [press enter to continue]')
    else:
        entries = Log.select().where((Log.task_name.contains(search_query)) |
                                     (Log.notes.contains(search_query)))
        display_entries(entries)


def search_by_time_spent():
    '''Search by Time Spent'''

    search_query = input(
        'Please enter an amount of time spent to search for: '
        .strip())

    if validation.validate_time_spent(search_query):
        entries = Log.select().where(Log.time_spent == search_query)
        display_entries(entries)
    else:
        clear()
        input(
            'Please enter a value number of time spent.'
            ' [press enter to continue]')


def add_entry():
    '''Add Entry'''

    name = input("Enter a name for this task: ")
    user_fname = input("Enter your first name: ")
    user_lname = input("Enter your last name: ")
    task_time = input("Enter the time spent completing this task: ")
    task_notes = input("Enter any additional notes: ")

    Log.create(task_name=name,
               first_name=user_fname,
               last_name=user_lname,
               time_spent=task_time,
               notes=task_notes)

    clear()
    input('Entry Saved Successfully [press enter to continue]')


def print_menu(menu):
    current_date = datetime.datetime.now()

    print(current_date.strftime('%A %B %d, %Y %I:%M%p'))
    print('=' * 40)
    for key, value in menu.items():
        print('[{}] {}'.format(key, value.__doc__))
    print('=' * 40)


def get_user_choice(choice=''):
    if not choice:
        choice = input("Please select a menu option: ")

    return choice


def validate_menu_choice(choice, menu):
    if choice in menu or choice == 'r':
        return True

    return False


def execute_menu_selection(choice='', menu=OrderedDict()):
    if validate_menu_choice(choice, menu):
        clear()
        menu[choice]()
    else:
        clear()
        print("ERROR: Oops, that doesn't seem to be a valid menu option."
              "Try again.\n")


MAIN_MENU = OrderedDict([
    ('a', add_entry),
    ('s', search_entries),
    ('q', quit_program)
])

SEARCH_MENU = OrderedDict([
    ('e', search_by_employee),
    ('d', search_by_date),
    ('t', search_by_time_spent),
    ('m', search_by_term),
])


def menu_loop():
    '''Show the current menu'''

    while True:
        clear()
        print_menu(menu=MAIN_MENU)
        execute_menu_selection(get_user_choice(), menu=MAIN_MENU)


def initialize():
    db.connect()
    db.create_tables([Log], safe=True)


if __name__ == '__main__':
    initialize()
    menu_loop()
