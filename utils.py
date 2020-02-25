import re
import sys

specials = [r"==>", r"->", r"\.\.\.", r">>", r"=\)\)"]
email = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
urls = r"""             # Capture 1: entire matched URL
  (?:
  (ftp|http)s?:               # URL protocol and colon
    (?:
      /{1,3}            # 1-3 slashes
      |                 #   or
      [a-z0-9%]         # Single letter or digit or '%'
                        # (Trying not to match e.g. "URI::Escape")
    )
    |                   #   or
                        # looks like domain name followed by a slash:
    [a-z0-9.\-]+[.]
    (?:[a-z]{2,13})
    /
  )
  (?:                                  # One or more:
    [^\s()<>{}\[\]]+                   # Run of non-space, non-()<>{}[]
    |                                  #   or
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\) # balanced parens, one level deep: (...(...)...)
    |
    \([^\s]+?\)                        # balanced parens, non-recursive: (...)
  )+
  (?:                                  # End with:
    \([^\s()]*?\([^\s()]+\)[^\s()]*?\) # balanced parens, one level deep: (...(...)...)
    |
    \([^\s]+?\)                        # balanced parens, non-recursive: (...)
    |                                  #   or
    [^\s`!()\[\]{};:'".,<>?«»“”‘’]     # not a space or one of these punct chars
  )
  |                        # OR, the following to match naked domains:
  (?:
    (?<!@)                 # not preceded by a @, avoid matching foo@_gmail.com_
    [a-z0-9]+
    (?:[.\-][a-z0-9]+)*
    [.]
    (?:[a-z]{2,13})
    \b
    /?
    (?!@)                  # not succeeded by a @,
                           # avoid matching "foo.na" in "foo.na@example.com"
  )
"""
datetime = [
    r"\d{1,2}\/\d{1,2}(\/\d+)",
    r"\d{1,2}-\d{1,2}(-\d+)?",
    r"\d{1,2}am|\d{1,2}pm"
]
money = [
    r"\s\d{1,5}k\s|\d{1,5}vnd|\d{1,3}\.\d{3,3}\svnđ",
    r"\d{3,10}đ",
    r"\d{1,3}\s{1,1}\d+đ",
    r"\d{1,3}\.\d+đ",
    r"\d{1,2}\.\d{3,3}k",
    r"\d{1,5}k\/\d",
    r"\d{1,3}\stiền",
    r"giá\s\d{1,3}k\/\d\scái",
    r"\d{1,3}ngàn"
]
non_word = r"[^\w\s\/\-\.\,\+]"
abbreviations = [
    r"[A-ZĐ]+\.",
    r"Tp\.",
    r"Mr\.", "Mrs\.", "Ms\.",
    r"Dr\.", "ThS\."
]
dimensions = [
    r"m\d{1,2}|\d{1,1}m\d{1,2}|\d{1,3}cm|\d{1,2}\,\d+m|\d{1,2}\.\d+m",
    r"^\d{1,2}kg|\/kg",
    r"^\d{1,2}\skg",
    r"^\d{1,3}g",
    r"^\d{1,2}h",
    r"^\d{1,3}\.\d+inch",
    r"^\d{1,4}sp|\d{1,4}c",
    r"^\d{1,4}ml",
    r"^\d{1,3}\scái",
    r"^\d{1,3}\sset",
    r"^\d{1,2}\sđộ",
    r"^\d{1,2}\slit"
]
phones = [
    r"\d{2,4}(\.\d{2,3}){2,3}",
    r"\d{3,3}\s\d{7,12}",
    r"\d{3,4}\s\d{3,3}\s\d{3,4}",
    r"\d{7,10}\s\d{3,4}"
]

patterns = []
patterns.extend(specials)
patterns.extend([urls])
patterns.extend([email])
patterns.extend(abbreviations)
patterns.extend(datetime)
# patterns.extend(dimensions)
patterns.extend([non_word])

patterns = "(" + "|".join(patterns) + ")"
if sys.version_info < (3, 0):
    patterns = patterns.decode('utf-8')
patterns = re.compile(patterns, re.VERBOSE | re.UNICODE)


def tokenize(text):
    text = patterns.sub('', text)
    return text
