from Parser import *
from Predicate import *
from os.path import exists

class Structure:
    def __init__(self):
        self.type = "Structure"

    def Filter(self):
        raise Exception(f"Filter operation not implemented for {self.type}")
    
    def Remove(self):
        raise Exception(f"Remove operation not implemented for {self.type}")
    
    def Replace(self):
        raise Exception(f"Replace operation not implemented for {self.type}")
    
    def Count(self):
        raise Exception(f"Count operation not implemented for {self.type}")
    
    def Iterate(self):
        raise Exception(f"{self.type} iteration is not implemented")
    
    def Print(self):
        raise Exception(f"Print operation not implemented for {self.type}")
    
    def Read(self):
        raise Exception(f"Read operation not implemented for {self.type}")
    
    def Write(self):
        raise Exception(f"Write operation not implemented for {self.type}")

class File(Structure):
    def __init__(self, args):
        self.content = None
        if(len(args) != 2):
            raise Exception("Expected 2 arguments")
        
        path = args[0]
        if(type(args[0]) == Text):
            path = args[0].content
        
        file_type = args[1]
        match file_type.content:
            case "TEXT":
                self.content = TEXTFile(path)
            case "CSV":
                self.content = CSVFile(path)
            case _:
                raise Exception(f"Could not recognize file type {file_type.content}")

    def Filter(self, args, isExpr):
        if(isExpr):
            return self.content.Filter(args, isExpr)
        else:
            return self.content.Filter(args, isExpr)

    def Remove(self, args, isExpr):
        if(isExpr):
            return self.content.Remove(args, isExpr)
        else:
            self.content.Remove(args, isExpr)

    def Replace(self, args, isExpr):
        if(isExpr):
            return self.content.Replace(args, isExpr)
        else:
            self.content.Replace(args, isExpr)

    def Count(self, args, isExpr):
        if(isExpr):
            return self.content.Count(args, isExpr)
        else:
            raise Exception("Count operation can only be performed as an expression")

    def Print(self, args, isExpr):
        if(isExpr):
            raise Exception("Print operation cannot be performed as an expression")
        else:
            self.content.Print(args, isExpr)

    def Read(self, args, isExpr):
        if(isExpr):
            return self.content.Read(args)
        else:
            raise Exception("Read operation can only be performed as an expression")
    

class CSVFile(Structure):
    def __init__(self, path):
        self.path = path

    def Filter(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception("File does not exist and cannot be filtered")
        #Arg verification
        if(args[0][0] is None):
            raise Exception("Filter CSV File operation requires an object member to filter")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Filter Text File operation requires a predicate to filter by. Encountered {type(args[1])}")
        
        if(args[2]):
            raise Exception(f"Filter Text File operation does not accept additional arguments")
        
        target = args[0][0] #String
        isPlural = args[0][1] #Boolean

        newVal = None

        if(target == "Record"):
            newVal = self.__filter_records(isPlural, args[1])
        elif(target == "Field"):
            raise Exception("Filter by Fields is not implemented in CSV File")
        elif(target == "Value"):
            raise Exception("Cannot Filter by value in CSV File")
        else:
            raise Exception("Object memeber not recognized")

        if(isExpr):
            return Text(newVal)
        else:
             with open(self.path, "w+", encoding="utf-8") as f:
                 f.write(newVal)

    def __filter_records(self, isPlural, predicate):
        newVal = ""
        with open(self.path, encoding="utf-8") as f:
            lines = [line.rstrip() for line in f]

            for line in lines:
                row = line.split(',')
                if(predicate.match(row)):
                    newVal += line
                    newVal += "\n"
                    if(not isPlural):
                        break
        return newVal

    def Remove(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception("File does not exist")
        #Arg verification
        if(args[0][0] is None):
            raise Exception("Remove CSV File operation requires an object member")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Remove CSV File operation requires a predicate")
        
        if(args[2]):
            raise Exception(f"Remove CSV File operation does not accept additional arguments")
        
        target = args[0][0] #String
        isPlural = args[0][1] #Boolean

        newVal = None

        if(target == "Record"):
            newVal = self.__remove_records(isPlural, args[1])
        elif(target == "Field"):
            raise Exception("Remove by Fields is not implemented in CSV File")
        elif(target == "Value"):
            raise Exception("Cannot Remove by value in CSV File")
        else:
            raise Exception("Object memeber not recognized")

        if(isExpr):
            return Text(newVal)
        else:
             with open(self.path, "w+", encoding="utf-8") as f:
                 f.write(newVal)

    def __remove_records(self, isPlural, predicate):
        newVal = ""
        with open(self.path, encoding="utf-8") as f:
            lines = [line.rstrip() for line in f]

            for line in lines:
                row = line.split(',')
                if(not predicate.match(row)):
                    newVal += line
                    newVal += "\n"
                    if(not isPlural):
                        break
        return newVal

    def Replace(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception("File does not exist")
        #Arg verification
        if(args[0][0] is None):
            raise Exception("Replace CSV File operation requires an object member")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Replace CSV File operation requires a predicate")
        
        if(len(args[2]) != 1):
            raise Exception(f"Replace CSV File operation requires one additional arguments")
        
        target = args[0][0] #String
        isPlural = args[0][1] #Boolean


        newVal = None

        if(target == "Record"):
            raise Exception("Cannot Remove by value in CSV File")
        elif(target == "Field"):
            raise Exception("Remove by Fields is not implemented in CSV File")
        elif(target == "Value"):
            newVal = self.__replace_values(isPlural, args[1], args[2][0])
        else:
            raise Exception("Object memeber not recognized")

        if(isExpr):
            return Text(newVal)
        else:
             with open(self.path, "w+", encoding="utf-8") as f:
                 f.write(newVal)

    def __replace_values(self, isPlural, predicate, replacement):
        newVal = ""
        with open(self.path, encoding="utf-8") as f:
            lines = [line.rstrip() for line in f]

            for line in lines:
                row = line.split(',')

                for item in row:
                    if(predicate.match(item)):
                        newVal += replacement.content
                    else:
                        newVal += item
                    newVal+=','
                newVal += '\n'
        return newVal


    def Print(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception(f"File {self.path} does not exist and cannot be printed")
        #Arg verification
        if(args[0][0] is not None):
            raise Exception("Print Text File operation does not accept an object member")
        
        if(args[1]):
            raise Exception("Print Text File operation does not accept a predicate")
        
        if(args[2]):
            raise Exception("Print Text File operation does not accept additional arguments")
        
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                print(L)

class TEXTFile(Structure):
    def __init__(self, path):
        self.path = path

    def Filter(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception("File does not exist and cannot be filtered")
        #Arg verification
        if(args[0][0] is None):
            raise Exception("Filter Text File operation requires an object member to filter by")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Filter Text File operation requires a predicate to filter by. Encountered {type(args[1])}")
        
        if(args[2]):
            raise Exception(f"Filter Text File operation does not accept additional arguments")
        
        target = args[0][0] #String
        isPlural = args[0][1] #Boolean

        newVal = None

        if(target == "Text"):
            newVal = self.__filter_text(isPlural, args[1])

        elif(target == "Line"):
            newVal = self.__filter_lines(isPlural, args[1])

        elif(target == "Word"):
            newVal = self.__filter_words(isPlural, args[1])

        if(isExpr):
            return Text(newVal)
        else:
             with open(self.path, "w+") as f:
                 f.write(newVal)

    def __filter_lines(self, isPlural, predicate):
        newVal = ""
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                if(predicate.match(L)):
                    newVal += L
                    newVal += "\n"
                    if(not isPlural):
                        break
        return newVal

    def __filter_words(self, isPlural, predicate):
        newVal = ""
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                line = ""
                for word in L.split():
                    if(predicate.match(word)):
                        line += word
                        line += " "
                        if(not isPlural):
                            break
                if line != "":
                    line += "\n"
                    newVal += line

        return newVal


    def Remove(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception("File does not exist and cannot be altered")
        #Arg verification
        if(args[0][0] is None):
            raise Exception("Remove Text File operation requires an object member to remove")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Remove Text File operation requires a predicate to remove by")
        
        if(args[2]):
            raise Exception(f"Remove Text File operation does not accept additional arguments")
        
        target = args[0][0] #String
        isPlural = args[0][1] #either s or none

        newVal = None

        if(target == "Text"):
            newVal = self.__remove_text(isPlural, args[1])

        elif(target == "Line"):
            newVal = self.__remove_lines(isPlural, args[1])

        elif(target == "Word"):
            newVal = self.__remove_words(isPlural, args[1])

        if(isExpr):
            return Text(newVal)
        else:
             with open(self.path, "w+") as f:
                 f.write(newVal)

    def __remove_lines(self, isPlural, predicate):
        newVal = ""
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                if(not predicate.match(L)):
                    newVal += L
                    newVal += "\n"
                    if(not isPlural):
                        break
        return newVal

    def __remove_words(self, isPlural, predicate):
        newVal = ""
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                line = ""
                for word in L.split():
                    if(not predicate.match(word)):
                        line += word
                        line += " "
                        if(not isPlural):
                            break
                if line != "":
                    line += "\n"
                    newVal += line

        return newVal


    def Replace(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception(f"File {self.path} does not exist and cannot be altered")
        #Arg verification
        if(args[0][0] is None):
            raise Exception("Replace Text File operation requires an object member to replace")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Replace Text File operation requires a predicate to replace by")
        
        if(len(args[2]) != 1):
            raise Exception(f"Replace Text File operation requires one additional replacement argument. {len(args[2])} was given")
        
        target = args[0][0] #String
        isPlural = args[0][1] #either s or none

        newVal = None

        if(target == "Text"):
            newVal = self.__replace_text(isPlural, args[1], args[2][0])

        elif(target == "Line"):
            newVal = self.__replace_lines(isPlural, args[1], args[2][0])

        elif(target == "Word"):
            newVal = self.__replace_words(isPlural, args[1], args[2][0])

        if(isExpr):
            return Text(newVal)
        else:
             with open(self.path, "w+") as f:
                 f.write(newVal)

    def __replace_lines(self, isPlural, predicate, replacement):
        newVal = ""
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                if(predicate.match(L)):
                    newVal += replacement
                    newVal += "\n"
                    if(not isPlural):
                        break
                else:
                    newVal += L
                    newVal += "\n"

        return newVal

    def __replace_words(self, isPlural, predicate, replacement):
        newVal = ""
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                line = ""
                for word in L.split():
                    if(predicate.match(word)):
                        line += replacement
                        line += " "
                        if(not isPlural):
                            break
                    else:
                        line += word
                        line += " "
                if line != "":
                    line += "\n"
                    newVal += line

        return newVal


    def Count(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception("File does not exist and cannot be counted")
        #Arg verification
        if(args[0][0] is None):
            raise Exception("Count Text File operation requires an object member to cout")
        
        if(args[2]):
            raise Exception(f"Count Text File operation does not accept additional arguments.")
        
        if(not isExpr):
            raise Exception("Count result is not attached to an object")
        
        target = args[0][0] #String
        isPlural = args[0][1] #either s or none

        count = 0

        if(target == "Line"):
            count = self.__count_lines(isPlural, args[1])

        elif(target == "Word"):
            count = self.__count_words(isPlural, args[1])

        return Number(count)
    
    def __count_lines(self, isPlural, predicate):
        count = 0
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                if(predicate):

                    if(predicate.match(L)):
                        count += 1
                        if(not isPlural):
                            break
                else:
                    count += 1
                    if(not isPlural):
                            break
                    
        return count

    def __count_words(self, isPlural, predicate):
        count = 0
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                for word in L.split():
                    
                    if(predicate):
                        if(predicate.match(word)):
                            count += 1
                            if(not isPlural):
                                break
                    else:
                        count += 1
                        if(not isPlural):
                                break
        return count


    def Print(self, args, isExpr):
        if(not exists(self.path)):
            raise Exception(f"File {self.path} does not exist and cannot be printed")
        #Arg verification
        if(args[0][0] is not None):
            raise Exception("Print Text File operation does not accept an object member")
        
        if(args[1]):
            raise Exception("Print Text File operation does not accept a predicate")
        
        if(args[2]):
            raise Exception("Print Text File operation does not accept additional arguments")
        
        with open(self.path) as f:
            lines = [line.rstrip() for line in f]
            for L in lines:
                print(L)


    def Read(self, args):
        if(not exists(self.path)):
            raise Exception("File does not exist and cannot be read")
        #Arg verification
        if(args[0][0] is None):
            raise Exception("Read Text File operation requires an object member to read values by")
        
        if(args[1]):
            raise Exception(f"Read Text File operation does not accept a predicate.")
        
        if(args[2]):
            raise Exception(f"Read Text File operation does not accept additional arguments")
        
        target = args[0][0] 
        isPlural = args[0][1]

        val = None

        if(target == "Text"):
            if(isPlural):
                raise Exception("Text as a member type represents the entire body of content and cannot be plural")
            val = self.__read_text
            
        elif(target == "Line"):
            val = self.__read_lines(isPlural)

        elif(target == "Word"):
            val = self.__read_words(isPlural)

        return val
    
    def __read_text(self):
        with open(self.path) as f:
            txt = f.read()
        return Text(txt)

    def __read_lines(self, isPlural):
        with open(self.path) as f:
            if(isPlural):
                lines = [line.rstrip() for line in f]
                return List(lines)
            else:
                line = f.readline()
                return Text(line)

    def __read_words(self, isPlural):
        words = []
        with open(self.path) as f:
             for line in f:
                 if(not isPlural):
                    return Text(line.split()[0])
                 for word in line.split():
                     words.append(word)
        return List(words)
                     
class Table(Structure):
    def __init__(self, args):
        self.Fields = []
        self.IDs = []
        self.content = []

        if(len(args) == 2):
            if(type(args[0]) == List and type(args[1]) == List):
                self.IDs = args[0].content
                self.Fields = args[1].content

                for i in self.IDs:
                    row = []
                    for j in self.Fields:
                        row.append(Text("N/A"))
                    self.content.append(row)

        elif(len(args) == 1):
            if(type(args[0]) == File):
                pass
            elif(type(args[0]) == str):
                pass
        
        else:
            raise Exception("Expected two lists(IDs and Records) or a file")
        
    def __str__(self):
        retStr = ""
        if(self.Fields):
            retStr += ','
            for i in self.Fields:
                retStr += i.content
                retStr += ','
            retStr += '\n'

        for i, row in enumerate(self.content):
            if(self.IDs):
                    retStr += self.IDs[i]
                    retStr += ','
            for field in row:
                retStr += str(field)
                retStr += ','
        
            retStr += '\n'

        return retStr

    def Iterate(self):
        for ID, row in enumerate(self.content):
            for Field, Value in enumerate(row):
                yield [Value, self.IDs[ID], self.Fields[Field].content]

    def Print(self,args, isExpr):
        print(self)

class Text(Structure):
    def __init__(self, args):
        self.content = args
    
    def setValue(self, args):
        self.content = args.content

    def __str__(self):
        return str(self.content)
    
    def Print(self, args, isExpr):
        print(str(self))

class List(Structure):
    def __init__(self, args):
        self.content = args

    def __str__(self):
        retStr = ', '.join(map(str, self.content))
        return retStr

    def Filter(self, args, isExpr):
        if(args[0][0] is not None):
            raise Exception("Filter List operation does not accept object member")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Filter List operation requires a predicate to filter by.")
        
        if(args[2]):
            raise Exception(f"Filter Text File operation does not accept additional arguments")
        
        filtered = self.__filter(args[1])

        if(isExpr):
            return List[filtered]
        else:
            self.content = filtered
        
    def __filter(self, predicate):
        newItems = []
        for item in self.content:
            if(predicate.match(item)):
                newItems.append(item)
        return newItems
    
    def Remove(self, args, isExpr):
        if(args[0][0] is not None):
            raise Exception("Remove List operation does not accept object member")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Remove List operation requires a predicate to remove items by.")
        
        if(args[2]):
            raise Exception(f"Remove List operation does not accept additional arguments")
        
        value = self.__remove(args[1])
        if(isExpr):
            return List[value]
        else:
            self.content = value

    def __remove(self, predicate):
        newItems = []
        for item in self.content:
            if(not predicate.match(item)):
                newItems.append(item)
        return newItems

    def Replace(self, args, isExpr):
        if(args[0][0] is not None):
            raise Exception("Replace List operation does not accept object member")
        
        if(not isinstance(args[1], Predicate)):
            raise Exception(f"Replace List operation requires a predicate to replace items by.")
        
        if(len(args[2]) != 1):
            raise Exception(f"Replace List operation requires 1 additional argument")
        
        value = self.__replace(args[1], args[2][0])
        if(isExpr):
            return List[value]
        else:
            self.content = value

    def __replace(self, predicate, replacement):
        newItems = []
        for item in self.content:
            if(predicate.match(item)):
                newItems.append(replacement)
            else:
                newItems.append(item)
        return newItems

    def Count(self, args, isExpr):
        if(not isExpr):
            raise Exception("Count operation can only be performed as an expression")
        
        if(args[0][0] is not None):
            raise Exception("Count operation does not accept object member")
        
        if(args[2]):
            raise Exception(f"Count operation does not accept additional arguments")
        
        pred = args[1]
        count = self.__count(pred)
        return Number(count)
        
    def __count(self, predicate):
        count = 0
        for item in self.content:
            if(predicate):
                if(predicate.match(item)):
                    count += 1
            else:
                count += 1

        return count

    def Print(self, args, isExpr):
        print(str(self))

    def Iterate(self):
        for item in self.content:
            yield [item]
    
class Number:
    def __init__(self, args):
        self.content = args

    def __str__(self):
        return str(self.content)

    def Print(self, args, isExpr):
        print(self.value)   
  
structures = {'File' : File, 'Table': Table, 'List':List, 'Text':Text,}