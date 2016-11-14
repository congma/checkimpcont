# vim: set encoding=utf-8
"""
A test case file.  Currently containing valid Python code only.
"""
# must find 10 warnings
x = ("a"    # XXX
        "b"  # some trailing spaces, XXX
                        # more hanging comments

"c"    # XXX
# Coment line, MOAR newlines
# Comment block


""  # XXX
     # The following is an explicit continuation, XXX
  "d" \
     "e",
     ["sp"  # XXX
      "am", "eggs", u"œu"  # XXX
      u"fs",
      None
      ],
         "f"    # XXX
     "g" "h"    # XXX XXX

     # Last item in seq with closing-paren on another line.
     # Shouldn't generate warning.
     "x"


# Again

 )

y = "i"
z = "j"
