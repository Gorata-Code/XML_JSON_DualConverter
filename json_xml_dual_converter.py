import os
import sys
from types_swap_bot.files_converter import dict_types_files_converter


def script_summary() -> None:
    print('''
               ***----------------------------------------------------------------------------------------***
         \t***------------------------ DUMELANG means GREETINGS! ~ G-CODE -----------------------***
                     \t***------------------------------------------------------------------------***\n

        \t"XML <-> JSON DUAL CONVERTER" Version 1.0.0\n

        This bot will help you convert a JSON file to an XML file type
        and back. Enter the name of the file you want convert.

        Cheers!!
    ''')


def dicts_converting_bot(file_name: str) -> None:
    try:
        dict_types_files_converter(file_name)

    except Exception and FileNotFoundError:
        if FileNotFoundError:
            print(
                '\n\t*** Unable to locate your file. Please make sure you provide a valid file name & '
                'file extension within this folder. ***')
        else:
            raise

    input('\nPress Enter to Exit.')
    sys.exit(0)


def main() -> None:
    script_summary()
    file_name: str = input('\nPlease type the name of the file (including the extension) you would like to convert '
                           'and Press Enter: ')

    if len(file_name.strip()) >= 5:
        if os.path.splitext(file_name)[-1].casefold() not in ['.json', '.xml']:  # Confirming source file type
            input('\nPlease provide a valid file name and file type.')
            sys.exit(1)

        if os.path.exists(file_name):
            dicts_converting_bot(file_name)
        elif FileNotFoundError:
            print(
                '\n\t*** Unable to locate your file. Please make sure you provide a valid file name & '
                'file extension within this folder. ***')
            input('\nPress Enter to Exit: ')
            sys.exit(1)

    elif len(file_name.strip()) < 5 or os.path.splitext(file_name.strip()[-1]) == '':
        print('\nPlease provide a valid file name.')
        input('\nPress Enter to Exit: ')
        sys.exit(1)


if __name__ == '__main__':
    main()
