def find_unique_numbers(s):
    uniques = set()
    left, right = 0, 0
    n = len(s)
    while left < n and right < n:
        if not s[right].isdigit():
            if left != right:
                uniques.add(int(s[left:right]))
            right += 1
            left = right
        else:
            right += 1
    if left != right:
        uniques.add(int(s[left:right]))
    return len(uniques)


def shift_zeroes(li):
    n = len(li)
    left, right = 0, n - 1
    while left < right:
        while li[right] == 0:
            right -= 1
        if li[left] == 0:
            li[left], li[right] = li[right], li[left]
        left += 1
    return li


def main():
    # s = "abc01def123mn2de122"
    # print(find_unique_numbers(s))
    li = [0, 1, 2, 3, 0, 0, 3, 0, 0]
    print(shift_zeroes(li))


if __name__ == "__main__":
    main()
