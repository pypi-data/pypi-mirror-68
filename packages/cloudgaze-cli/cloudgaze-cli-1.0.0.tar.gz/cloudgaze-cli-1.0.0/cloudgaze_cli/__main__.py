import json
import zlib
import sys
import base64
from urllib import request, error


import click


def compress(raw):
    return base64.b64encode(zlib.compress(raw))


def decompress(raw):
    return zlib.decompress(base64.b64decode(raw))


@click.command()
@click.argument("template-file", type=click.Path(dir_okay=False, exists=True, resolve_path=True))
@click.argument("output-file", type=click.Path(dir_okay=False, resolve_path=True))
def cli(template_file, output_file):
    with open(template_file, "r") as fh:
        data = fh.read()
    compressed = compress(data.encode("utf-8")).decode('utf-8')
    payload = json.dumps({
        'data': compressed,
        'alg': 'z'
    }).encode("utf-8")
    req = request.Request("https://cg.deforest.io/live/convert", data=payload)
    try:
        rsp = request.urlopen(req)
    except error.HTTPError as e:
        if e.code == 429:
            print(f"conversion failed, too many requests")
        elif e.code == 400:
            error_body = json.loads(e.read().decode("utf-8"))
            error_message = error_body["error"]
            error_code = error_body["code"]
            print(f"conversion failed: {error_message} ({error_code})")
        else:
            print(f"conversion failed because of an unknown reason: ({e.code})")
        sys.exit(1)

    rsp_json = json.loads(rsp.read())
    data = decompress(rsp_json["data"])
    with open(output_file, "w") as fh:
        fh.write(data.decode("utf-8"))
    print(f"results written to '{output_file}'")
