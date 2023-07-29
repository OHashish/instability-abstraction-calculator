# instability-abstraction-calculator
The program calculates instability and abstractness of a chosen java package.

Libraries:-

The python file only needs javalang library to work.

pip or pip3 install javalang should work.

https://github.com/c2nes/javalang

Javalang was designed to provide and target Java 8 . When tested it works for newer versions.


Notes:
-The program assumes that there are no classes with the same name in two different packages.

-The program calculates total number of classes by counting all classes + number of abstract classes+ interfaces.

- In this program , dependencies are classes that would not work without the existence of another class. If a Class creates another class, uses one of its members or attributes is considered a dependency.


How to use:
 1. Simply run the python files.
 2. You will prompted to enter the full path of the directory that contains all of the packages (its preferable to no have the directory containing the tests in it) , the program excludes any java file containing the characters 'test' in their name.

3. Then you will be prompted to enter the name of the package you want to get its abstractness and instability.
