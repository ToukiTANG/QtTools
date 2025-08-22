from qfluentwidgets import ScrollArea


class HomeInterface(ScrollArea):
    """
    首页interface，可以放一些描述性信息，如公告、使用帮助等
    """

    def __init__(self, parent=None):
        super().__init__(parent)
