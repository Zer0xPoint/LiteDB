class Node(object):
    def __init__(self):
        self.parent = None
        self.entitys = []
        self.childs = []

    def find(self, key):
        '''''通过key查找并返回一个数据实体'''

        for e in self.entitys:
            if key == e.key:
                return e

    def delete(self, key):
        '''''通过key删除一个数据实体,并返回它和它的下标(下标,实体)'''
        for i, e in enumerate(self.entitys):
            if e.key == key:
                del self.entitys[i]
                return (i, e)

    def isLeaf(self):
        '''''判断该节点是否是一个叶子节点'''

        return len(self.childs) == 0

    def addEntity(self, entity):
        '''''添加一个数据实体'''

        self.entitys.append(entity)
        self.entitys.sort(key=lambda x: x.key)

    def addChild(self, node):
        '''''添加一个子节点'''

        self.childs.append(node)
        node.parent = self
        self.childs.sort(key=lambda x: x.entitys[0].key)