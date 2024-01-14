#!/usr/bin/python3
"""Defines the console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """class to define entry point of the command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        _match = re.search(r"\.", arg)
        if _match is not None:
            argl = [arg[:_match.span()[0]], arg[_match.span()[1]:]]
            _match = re.search(r"\((.*?)\)", argl[1])
            if _match is not None:
                command = [argl[1][:_match.span()[0]], _match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Prints string repr of instance based on class name & id."""
        arg_l = parse(arg)
        objdict = storage.all()
        if len(arg_l) == 0:
            print("** class name missing **")
        elif arg_l[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_l) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_l[0], arg_l[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(arg_l[0], arg_l[1])])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        arg_l = parse(arg)
        obj_dict = storage.all()
        if len(arg_l) == 0:
            print("** class name missing **")
        elif arg_l[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_l) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_l[0], arg_l[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_l[0], arg_l[1])]
            storage.save()

    def do_all(self, arg):
        """Prints all string repr of instances based or not on class name."""
        arg_l = parse(arg)
        if len(arg_l) > 0 and arg_l[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_l = []
            for obj in storage.all().values():
                if len(arg_l) > 0 and arg_l[0] == obj.__class__.__name__:
                    obj_l.append(obj.__str__())
                elif len(arg_l) == 0:
                    obj_l.append(obj.__str__())
            print(obj_l)

    def do_count(self, arg):
        """Retrieve the number of instances of a given class."""
        arg_l = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arg_l[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        arg_l = parse(arg)
        obj_dict = storage.all()

        if len(arg_l) == 0:
            print("** class name missing **")
            return False
        if arg_l[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_l) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_l[0], arg_l[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_l) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_l) == 3:
            try:
                type(eval(arg_l[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_l) == 4:
            obj = obj_dict["{}.{}".format(arg_l[0], arg_l[1])]
            if arg_l[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arg_l[2]])
                obj.__dict__[arg_l[2]] = valtype(arg_l[3])
            else:
                obj.__dict__[arg_l[2]] = arg_l[3]
        elif type(eval(arg_l[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_l[0], arg_l[1])]
            for k, v in eval(arg_l[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
