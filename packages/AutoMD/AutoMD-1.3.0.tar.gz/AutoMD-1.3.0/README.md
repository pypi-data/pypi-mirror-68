# AutoMD
AutoMD is a documentation library for Flask APIs build with FlaskRESTful and Webargs.
Endpoint parameters and basic responses are automatically parsed into the OpenAPI specification,
using Type Hints and introspection, and a endpoints registered to serve the specification.

## Motivation
Documentation libraries tend to rely heavily on elaborate docstrings and static generation from source code.
This library requires minimal changes to existing code, and most information (especially parameter specs)
doesn't rely on keeping docstrings up to date.

## Installation
AutoMD is available through PyPi.  AutoMD requires Python >= 3.6 (f-strings are too convenient to ignore)
Install using pip:
```
pip install automd
```

AutoMD also install the following dependencies:
- flask
- flask-restful
- webargs
- apispec
- pyyaml
- marshmallow
- werkzeug

## Usage
### AutoMD registration/initialization
The first step is to initialize the AutoMD app from a FlaskRESTful Api.

```python
from flask import Flask
from flask_restful import Api
from automd.registration import AutoMDApp


app: Flask = Flask(__name__)
api: Api = Api(app)

spec: AutoMDApp = AutoMDApp(api, title="AutoMD Test App", app_version="1.0.0", openapi_version="3.0.0")
``` 

After that, all that is *required* is adding the `@automd` decorator to an existing Resource endpoint.

```python
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_kwargs
from automd.decorators import automd


class MinimalStatus(Resource):
    get_query_arguments = {
        "text": fields.String(required=False)
    }

    @automd()
    @use_kwargs(get_query_arguments)
    def get(self, text):
        return text
```
which will mark the endpoint for inclusion in the OpenAPI spec.  In this example, the spec information
will be pretty limited, but will still have the API url, argument, and a default value.

With more complete python annotations, more information can be gleaned:
```python
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_kwargs
from automd.decorators import automd


class IntrospectionStatus(Resource):
    post_query_arguments = {
        "text": fields.String(required=False)
    }

    @automd()
    @use_kwargs(post_query_arguments, location="json")
    def post(self, text: str = "Hello AutoMD") -> str:
        ret_text: str = "status check OK"

        if text is not None:
            ret_text = f"{ret_text}: {text}"

        return ret_text
```
From this the APISpec also get the parameter type, default value, and API response type.  It does not get the parameter
location yet though, that takes more aguements to automd.

Filling in more information in the webargs fields, automd decorator, use_kwargs decorator, and using one of the
AutoMD response classes for type annotation and  gives even better information:
```python
from flask_restful import Resource
from marshmallow import fields
from webargs.flaskparser import use_kwargs
from automd.decorators import automd
from automd.responses import ValueResponse

class Status(Resource):
    get_query_arguments = {
        "text": fields.String(required=False, description='Text to return', doc_default="Hello AutoMD")
    }

    @automd(parameter_schema=get_query_arguments,
             summary="Status Endpoint",
             description="Status Endpoint, responds with a message made from the input string")
    @use_kwargs(get_query_arguments, location="query")
    def get(self, text: str = None) -> ValueResponse:
        log_text: str = "status check OK"

        log_text = f"{log_text}: {text or 'Hello AutoMD'}"

        return ValueResponse(log_text)
```

With this information, argument types, return types, summaries, descriptions, detailed default
information, and parameter location info (body, query, etc) is included.  Summary and description
are the only "magic strings" needed, and those will generally not change much or be onerous to
keep up to date compared to the automatically grabbed information.

An example Flask API app is provided to showcase some functionality.  Start it using `run.py`.
A sample of the OpenAPI spec generated is [here](https://cliftbar.github.io/automd/documentation/sample_spec.html).
