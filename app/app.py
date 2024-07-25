from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":

    import uvicorn
    import argparse
    import logging

    from ssl import VerifyMode

    parser = argparse.ArgumentParser(description="Secure fastapi/uvicorn website")
    parser.add_argument("--host", type=str, required=True)
    parser.add_argument("--port", type=str, required=True)
    parser.add_argument("--key", type=str, required=True)
    parser.add_argument("--server_cert", type=str, required=True)
    parser.add_argument("--client_ca", type=str, required=True)
    parser.add_argument("--cert_required", type=int, required=True)

    args = parser.parse_args()
    args.cert_required = VerifyMode(args.cert_required)

    uvicorn.run(
            app,
            host=args.host,
            port=int(args.port),
            ssl_keyfile=args.key,
            ssl_certfile=args.server_cert,
            ssl_ca_certs=args.client_ca,
            ssl_cert_reqs=int(args.cert_required),
            log_level=logging.INFO,
        )
    