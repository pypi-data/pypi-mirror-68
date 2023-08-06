# Persistables

A persistable is a python class that can be saved to a file in a portable manner, and recreated on demand. This can be useful if you wish to save the state of your code to make errors more reproducible.

The current usecase for this code is to "drop" a file that enables code to be debugged if an exception is triggered in a long running code. In future, I hope to make it a medium to communicate the state of code between machines, (e.g as a re-implementation of Matlab's .fig files)

## What is a persistable?
Making a persistable class is often as easy as

```python
import persist
class Foo(persist.Persistable):
	pass
```

The class can then be written to disk with
```python
my_foo = Foo()
persist.persist_to_file('state.per', obj=my_foo)
```

and retrieved with

```python
state, meta = persist.restore_from_file('state.per')
my_foo = state['obj']
```

The metadata contains information about the function that called persist_to_file.

## Wait, what do you mean by "often"?
Many classes will be able to be persisted just by sublassing Persistable, but some will not. A class can be persisted if it is composed of one or more of 

* Numbers (ints, floats, complex)
* strings
* Iterables (lists, dicts, etc.)
* Functions
* Nonetypes
* Numpy Arrays
* Pandas Dataframes
* Any object that implements the `to_dict` and `from_dict` methods to descibe how the class can be converted to/from a dictionary of simple data types (i.e anything that can be written to json)

If this is not true of your class, you need to implement a method `to_dict` which converts your class to a dictionary of json compatible types (numbers, strings, lists, and dictionaries). You also need to implement a `from_dict` to convert a dictionary back into a class.

Examples of classes that need to implement their own `to_dict` method are ones that maintain file pointers or network connections. These classes need a way of saving enough infomation about the connection that it can be recreated at a later date.

#### Example

```python
from foobar import ComplicatedThing

# Note: Any class that implements to_dict and from_dict can be
# persisted. It does not need to extend the Persistable class
class Foo():
	def __init__(self, a, b, c):
		self.a = a
		self.complicated_thing = ComplicatedThing(b, c)
		
	def to_dict(self):
		out = dict()
		#This key is required. It is used by persist.py to
		#recreate the object
		out['__class__'] = 'mymodule.submodule.Foo'
		out['a'] = a
		out['b'] = b
		out['c'] = c
		extra = self.complicated_thing.get_internal_variable()
		out['extra'] = extra 
		return out

	@classmethod
	def from_dict(cls, cfg):
		a =  cfg['a']
		b =  cfg['b']
		c =  cfg['c']		
		stuff = cfg['extra']
		
        obj = cls.__new__(cls)
		obj.__dict__['complicated_thing'] = ComplicatedThing(b,c)
		obj.complicated_thing.set_internal_variable(stuff)
		return obj
```		
		
	
		

## Limitations
* A class can not be completely persisted if it is composed of a class whose internal state can not be exposed. This is probably a rare occurrence because the state is usually held in the `__dict__` variable

* Pandas series and dataframes can't be properly persisted if some of their columns contain objects. For example

```python
df = pd.DataFrame()
df['date'] = pd.to_daterange("2020-01-01", "2020-12-31")
persist.to_file('state.per', obj=df)
new_df = persist.from_file('state.per')['obj']
type(new_df['date'])
>>> np.int64
```

The datatime type gets persisted as an integer representing the time in milliseconds of unixtime. This is a limitation in pandas I can't figure out how to overcome.

## More examples

```python
import persist.funcs

class Foo():
	"""Store and retrive a file with an open file handle
	
	Recreating one of these objects will fail if the original file
	is not acessible at the same path as when the original object
	was created
	"""
	def __init__(self, filename):
	    	self.file_pointer = open(fp, 'r')
    	
   	def to_dict(self):
   		#We can't save the filepointer, but we can save
   		#everything we need to restore the file_pointer
		out = dict()
		out['class'] = 'mymodule.submodule.Foo'
		out['filename'] = self.file_pointer.name
		out['seek_pos'] = self.file_pointer.tell()
        persist.validate_dict(out)
        return out
       
    def from_dict(cls, cfg):
        _class = persist.funcs.get_class_from_instance_dict(cfg)
        assert _class == cls
        
        obj = cls.__new__()
        fp = open(cfg['filename'], 'r')
        fp.seek(int(cfg['seek_pos']))
        obj.__dict__['file_pointer'] = fp
        
        return obj

```
