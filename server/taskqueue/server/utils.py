def delay_gen(delay=1, base=2, max_delay=64):
    while True:
        if delay > max_delay:
            while True:
                yield max_delay
        else:
            yield delay
            delay *= base
