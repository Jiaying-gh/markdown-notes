"""MCP 邮件服务器 — 通过 SMTP 发送邮件（仅标准库）"""

import json
import sys
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

def send_email(to_addr, subject, body, cc=None):
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header("技术写作日报", "utf-8")), SMTP_CONFIG["user"]))
    msg["To"] = to_addr
    msg["Subject"] = Header(subject, "utf-8")
    if cc:
        msg["Cc"] = cc
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(MIMEText(body.replace("\n", "<br>\n"), "html", "utf-8"))

    recipients = [to_addr]
    if cc:
        recipients += cc.split(",")

    if SMTP_CONFIG["use_ssl"]:
        server = smtplib.SMTP_SSL(SMTP_CONFIG["host"], SMTP_CONFIG["port"])
    else:
        server = smtplib.SMTP(SMTP_CONFIG["host"], SMTP_CONFIG["port"])

    with server:
        server.login(SMTP_CONFIG["user"], SMTP_CONFIG["password"])
        server.sendmail(SMTP_CONFIG["user"], recipients, msg.as_string())

    return {"success": True, "to": to_addr, "subject": subject}


def handle_request(request):
    req_id = request.get("id")
    method = request.get("method", "")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "mail-server", "version": "1.0.0"},
            },
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "send_email",
                        "description": "发送邮件",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "to": {"type": "string", "description": "收件人邮箱"},
                                "subject": {"type": "string", "description": "邮件主题"},
                                "body": {"type": "string", "description": "邮件正文"},
                                "cc": {"type": "string", "description": "抄送（可选，多个用逗号分隔）"},
                            },
                            "required": ["to", "subject", "body"],
                        },
                    }
                ]
            },
        }

    if method == "tools/call":
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        if name == "send_email":
            try:
                result = send_email(
                    to_addr=arguments["to"],
                    subject=arguments["subject"],
                    body=arguments["body"],
                    cc=arguments.get("cc"),
                )
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]},
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32603, "message": str(e)},
                }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Unknown tool: {name}"},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"},
    }


def main():
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer
    for raw_line in stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            line = raw_line.decode("utf-8")
            request = json.loads(line)
            response = handle_request(request)
            if response is not None:
                stdout.write(json.dumps(response, ensure_ascii=False).encode("utf-8") + b"\n")
                stdout.flush()
        except json.JSONDecodeError:
            continue
        except Exception as e:
            stdout.write(
                json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}})
                .encode("utf-8")
                + b"\n"
            )
            stdout.flush()


if __name__ == "__main__":
    main()
