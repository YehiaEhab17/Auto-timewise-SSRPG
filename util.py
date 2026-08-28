def choose_number(message, retry=False, default=1, max=-1):
    # default only used if retry is false
    while True:
        choice = input(message).strip()
        try:
            choice = int(choice)
            if choice < max and choice > 0:
                return choice

        except ValueError:
            print("invalid input")

        if retry:
            continue

        return default
