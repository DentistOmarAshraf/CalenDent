#!/usr/bin/env python3
"""
The console the entry point to
command interpreter
"""

import cmd
import sys
from models.__init__ import storage
from models.base_model import BaseModel
from models.user import User
from models.address import Address
from models.city import City
from models.neighborhood import Neighborhood
from models.review import Review
from models.clinic import Clinic
from models.reservation import Reservation
from models.service import Service

class CALENDENTCommand(cmd.Cmd):
    """
    CALENDENTCommand class
    """

    prompt = '(CalenDent) '

    valid_classes = {"BaseModel": BaseModel, "User": User, "Address": Address,
                     "City": City, "Review": Review, "Clinic": Clinic,
                     "Reservation": Reservation, "Service": Service,
                     "Neighborhood": Neighborhood}
    data = storage.all()

    def help_help(self):
        """Overwrite of super class help def"""
        print('This is a CalenDent created using Python, OOP')
        print('and other concepts learned on ALX.')

    def do_quit(self, line):
        """Quit command to exit the program"""
        exit()

    def help_quit(self):
        print('exit cmd')
        print()

    def do_EOF(self, line):
        """Exit the program on EOF Style"""
        print()
        exit()

    def emptyline(self):
        """The program will perform no action when an empty line is entered."""
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel"""
        args = line.split(' ')

        if not args or not args[0]:
            print("** class name missing **")
            return

        if args[0] not in self.valid_classes.keys():
            print("** class doesn't exist **")
            return

        get_class = self.valid_classes[args[0]]
        var_class = get_class()

        if len(args) > 1:
            param = args[1:]
            for x in param:
                key = x[:x.find('=')]
                value = x[x.find('=')+1:]
                if value[0] == '"':
                    value = value[1:]
                if value[len(value)-1] == '"':
                    value = value[:len(value)-1]
                if value and len(value) != 0:
                    if '"' in value:
                        value = value.replace('"', '')
                    if '_' in value:
                        value = value.replace("_", " ")
                    if '.' in value:
                        try:
                            value = float(value)
                        except Exception:
                            pass
#                    elif value[0] != '0' and value.isdigit():
#                        value = int(value)
                    setattr(var_class, key, value)

        var_class.save()
        print(var_class.id)

    def do_show(self, line):
        """Prints the string representation of an instance based on
        the class name and id"""
        args = line.split(' ')

        if not args or not args[0]:
            print("** class name missing **")
            return

        if args[0] not in self.valid_classes.keys():
            print("** class doesn't exist **")
            return

        if not args or len(args) < 2 or not args[1]:
            print("** instance id missing **")
            return

        dic_key = args[0] + '.' + args[1]

        all_objects = storage.all()

        if dic_key not in all_objects:
            print("** no instance found **")
            return

        print(all_objects.get(dic_key))

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        args = line.split(' ')

        if not args or not args[0]:
            print("** class name missing **")
            return

        if args[0] not in self.valid_classes.keys():
            print("** class doesn't exist **")
            return

        if not args or len(args) < 2 or not args[1]:
            print("** instance id missing **")
            return

        dic_key = args[0] + '.' + args[1]

        if dic_key not in storage.all():
            print("** no instance found **")
            return

        del (storage.all()[dic_key])
        storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances based or
        not on the class name"""
        args = line.split(' ')

        to_show = []

        if not args or not args[0]:
            for value in storage.all().values():
                to_show.append(str(value))
        elif args[0]:
            if args[0] not in self.valid_classes.keys():
                print("** class doesn't exist **")
                return

            for key, value in storage.all().items():
                if key.split('.')[0] == args[0]:
                    to_show.append(str(value))

        print(to_show)

    def do_update(self, line):
        """Update class attributes"""
        args = line.split(' ')

        if not args or not args[0]:
            print("** class name missing **")
            return

        if args[0] not in self.valid_classes.keys():
            print("** class doesn't exist **")
            return

        if not args or len(args) < 2 or not args[1]:
            print("** instance id missing **")
            return

        dic_key = args[0] + '.' + args[1]

        if dic_key not in storage.all():
            print("** no instance found **")
            return

        if not args or len(args) < 3 or not args[2]:
            print("** attribute name missing **")
            return

        if not args or len(args) < 4 or not args[3]:
            print("** value missing **")
            return

        setattr(storage.all()[dic_key], args[2], args[3].strip('"'))
        storage.save()

    def do_count(self, line):
        """Counting Instance"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.valid_classes.keys():
            print("** class doesn't exist **")
            return
        ls = []
        for k, v in self.data.items():
            if k.split('.')[0] == args[0]:
                ls.append(str(v))
        print(len(ls))

    def precmd(self, line):
        """Pre Command Proccessing"""
        args = line.split('.')
        if len(args) == 1:
            return args[0]

        if len(args) == 2:
            sec_seg = args[1].split('(')
            if len(sec_seg) == 1:
                return line
            if len(sec_seg[1]) == 1:
                return sec_seg[0] + ' ' + args[0]
            if len(sec_seg[1]) > 1:
                z = sec_seg[1].split(',')
                z = [x.strip(')') for x in z]
                z = [x.strip('"') for x in z]
                z = [x.strip(' ') for x in z]
                z = [x.strip('"') for x in z]
                z = [x.strip('\'') for x in z]
                string = sec_seg[0] + ' ' + args[0]
                for i in z:
                    string += ' ' + i
                return string


if __name__ == '__main__':
    CALENDENTCommand().cmdloop()
