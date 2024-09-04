import re

def compile_patterns(patterns): return [
    (re.compile(pattern), repl) for pattern, repl in patterns]
