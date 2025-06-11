from django.db.models import Value
from django.db.models.functions import Lower, Replace
from django.db.models import Func, F, Expression


def normalize_text(text: str) -> str:
    """
    Normalize user input by converting to lowercase and replacing 
    hyphens/en-dashes with spaces.
    """
    return text.lower().replace("-", " ").replace("–", " ")


def normalize_jobname_expression(field_name: str) -> Expression:
    """
    Returns a Django ORM expression that normalizes job names in the database.
    Used for filtering job names in a consistent way.
    """
    return Replace(
        Replace(Lower(field_name), Value("-"), Value(" ")),
        Value("–"), Value(" ")
    )
