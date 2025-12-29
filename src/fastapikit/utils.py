from fastapi import Request


def get_client_ip(request: Request) -> str:
    if request.headers.get("X-Forwarded-For") is not None:
        client_ip = request.headers.get("X-Forwarded-For")
    else:
        client_ip = request.scope["client"][0]
    return client_ip
