# Nopea
(Version 0.0.5)

---
## Purpose
Provides an ORM for MySQL, PostgreSQL and SQLite.

## Usage

To use the power of Nopea you need to set up an adaptor and let your classed inherit from nopea.DbObject.

### Setting up Adaptor and Connection
```python
from nopea.dbobject import DbObject
from nopea.adaptors.sqlite import SQLiteAdaptor

DbObject = DbObject
DbObject.adaptor = SQLiteAdaptor('nopea.db')
```

### Creating a subclass
```python
class User(DbObject):
    name = nopea.CharField(max_length=25)
    password = nopea.CharField(max_length=50)
    describtion = nopea.TextField()
    registered = nopea.DateField()
    logins = nopea.IntegerField()
    active = nopea.BooleanField(default=True)
```

> Users automatically get an additional id field which is an instance of `nopea.fields.PkField`.

### Instance methods:
```python
instance.save()
# Simply saves the object. If it is new, it will be created, if it already exists, it will be updated. Depending on whether the instance has an id != None or not.

instance.delete()
# The instance will be delete from the removed from the database. The instance will not be deleted and keep it's original id.

```

### Class methods
```python
User.create_table()
# Function to create tables.
# The class which calls this function will get a table in the database.
```

### Manager operations:
The class provides an interface to create objects: The objects manager.
```python
User.objects.all()
# Returns all objects, unordered

User.objects.get(key=value)
# E.g.: User.objects.get(id=2) Returns one object

User.objects.filter(key=value)
# E.g.: User.objects.filter(active=True) Returns a list of
# objects (like `get` but returns more than one).

# key__lt, key__lte, key__gte and key__gt can be used to limit
# the results. lte means 'lower than equal',
# lt means 'lower than', gte means 'greater than equal' and
# gt means 'greater than'

# E.g. "logins__lt=10". This will return all users with less
# than 10 logins.

# The filters can be combined:

User.objects.filter(logins__gte=10, logins__lte=50)

User.objects.exclude(key=value)
# Returns all results where the the value of the row does not match.

User.objects.create()
# Used to create objects of the calling class.
# Takes fieldnames as kwargs. E.g.

User.objects.create(name='Christian')
# returns the just created object.

User.objects.order_by('name')
# Returns a list of matching object. Can be used with a leading - to
# reverse the order.

User.objects.count()
# Returns the number of mathing rows.
```

### DbObject class methods

```python
DbObject.raw(query, args)
# The builtin SQL injection function.
# It simply executes queries and can be used with arguments.
# It always returns what it fetches. Use it wisely.

DbObject.raw(
    "INSERT INTO user (name, description)
     VALUES (?, ?)", 'Christian', 'Nopea developer.'
    )
```

# License
Nopea is available under the terms of the GPLv3.


# Disclaimer
This software comes without any warranty. You use it on your own risk. It may contain bugs, viruses or harm your software and hardware in another way. The developer is not responsible for any consequences which may occur caused by using the software.
