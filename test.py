import heapq

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __lt__(self, other):
        return (self.age, self.name) < (other.age, other.name)

people = [
    Person('Alice', 30),
    Person('Bob', 20),
    Person('Charlie', 20)
]

heapq.heapify(people)

youngest_person = heapq.heappop(people)
print(youngest_person.name)  # Gibt 'Bob' aus
