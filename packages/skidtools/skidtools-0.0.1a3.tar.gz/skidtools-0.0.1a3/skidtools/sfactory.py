# Skidtools, A collection of utilities and tools to rapidly develop CLI programs. 
# It aims to get rid of boilerplate and aid skiddies.
# Copyright (C) 2020 Abdos

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

"""Collection of generators used for generation credentials and other data

Typical usage example:
```python
from skidtools import sfactory
credentials = sfactory.generate_credentials("number", "bot")
login(credentials['username']) # made up example function
```

"""

from typing import Dict, List, Union, Optional
from faker import Faker # type: ignore

# Faker instance used for fake data
fake = Faker()


def generate_credentials(engine: str = "name", prefix: Optional[str] = None) -> Dict[str, str]:
    """Generates a pair of random credentials (firstname, lastname, username, email, password).

    Args:
        engine: This defines the pattern used to generate the credentials, number generates using only numbers, leter genrates using only letters,
                name generates a random realistic name using the Faker module, mix is a combination of numbers and letters. This doesn't effect password
                genration or email. The email is in the username@skid.dev format.
        prefix: Optional argument which prefixes the given string to the the generated username and email

    Returns:
        A dict with with they keys: firstname, lastname, username, email, password
    """
    credentials: Dict[str, str] = {}

    if engine == "name":
        # Real names and data with Faker
        credentials['firstname'] = fake.first_name()
        credentials['lastname'] = fake.first_name()
        credentials['username'] = fake.user_name()
        credentials['email'] = fake.free_email()

    elif engine == "number":
        # Combination of random integers
        credentials['firstname'] = str(fake.random_number(digits=10, fix_len=True)) #turn into string
        credentials['lastname'] = str(fake.random_number(digits=10, fix_len=True)) 
        credentials['username'] = str(fake.random_number(digits=10, fix_len=True))
        credentials['email'] = credentials['username'] + "@skid.dev"

    elif engine == "letter":
        # Combination of random letters
        credentials['firstname'] = ''.join(fake.random_letters(length=10)) # turn into string
        credentials['lastname'] = ''.join(fake.random_letters(length=10))
        credentials['username'] = ''.join(fake.random_letters(length=10))
        credentials['email'] = credentials['username'] + "@skid.dev"

    elif engine == "mix":
        # A combination of numbers and letters
        credentials['firstname'] = fake.password(length=10, special_chars=False) # fake.password returns a combination of random numbers and letters
        credentials['lastname'] = fake.password(length=12, special_chars=False)
        credentials['username'] = fake.password(length=12, special_chars=False)
        credentials['email'] = credentials['username'] + "@skid.dev"
         
    else:
        raise ValueError("Invalid argument: engine")
    
    credentials['password'] = fake.password(length=12, special_chars=False)
    # Add prefix to username and email
    if prefix != None:
        credentials['username'] = prefix + credentials['username']
        credentials['email'] = prefix + credentials['email']

    return credentials