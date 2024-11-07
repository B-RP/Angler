BY_VALUE = 'by_value'

class Predicate:
    def __init__(self, args):
        self.args = args


class ByValue(Predicate):
    def __init__(self,args):
        super().__init__(args)

    def match(self, item) -> bool:
        if(item in self.args):
            return True
        else:
            return False

class ByMaxValue(Predicate):
    def __init__(self,args):
        super().__init__(args)
        if(len(self.args) != 1):
            raise Exception("ByMaxValue predicate takes exactly one argument")
        self.max_value = args[0].content

    def match(self, item) -> bool:
        try:
            num = float(item)
        except:
            return False
        if(num <= self.max_value):
            return True
        else:
            return False
        
class ByEndsWith(Predicate):
     
    def __init__(self,args):
        super().__init__(args)

    def match(self, item):
        if(item.endswith(tuple(map(str,self.args)))):
            return True
        
        False

        
class ByValueAtCol(Predicate):
    def __init__(self, args):
        super().__init__(args)
        if(len(args) != 2):
            raise Exception("ByValueAtCol takes 2 arguments, value and column")
        
        self.value = args[0].content
        self.col = args[1].content

    def match(self, row:list):
        if(row[self.col] == self.value):
            return True
        return False
    
class ByMaxValueAtCol(Predicate):
    def __init__(self, args):
        super().__init__(args)
        if(len(args) != 2):
            raise Exception("ByValueAtCol takes 2 arguments, value and column")
        
        self.value = args[0].content
        self.col = args[1].content

    def match(self, row:list):
        try:
            num = float(row[self.col])
        except:
            return False
        
        if(num <= self.value):
            return True
        return False

class ByMinValueAtCol(Predicate):
    def __init__(self, args):
        super().__init__(args)
        if(len(args) != 2):
            raise Exception("ByValueAtCol takes 2 arguments, value and column")
        
        self.value = args[0].content
        self.col = args[1].content

    def match(self, row:list):
        try:
            num = float(row[self.col])
        except:
            return False
        if(num >= self.value):
            return True
        return False
        
predicates = {'ByValue':ByValue, 'ByMaxValue':ByMaxValue, "ByEndsWith":ByEndsWith, "ByValueAtCol":ByValueAtCol, "ByMaxValueAtCol":ByMaxValueAtCol, "ByMinValueAtCol":ByMinValueAtCol}