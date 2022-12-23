class Namespace(object):
    def __init__(self) -> None:
        super().__init__()

        self._parent = None

        # what to prefix namespace symbols with
        self._mangle = ""

    # @param name - what this namespace is called in user code
    # @param parent - parent namespace
    def __init__(self, name, parent):
        self._parent = parent
        self._calcMangle()

    def _calcMangle(self):
        curParent = self._parent
        mangle = ""

        while curParent != None:
            mangle = curParent.getMangle() + "_" + mangle
            curParent = curParent.getParent()

        mangle +=

    def getMangle(self):
        return self._mangle

    def getParent(self):
        return self._parent

GLOBAL_NAMESPACE = "__global"