1)How to start :

# PyProlog

A lightweight single-file **Python + Prolog** integration tool with a rich CLI for working with logic programming and knowledge bases.

Built using `pyswip` and `rich` for a beautiful terminal experience.

## Features

- Embed Prolog knowledge base directly in Python
- Easy-to-use CLI commands
- Dynamic fact assertion at runtime
- Rich formatted output with tables
- Family relationship example included

## Installation

```bash
pip install pyswip typer rich


2)Quick Start:

# Run the tool
python pyprolog.py


3)Example Commands:

# Run any Prolog query
python pyprolog.py q "father(X, mary)"

# Find specific relations
python pyprolog.py father mary
python pyprolog.py mother anne
python pyprolog.py grandparents lucas
python pyprolog.py siblings sophia

# Add new facts dynamically
python pyprolog.py add "parent(mary, bob)"
python pyprolog.py add "male(bob)"


4)Available Commands:


Command	                Description

q <query>		Run any custom Prolog query
father <child>		Find father of a person
mother <child>		Find mother of a person
grandparents<child>	Find grandparents
siblings <person>	Find siblings
add "<fact>"		Add new fact (e.g. parent(X,Y))
facts			List all facts in the knowledge base