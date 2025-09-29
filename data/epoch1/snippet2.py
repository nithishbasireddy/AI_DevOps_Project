def sum_list(nums):
    s = 0
    for i in range(len(nums)):
        s += nums[i]
    return s

# walrus example
if (n := 5) > 3:
    pass
