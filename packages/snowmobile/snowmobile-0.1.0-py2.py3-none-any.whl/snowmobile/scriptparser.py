
import re
import sqlparse
from IPython.core.display import display, Markdown


class ParseScript:
    """
    Active-parsing of SQL script in Python for seamless development loop.

    Enables flexible parsing of a SQL script into individual statements or
    spans of statements based on statement headers declared in SQL script.
    These should be denoted by placing headers above the statements within
    within the SQL file as shown below:

    .. code-block:: sql

        /*-statement_header-*/
        create or replace table sample_table as
        select
            *
        from sample_other

    """

    def __init__(self, path: str):
        """Instantiating an instance of 'script' by calling ParseScript class
        on a path to a SQL script.

        Structured this way so that each method within the class
        re-instantiates a new instance of 'script' (i.e. re-imports the raw
        file from local).

        This keeps users from having to alter or re-import anything on the
        Python side while editing & saving changes to the SQL file as well as
        ensures that all methods are using the latest version of the script.

        Args:
            path: Path to SQL script including file name

        Attributes:
        path:
            (str) path to SQL script
        pattern:
            (re.pattern) regex pattern that SQL statement headers are
            wrapped in
        script_txt:
            (str) raw SQL script read in as text file
        list_of_statements:
            (list) list of all SQL statements in SQL script (both with and
            without headers)
        statement_names:
            (list) List of statement headers - including blank entries for
            statements that do not have headers (these instances have entries
            equal to '[]')
        statement:
            (dict) Dictionary containing {'header': 'associated_sql'} - note
            the conditionals within the comprehensions that throw out entries
            from both lists that do not have a valid statement_header
        spans:
            (dict) Dictionary containing {'header': 'index_position_in_script'}
            and is used in the get_span() method
        ordered_statements:
            (list) List of statements in the order in which they appear in the
            script. Note that these are only statements that have a valid
            headers in the SQL file
        header_statements:
            (str) List of all statements with their headers prepended to them,
            same length as ordered_statements
        full_sql:
            (str) String containing all statements with valid headers combined
            into a single string.

        """
        self.path = path
        self.pattern = re.compile(r"/\*-(\w+)-\*/")
        self.script_txt = open(path).read()
        self.list_of_statements = self.script_txt.split(";")
        self.statement_names = [
            self.pattern.findall(self.statement)
            for self.statement in self.list_of_statements
        ]
        self.statement = {
            k[0].lower(): sqlparse.format(v, strip_comments=True).lstrip().rstrip()
            for k, v in zip(self.statement_names, self.list_of_statements)
            if k != []
        }
        self.spans = {val: i for i, val in enumerate(self.statement.keys())}
        self.ordered_statements = [val for val in self.statement.values()]
        self.header_statements = [
            f"/*-{head.upper()}-*/\n{sql}" for head, sql in self.statement.items()
        ]
        self.full_sql = ";\n\n".join(self.header_statements)

    def get_statement(self, header: str) -> str:
        """Returns a SQL statement given a statement header.

        For executing a single statement at a time - can also be used in
        conjunction with the iterable attributes or returned iterable from
        get_span() method.

        Args:
            header: Header for statement in SQL script
        Returns:
            Associated SQL statement based on header

        """
        self.script = ParseScript(self.path)

        self.statement = self.script.statement[header.lower()]

        return self.statement

    def span_from_headers(self, first: str, last: str) -> list:
        """Returns a list of statements given the headers bounding the range.

        This gives users the ability to create multiple spans representing
        different parts of their script and execute separately if desired.

        Args:
            first: Header of the first statement in the range
            last: Header of the last statement in the range
        Returns:
            A list of executable SQL statements within the [first, last] range.

        """
        self.start = self.spans[first]
        self.finish = self.spans[last]
        self.indexed_statements = {v: k for k, v in self.spans.items()}
        self.range_statements = [
            self.indexed_statements[i] for i in range(self.start, self.finish)
        ]
        self.statements = [
            f"/*-{head.upper()}-*/\n{self.get_statement(head)}"
            for head in self.range_statements
        ]
        return self.statements

    def span_from_index(self, lower: int, upper: int) -> list:
        """Returns a list of statements given the indices bounding the range.

        This gives users the ability to create multiple spans representing
        different parts of their script and execute separately if desired.

        Args:
            lower: Index of the first statement in the range
            upper: Index of the last statement in the range
        Returns:
            A list of executable SQL statements within the [first, last] range.

        """
        self.lower = lower
        self.upper = upper
        self.indexed_statements = {v: k for k, v in self.spans.items()}
        self.range_statements = [
            self.indexed_statements[i] for i in range(self.lower, self.upper
                                                      + 1)]
        self.statements = [
            f"/*-{head.upper()}-*/\n{self.get_statement(head)}"
            for head in self.range_statements]

        return self.statements

    def render_sql(self, sql: str) -> None:
        """Renders SQL as markdown when called in IPython environment.

        Useful when combining explanation of different components of a SQL
        script in notebook or similar environment.

        Args:
            sql: Raw SQL text to display
        """
        if isinstance(sql, list):
            self.sql = ';\n\n'.join(sql)

        display(Markdown(f"```mysql\n{self.sql}\n```"))

        return None



