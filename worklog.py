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


def search_entries():
    '''Search entries'''

    menu_loop(menu=SEARCH_MENU)


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


def search_by_employee(search_query):
    '''Search by Employee'''

    if search_query == '':
        clear()
        input(
            'You must enter a value to search by. [press enter to continue]')
    else:
        entries = Log.select().where((Log.first_name.contains(search_query)) |
                                     (Log.last_name.contains(search_query)))
        display_entries(entries)


def search_by_date(search_query):
    '''Search by Date'''

    if validation.validate_date_input(search_query):
        entries = Log.select().where(Log.timestamp.contains(search_query))
        display_entries(entries)
    else:
        clear()
        input("You must enter a date in the format YYYY - MM - DD."
              "[press enter to continue]")


def search_by_term(search_query):
    '''Search by custom term'''

    if search_query == '':
        clear()
        input(
            'You must enter a value to search by. [press enter to continue]')
    else:
        entries = Log.select().where((Log.task_name.contains(search_query)) |
                                     (Log.notes.contains(search_query)))
        display_entries(entries)


def search_by_time_spent(search_query):
    '''Search by Time Spent'''

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
        if menu == MAIN_MENU:
            if choice in menu:
                clear()
                menu[choice]()

        if menu == SEARCH_MENU:
            if choice == 'e':
                clear()
                search_by_employee(search_query=input(
                    'Please enter an employee name to search for: '))
            elif choice == 'd':
                clear()
                search_by_date(search_query=input(
                    'Please enter a date to search for (format YYYY-MM-DD): '))
            elif choice == 't':
                clear()
                search_by_time_spent(search_query=input(
                    'Please enter an amount of time spent to search for: '
                    .strip()))
            elif choice == 'm':
                clear()
                search_by_term(search_query=input(
                    'Please enter a term to search for: '))


def initialize():
    db.connect()
    db.create_tables([Log], safe=True)


if __name__ == '__main__':
    initialize()
    menu_loop()
