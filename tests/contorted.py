# vim: set encoding=utf-8
"""
A test case file.  Currently containing valid Python code only.
"""
# must find 7 warnings
x = ("a-shouldfind"
        "b-shouldfind"  # some trailing spaces
                        # more hanging comments

"c-shouldfind"
# Coment line, MOAR newlines
# Comment block


"" # shouldfind
     # The following is an explicit continuation
  "d" \
     "e",
     ["sp"  # shouldfind
      "am", "eggs", u"œu-shouldfind"
      u"fs",
      None
      ],
         "f"
     "g" "h"    # shouldfind

     # Last item in seq with closing-paren on another line.
     # Shouldn't generate warning.
     "x"


# Again

 )

y = "i"
z = "j"
