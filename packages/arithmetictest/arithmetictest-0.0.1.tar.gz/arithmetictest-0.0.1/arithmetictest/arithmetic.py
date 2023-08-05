def add(x, y):
    return x + y

def division(x, y):
    return x / y

def multiply(x, y):
    return x * y

def subtract(x, y):
    return x - y

if __name__ == "__main__":
	import sys
	import os
	import argparse

	my_parser = argparse.ArgumentParser(
					description='Operation between var1 and var2', 
					epilog='Enjoy the program !',
					prog='Calculate',
					allow_abbrev=False,
					add_help=True,
					usage='%(prog)s [options] value1 value2', #%(prog)s is automatically replaced by the name of the program)
					prefix_chars='-',
					)

	my_parser.add_argument('--Operation',
							'-ope',
	                       metavar='operation',
	                       type=str,
	                       choices=['a', 'd', 'm','s'],
	                       help='type of operation',
	                       required=True,
	                       action='store',)

	my_parser.add_argument('Values',
                       metavar='Values',
                       type=int,
                       nargs=2,
                       help='values to operate',
                       #required=True,
                       action='store',)

	args = my_parser.parse_args()
	v = args.Operation
	valOne = args.Values[0]
	valTwo = args.Values[1]
	if v == "a":
		print(add(valOne, valTwo))
	elif v == "d":
		print(division(valOne, valTwo))
	elif v == "m":
		print(multiply(valOne, valTwo))
	elif v == "s":
		print(subtract(valOne, valTwo))
	else:
		pass
