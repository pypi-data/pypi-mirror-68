Monapy is a library for declarative programming.
Use expressions instead of code blocks.

# Examples

### Binding

```
>>> from monapy import Binder
>>> b = Binder() >> range >> map << (lambda i: i*10) >> list
>>> b(5)
[0, 10, 20, 30, 40]
```

### Step expressions

```
from monapy import Step

class Text_to_Lines(Step):
    def __init__(self, text=None):
        self._text = text
    def make(self, value='', **kwargs):
        text = self._text or value
        return text.split('\n')

class Line_to_Words(Step):
    def __init__(self, text=None):
        self._text = text
    def make(self, value='', **kwargs):
        text = self._text or value
        return text.split(' ') 

class Find_Char(Step):
    def __init__(self, char):
        self._char = char
    def make(self, text=''):
        chars = []
        for ch in text:
            if ch == self._char:
                chars.append(ch)
        return chars

class Text(Step):
    def __init__(self, text=''):
        self._text = text
    def make(self, val=None, **kwargs):
        ret = self._text
        self._text = ''
        return ret

p = Text_to_Lines() >> Line_to_Words() >> (Find_Char('H') | Find_Char('o') | Find_Char('e')) << Text('Hi Jon')

result = p.make('Hello world!\nFor me')

print(list(result))

```
##### Result
```
['H', 'o', 'o', 'e', 'H', 'o']
```
