from django.db.models import Value
from django.db.models.functions import Lower, Replace
from django.db.models import Expression


def normalize_text(text: str) -> str:
    """
    Normalize user input by converting to lowercase and removing
    spaces, hyphens, and en-dashes.
    """
    # lowercase
    text = text.lower()
    # remove spaces, hyphens, en-dashes
    for char in [' ', '-', '–']:
        text = text.replace(char, '')
    return text


def normalize_jobname_expression(field_name: Expression) -> Expression:
    """
    Returns a Django ORM expression that normalizes job names in the database
    by lowering case and removing spaces, hyphens, and en-dashes.
    """
    # chain Replace functions to remove spaces, hyphens, en-dashes
    expr = Lower(field_name)
    for char in [' ', '-', '–']:
        expr = Replace(expr, Value(char), Value(''))
    return expr
