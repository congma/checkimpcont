import sys
import tokenize


g = tokenize.generate_tokens(sys.stdin.readline)
dumpstr = "%s : %r @ %s - %s\n%s"
for tok, tok_str, start, end, line_text in g:
    print dumpstr % (tokenize.tok_name[tok], tok_str, start, end,
                     line_text.rstrip("\n"))
