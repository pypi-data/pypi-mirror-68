
import re
import sqlparse
from IPython.core.display import display, Markdown
from snowmobile import snowquery
import os


class Statement:

    def __init__(self, sql, connector: snowquery.Connector = ''):

        self.sql = sql
        self.snowflake = snowflake

    def render(self) -> object:
        """Renders SQL as markdown when called in IPython environment.

        Useful when combining explanation of different components of a SQL
        script in IPython or similar environment.

        """
        if isinstance(self.sql, list):
            self.sql = ';\n\n'.join(self.sql)

        display(Markdown(f"```mysql\n{self.sql}\n```"))

        return None

    def raw(self) -> object:
        """Returns raw SQL text."""

        return self.sql

    def execute(self, results=True) -> object:
        """Executes sql and returns results"""
        if results:
            return self.connector.execute_query(self.sql)


class Script(Statement):
    """
    Active-parsing of SQL script in Python for more seamless development loop.

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

    def __init__(self, path: str, pattern: str = r"/\*-(\w.*)-\*/",
                 connector: snowquery.Connector = ''):
        """Instantiating an instance of 'script' by calling Script class
        on a path to a SQL script.

        Structured this way so that each method within the class
        re-instantiates a new instance of 'script' (i.e. re-imports the raw
        file from local).

        This keeps users from having to alter or re-import anything on the
        Python side while editing & saving changes to the SQL file as well as
        ensures that all methods are using the latest version of the script.

        Args:
            path: Full path to SQL script including .sql extension
            pattern:
                (re.pattern) regex pattern that SQL statement headers are
                wrapped in

        Instantiated Attributes:
            script_txt:
                (str) raw SQL script read in as text file
            list_of_statements:
                (list) list of all SQL statements in SQL script (both with and
                without headers)
            statement_names:
                (list) List of statement headers - including blank entries for
                statements that do not have headers (these instances have
                entries equal to '[]')
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
        super().__init__(self)
        self.pattern = pattern
        self.source = path
        self.snowflake = snowflake
        self.name = os.path.split(self.source)[-1].split('.sql')[0]
        self.pattern = re.compile(pattern)
        with open(self.source, 'r') as f:
            self.script_txt = f.read()
        self.list_of_statements = sqlparse.split(self.script_txt)
        self.statement_names = \
            [self.pattern.findall(self.statement) for self.statement in
             self.list_of_statements]

        self.statements = {
            k[0].lower():
                sqlparse.format(v, strip_comments=True).lstrip().rstrip()
            for k, v in zip(self.statement_names, self.list_of_statements)
            if k != []
        }

        self.spans = {val: i for i, val in enumerate(self.statements.keys())}
        self.ordered_statements = [val for val in self.statements.values()]
        self.header_statements = [f"/*-{head.upper()}-*/\n{sql}"
                                  for head, sql in self.statements.items()]
        self.full_sql = ";\n\n".join(self.header_statements)
        self.returned = {}

    def get_statements(self) -> object:
        """Gets dictionary of unique Statement objects & associated methods.

        Returns:
            Dictionary of unique Statement objects & following methods:

        .. code-block:: python

            statement.render()
            statement.run()
            statement.execute()
        """
        for k, v in self.statements.items():
            self.returned[k] = Statement(v, self.snowflake)

        return self.returned

    def run(self) -> None:
        """Executes entire script a statement at a time."
        """
        for raw_sql in self.list_of_statements:
            self.connector.execute_query(raw_sql)
