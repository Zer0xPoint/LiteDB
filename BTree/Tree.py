from BTree.Entity import Entity
from BTree.Node import Node


class Tree(object):
    def __init__(self, size=6):
        self.size = size
        self.root = None
        self.length = 0

    def add(self, key, value=None):
        '''''插入一条数据到B树'''

        self.length += 1

        if self.root:
            current = self.root

            while not current.isLeaf():
                for i, e in enumerate(current.entitys):
                    if e.key > key:
                        current = current.childs[i]
                        break
                    elif e.key == key:
                        e.value = value
                        self.length -= 1
                        return
                else:
                    current = current.childs[-1]

            current.addEntity(Entity(key, value))

            if len(current.entitys) > self.size:
                self.__spilt(current)
        else:
            self.root = Node()
            self.root.addEntity(Entity(key, value))

    def get(self, key):
        '''''通过key查询一个数据'''

        node = self.__findNode(key)

        if node:
            return node.find(key).value

    def delete(self, key):
        '''''通过key删除一个数据项并返回它'''

        node = self.__findNode(key)

        if node:
            i, e = node.delete(key)

            # 在节点不是叶子节点时需要做修复(取对应下标的子节点的最大的一个数据项来补)
            if not node.isLeaf():
                child = node.childs[i]
                j, entity = child.delete(child.entitys[-1].key)
                node.addEntity(entity)

                while not child.isLeaf():
                    node = child
                    child = child.childs[j]
                    j, entity = child.delete(child.entitys[-1].key)
                    node.addEntity(entity)

            self.length -= 1
            return e.value

    def isEmpty(self):
        return self.length == 0

    def __findNode(self, key):
        '''''通过key值查询一个数据在哪个节点,找到就返回该节点'''

        if self.root:
            current = self.root

            while not current.isLeaf():
                for i, e in enumerate(current.entitys):
                    if e.key > key:
                        current = current.childs[i]
                        break
                    elif e.key == key:
                        return current
                else:
                    current = current.childs[-1]

            if current.find(key):
                return current

    def __spilt(self, node):
        '''''
        分裂一个节点，规则为:
        1、中间的数据项移到父节点
        2、新建一个右兄弟节点，将中间节点右边的数据项移到新节点
        '''

        middle = len(node.entitys) / 2

        top = node.entitys[middle]

        right = Node()

        for e in node.entitys[middle + 1:]:
            right.addEntity(e)

        for n in node.childs[middle + 1:]:
            right.addChild(n)

        node.entitys = node.entitys[:middle]
        node.childs = node.childs[:middle + 1]

        parent = node.parent

        if parent:
            parent.addEntity(top)
            parent.addChild(right)

            if len(parent.entitys) > self.size:
                self.__spilt(parent)
        else:
            self.root = Node()
            self.root.addEntity(top)
            self.root.addChild(node)
            self.root.addChild(right)