from BPTree import BPlusTree

tree = BPlusTree(filename="/Users/rileylee/Documents/PyCharmProjects/LiteDB/BPTree/bptree.db", order=50)
tree.insert(1, b"hello")
tree.insert(3, b"world")

value = tree.get(1).decode()

print(value)

for i in tree:
    print(i)