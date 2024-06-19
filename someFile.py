import collections


def product_pair(nums: list, product: int) -> list:
    result = []
    mapping = collections.defaultdict(int)
    for num in nums:
        mapping[num] += 1

    for num in nums:
        complement = product // num
        if complement in mapping and mapping[complement] > 0:
            mapping[num] -= 1
            mapping[complement] -= 1
            result.append((num, complement))
    return result


def main():
    ls = [1, 12, 13, 3, 4, 1, 2, 12, 6, 4]
    prod = 12
    print(product_pair(ls, prod))  # [(1, 12), (3, 4), (1, 12), (2, 6)]


if __name__ == "__main__":
    main()



"""

Students - Class : One-to-many

Teachers - Class : Many-to-many

Subjects - Class : Many-to-many

Teachers - Subject : Many-to-one


select name from teachers where class = (select class from students where student.name = 'yasir')

from django.db.models import Subquery

subquery = Students.objects.filter(name="yasir")
Teachers.objects.filter(class__in=Subquery(subquery))
"""
