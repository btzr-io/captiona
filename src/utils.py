import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from langcodes import *

def printJson (data):
    json_str = json.dumps(data, indent=4, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))

def validate_name(entry, id):
    if "language" in entry and id:
        # Generate expected format for name
        expected = entry["language"] + '_' + id
        # Validate format
        return entry["name"] == expected
    # Missing metadata
    return false

# See: https://github.com/LuminosoInsight/langcodes/issues/28
def validate_language(lang):
    return lang.language_name() != lang.language
