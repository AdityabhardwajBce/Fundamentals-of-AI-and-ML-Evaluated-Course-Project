# ================================================
# PYPROLOG - Python + Prolog Integration (Single File Version)
# ================================================

# ====================== KNOWLEDGE BASE (Prolog) ======================
prolog_code = """
% Family Relations Knowledge Base
parent(john, mary).
parent(john, peter).
parent(mary, anne).
parent(peter, lucas).
parent(peter, sophia).

male(john).
male(peter).
male(lucas).
female(mary).
female(anne).
female(sophia).

father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \\= Y.
"""

# ====================== MAIN PROGRAM ======================

import tempfile
import os
from pyswip import Prolog
from rich.console import Console
from rich.table import Table
import typer

console = Console()

class PyProlog:
    def __init__(self):
        self.prolog = Prolog()
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load Prolog facts and rules from string"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pl', delete=False) as f:
            f.write(prolog_code)
            temp_file = f.name
        
        try:
            self.prolog.consult(temp_file)
        finally:
            os.unlink(temp_file)  # Clean up temp file

    def query(self, query_str: str):
        """Execute Prolog query"""
        try:
            results = list(self.prolog.query(query_str))
            return results
        except Exception as e:
            return f"Error: {str(e)}"

    def assert_fact(self, fact: str):
        """Add new fact dynamically"""
        try:
            self.prolog.assertz(fact)
            console.print(f"[green]✓ Fact added:[/] {fact}")
        except Exception as e:
            console.print(f"[red]Failed to add fact:[/] {e}")


# ====================== CLI COMMANDS ======================

app = typer.Typer(help="PyProlog - Python + Prolog CLI Tool")
prolog = PyProlog()


@app.command()
def q(query_str: str):
    """Run any Prolog query (short form)"""
    console.print(f"[bold cyan]Query:[/] {query_str}")
    results = prolog.query(query_str)

    if isinstance(results, str):
        console.print(f"[red]{results}[/]")
        return

    if not results:
        console.print("[yellow]No results found.[/]")
        return

    table = Table(title="Results")
    for key in results[0].keys():
        table.add_column(key.capitalize(), style="cyan")
    
    for result in results:
        row = [str(result[key]) for key in result.keys()]
        table.add_row(*row)
    
    console.print(table)


@app.command()
def father(child: str):
    """Find father of a person"""
    results = prolog.query(f"father(F, {child})")
    _print_result("Father", results, "F")


@app.command()
def mother(child: str):
    """Find mother of a person"""
    results = prolog.query(f"mother(M, {child})")
    _print_result("Mother", results, "M")


@app.command()
def grandparents(child: str):
    """Find grandparents"""
    results = prolog.query(f"grandparent(GP, {child})")
    _print_result("Grandparents", results, "GP")


@app.command()
def siblings(person: str):
    """Find siblings"""
    results = prolog.query(f"sibling(S, {person})")
    _print_result("Siblings", results, "S")


@app.command()
def add(fact: str):
    """Add a new fact (e.g. parent(bob, alice))"""
    prolog.assert_fact(fact)


def _print_result(title: str, results, var: str):
    if not results:
        console.print(f"[yellow]No {title.lower()} found.[/]")
        return
    names = [r[var] for r in results]
    console.print(f"[bold green]{title}:[/] {', '.join(names)}")


# ====================== EXECUTION EXAMPLES (Run these commands) ======================

if __name__ == "__main__":
    # Uncomment and run one by one to test:
    
    # app()                    # Run full CLI mode
    
    # Examples:
    # prolog.query("father(X, mary)")
    # prolog.query("grandparent(X, lucas)")
    # prolog.assert_fact("parent(bob, charlie)")
    
    console.print("[bold green]PyProlog is ready! Use commands like:[/]")
    console.print("   python this_file.py q \"father(X, mary)\"")
    console.print("   python this_file.py father mary")
    console.print("   python this_file.py add \"parent(alice, dave)\"")