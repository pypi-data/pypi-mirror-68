from os import path
from robot.parsing.model import ResourceFile
from .testDataVisitor import FindVisitor, TestDataNode, TestDataVisitor
class TestDataDependencyBuilder:
    def __init__(self):
        self.root = None

    def build(self,testDataDir):
        def merge_resources_tree(resource_trees):
            def get_unimported_resource(trees):
                for tree in trees:
                    source = tree.source
                    if all([not FindVisitor(target, source).has_result() for target in trees if target.source!=source]):
                        return tree
                
                return trees[0]
            trees = [tree for tree in resource_trees.values()]
            trees_after_sort = []
            for index in range(len(trees)):
                un_import_tree = get_unimported_resource(trees)
                trees_after_sort.append(un_import_tree)
                trees.remove(un_import_tree)
            root = TestDataNode(testDataDir)
            root.add_child(trees_after_sort.pop(0))
            for resource_root in trees_after_sort:
                find_visitor = FindVisitor(root, resource_root.source)
                if find_visitor.has_result():
                    for node in find_visitor.get_result():
                        parent = node.parent
                        if parent:
                            parent.remove_child(node)
                            parent.add_child(resource_root)
                else:
                    root.add_child(resource_root)
            return root
        def build_resource_tree(testData, resource_trees):
            for lib in testData.imports:
                source = path.normpath(testData.directory+'/'+lib.name)
                extension = path.splitext(source)[1]
                if path.exists(source) and extension !=".py":
                    if source not in resource_trees.keys():
                        resource = ResourceFile(source=source).populate()
                        node = TestDataNode(resource)
                        node.add_child(TestDataNode(testData))
                        resource_trees[source] = node
                        build_resource_tree(resource, resource_trees)
                    else:
                        resource_trees[source].add_child(TestDataNode(testData))
            for child in testData.children:
                build_resource_tree(child, resource_trees)

        resource_trees = {}
        build_resource_tree(testDataDir,resource_trees)
        return merge_resources_tree(resource_trees)