class Slimjson:
    def __init__(self):
        self.arrayDelimiters = [',', ']'];
        self.dictDelimiters = [',', '}'];
        self.dictKeyDelimiters = [':'];
        self.whitespace = ['\t', '\r', '\n', ' ', '\u2002']

        self.i = 0 

    def parse(self, sjson):
        return self.parse_object(sjson, None)

    def parse_object(self, first, second):
        if not isinstance(first, str):
            return first
        if second is None:
            self.i = 0
            return self.parse_object_list(first)
        if isinstance(second, str):
            return self.parse_object_key(first, second)
        
        return self.parse_object_list(first,second)
    

    def parse_object_key(self, sjson, key):
        self.i = 0 
        parsed = self.parse_object_dictionary(sjson)
        if parsed is not None and key in parsed:
            return parsed[key]
        return None 

    def parse_object_list(self, sjson, delimiters=None):
        self.i = self.skip_formatting(sjson, self.i);
        if sjson[self.i] == "{" :
            return self.parse_object_dictionary(sjson);
        
        if sjson[self.i] == "[":
            return self.parse_object_array(sjson);
        
        text = self.parse_object_string(sjson, delimiters);
        text2 = text.strip() if text is not None else None
        if (text2 is None):
            raise ValueError(f"Expected value at index {self.i}")
        
        if len(text2) == 0:
            return "";
        
        try:
            return float(text)
        except ValueError:
            pass
        
        if (text2.lower() == "true"):
            return True;
        if (text2.lower() == "false"):
            return False;
        
        if text2.startswith('"') and text2.endswith('"'):
            text = text2[1:-1]

        if text2 == "null":
            text = None
        return text;

    def parse_object_string(self, sjson, delimiters):
        if sjson[self.i] == '"':
            num = sjson.find('"', self.i+1)
            length = num - self.i - 1
            result = sjson[self.i+1:self.i+1+length]
            self.i = num + 1
            return result
        flag = False
        string = ""
        while self.i < len(sjson):
            c = sjson[self.i]
            # if (!flag && c == '\\') {
            # flag = true;
            # i++;
            # continue;
            # }
            if not flag and ((delimiters is not None and c in delimiters) or c == '\n'):
                break
            string += c
            flag = False
            self.i += 1
        return string

    def parse_object_array(self, sjson):
        self.i += 1
        items = []
        c = None
        while True:
            self.i = self.skip_formatting(sjson, self.i)
            if self.i >= len(sjson):
                raise ValueError(f"Expected ']' at {self.i}")
            if sjson[self.i] == ']':
                self.i += 1
                break
            item = self.parse_object(sjson, self.arrayDelimiters)
            if self.i >= len(sjson):
                raise ValueError(f"Expected ']' at {self.i}")
            self.i = self.skip_formatting(sjson, self.i)
            c = sjson[self.i]
            if c != ']' and c != ',':
                raise ValueError(f"Expected ']' at {self.i}")

            items.append(item)
            self.i += 1

            if c == ']':
                break
        return items
        

    def parse_object_dictionary(self, sjson):
        self.i += 1
        dictionary = {}
        c = None
        while True:
            self.i = self.skip_formatting(sjson, self.i)
            if self.i >= len(sjson):
                raise ValueError(f"Expected '}}' at {self.i}")
            if sjson[self.i] == '}':
                self.i += 1
                break

            text = self.parse_object_string(sjson, self.dictKeyDelimiters)
            if text is None or len(text) == 0:
                raise ValueError(f"Expected key at {self.i}")
            if self.i > len(sjson):
                raise ValueError(f"Expected ':' at {self.i}")
            c = sjson[self.i]
            if c != ':':
                raise ValueError(f"Expected ':' at {self.i}")
            self.i += 1
            value = self.parse_object(sjson, self.dictDelimiters)
            dictionary[text] = value 
            self.i = self.skip_formatting(sjson, self.i)
            if self.i > len(sjson):
                raise ValueError(f"Expected '}}' at {self.i}")           
            c = sjson[self.i]
            if c != '}' and c != ',':
                raise ValueError(f"Expected '}}' at {self.i}")
            self.i += 1

            if c == '}':
                break
        return dictionary
        


    def skip_formatting(self, string, index):
        while index < len(string) and string[index] in self.whitespace:
            index += 1
        return index