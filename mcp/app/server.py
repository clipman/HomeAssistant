import sys
import json
import uuid
import requests
import os

options_path = "/data/options.json"

if os.path.exists(options_path):
    with open(options_path) as f:
        options = json.load(f)
        WEBHOOK_URL = options.get("webhook_url")
else:
    WEBHOOK_URL = None


def send(msg):
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def read():
    line = sys.stdin.readline()
    if not line:
        sys.exit(0)
    return json.loads(line)


# 1️⃣ initialize
def handle_initialize(msg):
    send({
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "protocolVersion": "2025-03-26",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "kakao-mcp",
                "version": "0.1.0"
            }
        }
    })


# 2️⃣ tools/list
def handle_tools_list(msg):
    send({
        "jsonrpc": "2.0",
        "id": msg["id"],
        "result": {
            "tools": [
                {
                    "name": "send_kakao_message",
                    "description": "Send a KakaoTalk message via n8n webhook",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Message text"
                            }
                        },
                        "required": ["text"]
                    }
                }
            ]
        }
    })


# 3️⃣ tools/call
def handle_tools_call(msg):
    params = msg.get("params", {})
    name = params.get("name")
    args = params.get("arguments", {})

    if name == "send_kakao_message":
        text = args.get("text")

        r = requests.post(
            WEBHOOK_URL,
            json={"text": text},
            timeout=10
        )

        send({
            "jsonrpc": "2.0",
            "id": msg["id"],
            "result": {
                "status": "ok",
                "response": r.text
            }
        })
        return

    send({
        "jsonrpc": "2.0",
        "id": msg["id"],
        "error": {
            "code": -32601,
            "message": "Unknown tool"
        }
    })


# 🔁 Main loop
while True:
    msg = read()
    method = msg.get("method")

    if method == "initialize":
        handle_initialize(msg)
    elif method == "tools/list":
        handle_tools_list(msg)
    elif method == "tools/call":
        handle_tools_call(msg)
    else:
        send({
            "jsonrpc": "2.0",
            "id": msg.get("id"),
            "error": {
                "code": -32601,
                "message": f"Method {method} not supported"
            }
        })
