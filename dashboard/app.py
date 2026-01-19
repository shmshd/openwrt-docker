import json
import subprocess

from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)

DNS_PROVIDER = "Cloudflare"
DNS_ADDRESS = "1.1.1.1"
GATEWAY_ADDRESS = "10.10.10.10"


def shell_stream(cmd_args, check_error_func=None):
    try:
        process = subprocess.Popen(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        full_output = ""
        while True:
            output_line = process.stdout.readline()
            if output_line == '' and process.poll() is not None:
                break
            if output_line:
                full_output += output_line
                yield f"data: {output_line}\n\n"

        return_code = process.wait()

        error_occurred = False
        if check_error_func:
            error_occurred = check_error_func(full_output)
        elif return_code != 0:
            error_occurred = True

        # yield f"event: complete\ndata: {{\"error\": {error_occurred}, \"final_output\": \"{full_output.replace("\n", "\\n")}\"}}\n\n"
        yield f"event: complete\ndata: {json.dumps({"error": error_occurred, "final_output": full_output})}\n\n"

    except Exception as e:
        # yield f"event: error\ndata: {{\"error\": true, \"message\": \"{str(e)}\"}}\n\n"
        yield f"event: error\ndata: {json.dumps({"error": True, "message": str(e)})}\n\n"


def has_route_error(output):
    return GATEWAY_ADDRESS not in output or "default" not in output


def has_trace_error(output):
    return GATEWAY_ADDRESS not in output and " 1 " not in output


def has_ping_error(output):
    return "0% packet loss" not in output and "3 received" not in output


def sse_response(output):
    return Response(
        output,
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        }
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/info")
def api_info():
    return jsonify({
        "dns_provider": DNS_PROVIDER,
        "dns_address": DNS_ADDRESS,
        "gateway": GATEWAY_ADDRESS,
    })


@app.route("/api/stream/route")
def route_stream():
    cmd_args = ["ip", "route", "show", "default"]
    output = shell_stream(cmd_args, has_route_error)
    return sse_response(output)


@app.route("/api/stream/trace")
def trace_stream():
    cmd_args = ["traceroute", "-m", "5", "-w", "1", DNS_ADDRESS]
    output = shell_stream(cmd_args, has_trace_error)
    return sse_response(output)


@app.route("/api/stream/ping")
def ping_stream():
    cmd_args = ["ping", "-c", "3", DNS_ADDRESS]
    output = shell_stream(cmd_args, has_ping_error)
    return sse_response(output)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
