import csv
import json
import shelve
import re
from functools import singledispatchmethod


class CJSException(Exception):
    """"""

class DataLoadException(CJSException):
    """"""

class DataDumpException(CJSException):
    """"""


class CJS:
    def __init__(self):
        self.filename = ''
        self.ext = ''
        self.data = None
        self.size = 0
        self.position = 0

    def __str__(self):
        attrs = f'filname={self.filename}, ext={self.ext}, data={type(data)}, size={self.size}'
        return f'{self.__class__.__name__}({attrs})'

    def __iter__(self):
        return self

    def __next__(self):
        if not self.size or self.position >= self.size:
            self.position = 0
            raise StopIteration

        if isinstance(self.data, dict):
            item = list(self.data.items())[self.position]
        else:
            item = self.data[self.position]
        self.position += 1
        return item

    def _parse_filename(self, filename):
        if filename:
            regex = re.match('^(.+)(\.db|\.csv|\.txt|\.json)$', filename)
            try:
                self.filename, self.ext = regex.groups()
            except AttributeError:
                raise CJSException(f'Invalid file name: {filename}.')
        elif not self.filename:
            raise CJSException('File name is not specified.')

    def load(self, filename=None):
        self._parse_filename(filename)

        if self.ext == '.db':  
            with shelve.open(self.filename) as file:
                self.data = {key:val for key, val in file.items()}
        else:
            with open(self.filename+self.ext, encoding='utf-8') as file:
                if self.ext == '.csv':
                    self.data = list(csv.reader(file, delimiter=','))
                elif self.ext == '.json':
                    self.data = json.load(file)
                elif self.ext == '.txt':
                    self.data = [line.strip('\n').split(',') for line in file.readlines()]
                else:
                    msg = f'Unable to load {self.filename+self.ext}.'
                    raise DataLoadException(msg)

        self.size = len(self.data)
        return self.data

    @singledispatchmethod
    def dump(self, data, filename):
        raise NotImplementedError

    @dump.register(list)
    @dump.register(tuple)
    @dump.register(set)
    def _(self, data=[], filename=None):
        self._parse_filename(filename)
        self.data = data
        self.size = len(self.data)

        with open(self.filename+self.ext, 'w', encoding='utf-8') as file:
            if self.ext == '.csv':
                writer = csv.writer(file)
                writer.writerows(self.data)
            elif self.ext == '.txt':
                lines = [','.join(i) + '\n' for i in self.data]
                file.writelines(lines)
            else:
                msg = f'Unsupported dump: {type(self.data)} -> {self.filename+self.ext}'
                raise DataDumpException(msg)
        return None

    @dump.register(dict)
    def _(self, data={}, filename=None):
        self._parse_filename(filename)
        self.data = data
        self.size = len(self.data)

        if self.ext == '.json':
            with open(self.filename+self.ext, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=True, indent=4)
        elif self.ext == '.db':
            with shelve.open(self.filename, writeback=True) as file:
                file.update(self.data)
        else:
            msg = f'Unsupported dump: {type(self.data)} -> {self.filename+self.ext}'
            raise DataDumpException(msg)
        return None


if __name__ == '__main__':
    mydict = {
        'cat': 'meow',
        'dog': 'woof',
        'pig': 'oink',
        'cow': 'moo',
        'human': 'hello world',
    }

    cjs = CJS()
    
    cjs.dump(mydict, 'mydict.json')  # save dict to json
    data = cjs.load('mydict.json')   # load the json data
    print(data)

    data['human'] = 'i like wendie'  # modify the data
    cjs.dump(data, 'mydata.db')  # save the new data to shelve
    new_data = cjs.load('mydata.db')  # load the shelve data
    print(new_data)

    items = list(new_data.items())  # dictionary to key, val pairs
    cjs.dump(items, 'items.csv')  # save the items to csv
    data = cjs.load('items.csv')  # load the csv data
    print(data)

    data.append(['devil', 'named trump'])  # add a new row of key, val pair
    cjs.dump(data, 'newitems.txt')  # save the new items
    new_items = cjs.load('newitems.txt')  # load the txt data
    print(new_items)

    mydict = {key: val for (key, val) in new_items}  # convert key, val pairs back to dictionary
    cjs.dump(mydict, 'new_dict.db')  # save the new dictionary
    data = cjs.load('new_dict.db')  # load the shelve data
    print(data)

    data['human'] = 'does wendie like me?'  # modify the data
    cjs.dump(data, 'new_dict.json')  # save the new data to json
    new_dict = cjs.load('new_dict.json')  # load the json data
    print(new_dict)

    for i in cjs:
        print(i)
