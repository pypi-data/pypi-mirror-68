# Python Quick SQL 
*A light-weight (out-of-the box) tool for pushing SQL (MySQL and SQLite) queries, markup-language for structured txt files and running data loggers in python.*

	pip install pyquicksql==1.0

## SQL Queries
Designed as a purely light-weight and object-oriented aproach to sending MySQL and SQLite queries to a database server from python. Current modules offer partialy oo aproaches, resulting in over-complicated syntax for simple sql queries. The goal is that this module will offer ease-of-use in comparison to other modules while providing faster development time. 

### Supported Databases
	
1. __MySQL__ (v.7.0)
2. __SQLite__ (v.3.31.1)

### Functionality

#### Constructors
	server = Server('0.0.0.0.0', 800, username, password)
	database = Database('users', 'credentials', True)
	connector = Connect(server, database)

Lookup
> result = connector.lookup(unknown_column, known_colum, known_element)

Push
> result = connector.push(columns, elements)

Swap
> result = connector.swap(unknown_data, known_data)

Remove
> result = connector.remove(column, element)

## Logger
The logger offers developers who wish to log all sql traffic localy within their project OR for those who do not wish to overcomplicate their projects with SQL queries and use standard txt files. The goal is to offer a basic but efficient markup language which mimics relational tables found within MySQL for faster lookup times for values. This is (yet another) out-of-the-box module the package promises, to speed up development time by offering individuals who do not know how to make their own relational markup language.

### Functionality

#### Constructor

	l = Logger(directory) <- directory must be an active file path
	
Retreive Logs
> backup = l.getLogs()

Log
> l.log(Server, Database, Message)

Index
> value = l.index(0)

Lookup
> value = l.lookup(column, element, starting)

#### Data Markup
The 'Data Markup' is a markup-language designed with Rust and interface with python to offer the speed that it cannot. The language offers relational column-element formating for standard txt files for faster data lookup and retreival.

Syntax
> <Server<>Database>?Time?!Message!

Parse
> value = l.parse(line, Request)

Request Types
1. Column.SERVER
2. Column.DATABASE
3. Column.TIMESTAMP
4. Column.MESSAGE
	
## Credits

pyquickdb
> Gabriel Cordovado

	Functionality of all classes are not limited to this README, I encourage your to view the source
