
# match-case helper added

def _drift_match_demo(x):
    match x:
        case 1:
            return 'one'
        case _:
            return 'other'
def sum_list(nums):
    s = 0
    for i in range(len(nums)):
        s += nums[i]
    return s

# walrus example
if (n := 5) > 3:
    pass
