"""Document (overall window) class implementation.
"""

from apysc._type.variable_name_interface import VariableNameInterface


class Document(VariableNameInterface):

    def __init__(self) -> None:
        """
        Document (overall window) class.
        """
        from apysc._expression import var_names
        self.variable_name = var_names.DOCUMENT


document: Document = Document()
