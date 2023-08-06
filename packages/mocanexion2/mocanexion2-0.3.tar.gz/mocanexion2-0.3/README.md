# MOCANEXION 2

This code is based on mocanexion by @rnsaway, I modified the code to allow the connection to new WMS versions.

# How to Install
```
pip install mocanexion2
```

## How this works

MocaNexion allows you to connect to a MOCA application server using your application credentials.  

Once authenticated, you can then run MOCA commands and have the results returned back to you in a Pandas dataframe.

### Example
```
from mocanexion import MocaNexion2
moca = MocaNexion2()
moca.connect("Moca service", "User", "Password", device=None, warehouse=None, locale=None)
status, res = moca.execute("publish data where test = 'Success'")
print(status)
print(res)
```
```
from mocanexion import MocaNexion2
moca = MocaNexion2()
moca.connect("http://localhost:7700/service", "hittwar", "pass", device=None, warehouse=None, locale=None)
status, res = moca.execute("publish data where test = 'Success'")
print(status)
print(res)
```

## Data Frame
```
status, res = moca.execute("list inventory")
df = pd.DataFrame(res)
df.head()
```
