import json, pydantic
from ..models.models import FulfillmentRequest
from src.suppliers import Registry


def lambda_handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"]

    if method == "POST" and path == "/fulfill":
        return fulfill(event)

    return response(404, {"error": "Not found"})


def fulfill(event):
    try:
        body = json.loads(event.get("body") or "{}")
        request = FulfillmentRequest(**body)
        order = request.model_dump()

        supplier_id = order["supplier_id"]

        registry = Registry()
        adapter = registry.get_adapter(supplier_id)
        res = adapter.fulfill(order)

        return response(200, res)
    except json.JSONDecodeError:
        return response(400, {"error": "Invalid request body"})
    except pydantic.ValidationError as e:
        return response(400, {"error": "Validation Failed", "error_details": e.errors()})
    except (KeyError, json.JSONDecodeError) as exc:
        return response(400, {"error": str(exc)})


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }