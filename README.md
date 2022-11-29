# flask-apm
As both a Java and Python programmer I missed the convenience of a free, open-source APM.

During the last years I've been using [Glowroot](https://www.glowroot.org) to get the best error traces and find performance problems.
When I then started on a Flask based application I went looking for a comparable project and
so far I've been unable to find any.

That is why I started my own. Initially I'll be adding the features I need for my own project,
but I hope to mature it over time to support many libraries out of the box just like Glowroot.

The features I'll start with are:

- Capture logging
- Capture exception
- [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) queries
- Response and processor time

For some of these I'll be looking at how the [flask-debug-toolbar](https://flask-debugtoolbar.readthedocs.io/en/latest/) extension works.

I'll add support for different storage solutions. Initially I'll start with a sqlite backend that requires no setup.
Later I'll add support for more performant databases and also a rest-api for remote logging.

## Usage
The flask-apm will be a Flask extension like any other.

```python
from flask_apm import Apm
from flask import Flask

app = Flask(__name__)

apm = Apm()
apm.init_app(app)
```

Although it actually consists out of 2 extensions. The code above will both collect data and serve a user interface to look at the collected info.

You can either add an argument to the `init_app()` call, or use the specific Flask extension class: 
`ApmCollector` and `ApmUserInterface`.

By separating them, you can host the user interface on a non-public website.
Where [Glowroot](https://www.glowroot.org) starts it own web server on port 4000 I found it better to just give you the option.

## Licensing
I chose to license flask-apm using the MIT license to be very permissive on what you are allowed to do with it.

As a private person I cannot take the responsibilities of any kind of warranty of liability.
