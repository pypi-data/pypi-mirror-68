![PyPI](https://img.shields.io/pypi/v/chibp?style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/chibp?style=for-the-badge)

# chibp

## A package for interacting with the Haveibeenpwned API

Install package:

```
pip install chibp
```

Import the package:

```
import chibp
```

Example string request:

```
chibp.get("example@chrisdunne.net", API_KEY)
```

Example list request:

```
chibp.get(["example@chrisdunne.net", "example2@chrisdunne.net"], API_KEY)
```

Example full response:

```
chibp.get_full("example@chrisdunne.net", API_KEY)
```

Example list full response:

```
chibp.get_full(["example@chrisdunne.net", "example2@chrisdunne.net"], API_KEY)
```
Example get breaches:

```
chibp.get_breaches(API_KEY)
```
Example get breached site:

```
chibp.get_breach("MyFitnessPal", API_KEY)
```
Example get pastes for email:

```
chibp.get_pastes("example@chrisdunne.net", API_KEY)
```