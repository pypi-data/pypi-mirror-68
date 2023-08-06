# newpyproj
### *Automated Python Project Folder Creation*
------

Automatically creates a *new python project folder*, using best project standards, with common files, documentation, tests.


## Installation

    pip install newpyproj

## Usage

    newpyproj name_of_project [-h] [-c] [-g] [-v] [-p] [-r] [-s] [-t] [-d] [--template]


## Arguments

    -h or --help       Help message and exit
    -c or --cli        Creates a command line interface project
    -g or --gui        Creates a graphical user interface project
    -v or --verbose    Verbose mode
    -p or --pytest     Use pytest as unittest
    -r or --resources  Include resources folder
    -s or --shebang    Supress shebang line in files
    -t or --test       Supress test folders and files
    -d or --doc        Supress doc folders and files
    --template         Supress template content in files

## References

[Structuring Your Project](http://docs.python-guide.org/en/latest/writing/structure/) by Kenneth Reitz

[Python Application Layouts: A Reference](https://realpython.com/python-application-layouts/) by Kyle Stratis

[Dead Simple Python: Project Structure and Imports](https://dev.to/codemouse92/dead-simple-python-project-structure-and-imports-38c6) by Jason C. McDonald