from functools import wraps
from http import HTTPStatus
from http.client import responses

from dos import prop
from flask import request, jsonify


def wrap_handler(name, func):

    def wrapper(*a, **kw):
        return func(*a, **kw)

    wrapper.__name__ = name
    return wrapper


def wrap_route(app, func, rule, http_methods, *a, **kw):

    kw = kw.copy()

    if isinstance(http_methods, str):
        kw.setdefault("methods", [http_methods.upper()])
    elif isinstance(http_methods, list):
        kw.setdefault("methods", [method.upper() for method in http_methods])
    else:
        raise Exception("Not a valid representation of supported http methods.")

    @wraps(func)
    def wrapper(*args, **kwargs):

        func_response = func(*args, **kwargs)

        if isinstance(func_response, dict):
            ret = func_response
            status = ret.get("status", HTTPStatus.OK)
        if isinstance(func_response, tuple):
            ret = func_response[1]

            affiliated_response = responses.get(func_response[0])

            if affiliated_response is None:
                raise Exception(f"{func_response[0]} is not a valid http code!!")

            status = func_response[0]
        else:
            raise Exception("Must be a dict or a tuple!")

        resp = jsonify(ret)
        return resp, status

    kw.setdefault("endpoint", rule)

    wrapped = app.route(rule, *a, **kw)(wrapper)
    wrapped.provide_automatic_options = False

    return wrapper


def wrap_validation(handler, module):

    def validation_wrapper(*a, **kw):
        if hasattr(module, "input_schema"):
            http_status, reject_dict = validate_input(request, module.input_schema())
            if http_status is not HTTPStatus.OK:
                return http_status, reject_dict

        if hasattr(module, "output_schema"):
            return create_output(handler(*a, **kw), module.output_schema())

        return handler(*a, **kw)

    validation_wrapper.__name__ = "handler"
    return validation_wrapper


def validate_input(given_request, input_schema):  # pylint: disable=too-many-statements
    message = []
    field_error_messages = {}
    http_status = HTTPStatus.OK

    body = given_request
    if not isinstance(body, dict):
        try:
            body = given_request.get_json()
        except Exception:  # pylint: disable=broad-except
            message.append("Improperly formatted request body. Must provide valid JSON, even if it's just {}!")
            http_status = HTTPStatus.PRECONDITION_FAILED

    if http_status is HTTPStatus.OK:

        expected_fields = []
        required_fields = []

        for field_name, field_prop in input_schema.items():
            expected_fields.append(field_name)
            if field_prop.required:
                required_fields.append(field_name)

        unexpected_fields = []

        for key in body.copy():
            if key not in expected_fields:
                unexpected_fields.append(key)

        if len(unexpected_fields) > 0:
            if len(unexpected_fields) == 1:
                message.append(f"An unexpected field was sent to the server: {unexpected_fields[0]}")
                http_status = HTTPStatus.BAD_REQUEST
            else:
                message.append(f"Unexpected fields were sent to the server: {str(unexpected_fields)}")
                http_status = HTTPStatus.BAD_REQUEST

        missing_required_fields = []

        for field in required_fields:
            if field not in body.keys():
                missing_required_fields.append(field)

        if len(missing_required_fields) > 0:
            if len(missing_required_fields) == 1:
                message.append(f"A required field is missing: {missing_required_fields[0]}")
                http_status = HTTPStatus.BAD_REQUEST
            else:
                message.append(f"Required fields are missing: {missing_required_fields}")
                http_status = HTTPStatus.BAD_REQUEST

    if http_status is HTTPStatus.OK:

        for field_name, field_prop in input_schema.items():
            try:
                field_prop.parse_input_and_validate(field_name, body)
            except prop.ValidationError as validation_error:
                if validation_error is not None:
                    field_error_messages[field_name] = str(validation_error.message)
                    http_status = HTTPStatus.BAD_REQUEST

    reject_dict = {}

    if len(message) > 0:
        reject_dict["message"] = ' /// '.join(message)

    if field_error_messages:
        if "message" not in reject_dict:
            if len(field_error_messages) == 1:
                reject_dict["message"] = "A field has an error."
            else:
                reject_dict["message"] = "Multiple fields have an error."

        reject_dict["field_error_messages"] = field_error_messages

    return http_status, reject_dict


def create_output(endpoint_result, output_schema):

    http_status_code = endpoint_result[0]
    result_body = endpoint_result[1]

    output_dict_object = output_schema.get(http_status_code)
    if output_dict_object is None:
        raise prop.ValidationError(f"Endpoint does not define http status code {http_status_code} in the output schema!")

    returned_dict = {}

    for field_name, field_prop in output_dict_object.items():
        value = field_prop.format_output_and_validate(field_name, result_body)

        if value is None and field_prop.required is False:
            continue

        returned_dict[field_name] = value

    return http_status_code, returned_dict
