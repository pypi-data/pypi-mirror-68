from textwrap import fill

def merge_ranges(ranges, clamp=None):
    "Overlapping ranges? Let's fix that. Optionally supply clamp=[0, 100]"
    if any(filter(lambda r: r.step != 1, ranges)): raise ValueError("Ranges must have step=1")
    endpoints = [(r.start, r.stop) for r in sorted(ranges, key=lambda r: r.start)]
    results = []
    if any(endpoints):
        a, b = endpoints[0]
        for start, stop in endpoints:
            if start <= b:
                b = max(b, stop)
            else:
                results.append(range(a, b))
                a, b = start, stop
        results.append(range(a, b))
    if clamp is not None:
        lo, hi = clamp
        results = [range(max(lo, r.start), min(hi, r.stop)) for r in results]
    return results

def prepare_corpus_text(text, width=80, preformatted=False):
    "Splits corpus text at blank lines and wraps it."
    if preformatted:
        outlines = []
        lines = text.split("\n")
        for line in lines:
            while True:
                outlines.append(line[:width])
                if len(line) < 80:
                    break
                line = line[width:]
        return "\n".join(outlines)
    else:
        paragraphs = text.split("\n\n")
        return "\n\n".join(fill(p, width=width) for p in paragraphs)

def prompt_for_choice(prompt, options):
    "Asks for a prompt, returns an index"
    print(prompt)
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        raw_choice = input("> ")
        if raw_choice.isdigit() and int(raw_choice) in range(1, len(options)+1):
            return int(raw_choice)
        print("Sorry, that's not a valid choice.")


def _fmt(opts, _and=True):
    if len(opts) == 1:
        return opts[0]
    else:
        return "{} {} {}".format(", ".join(opts[:-1]), "and" if _and else "or", opts[-1])

class IncompatibleOptions(ValueError):
    pass

class Truthy:
    "Like True, but when used in comparison, coerces the other object to bool."
    val = True
    def __eq__(self, other):
        return bool(other) == self.val

    def __bool__(self):
        return self.val

    def __str__(self):
        return str(self.val) 

class Falsy(Truthy):
    "Like Truthy, but Falsy."
    val = False

def check_incompatible(args, **conditions):
    problem = all(val == getattr(args, opt, None) for opt, val in conditions.items())
    if problem:
        opts = ["--{}".format(k) for k in conditions.keys()]
        if all(conditions.values()):
                message = "{} may not {} be used.".format(_fmt(opts), "both" if len(conditions) == 2 else "all")
        elif not any(conditions.values()):
                message = "One of {} is required.".format(_fmt(opts, _and=False))
        else:
            present = ["--{}".format(o) for o, req in conditions.items() if req]
            absent = ["--{}".format(o) for o, req in conditions.items() if not req]
            message = "{}{} must be used when {} {} used.".format(
                "One of " if len(absent) > 1 else "",
                _fmt(absent), 
                _fmt(present), 
                "is" if len(present) == 1 else "are"
            )
        print(args)
        raise IncompatibleOptions(message)




