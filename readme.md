# Lazy(?) REST APIs

This is a series of examples that build on the previous ones showing my thought process. It abuses `__call__` and `__getattr__` call REST api endpoints without having to write a million `endpoint_url = '/endpoint'` and functions for each type of request, because I'm lazy and was sick of doing it.  Is it easier? Probably not. Did it require less work than normal implementations? Also probably not. Does it make the code more readable and portable though? Absolutely not.

Each step is in the `/src` folder under `/src/example1_<details>.py`. `/src/apisession.py` contains an abstract example.

This is largely done using the Virus Total v3 api as the example as its convenient and fits with working in cybersecurity.
