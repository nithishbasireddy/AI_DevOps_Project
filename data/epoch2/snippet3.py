
# match-case helper added

def _drift_match_demo(x):
    match x:
        case 1:
            return 'one'
        case _:
            return 'other'
def find_max(arr):
    maximum = arr[0]
    for x in arr:
        if x > maximum:
            maximum = x
    return maximum

# walrus example
if (n := 5) > 3:
    pass
