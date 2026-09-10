from flask import Flask, render_template, request
import socket
import os

app = Flask(__name__)


def scan_ports(target):
    open_ports = []

    ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389]

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)

            result = sock.connect_ex((target, port))

            if result == 0:
                open_ports.append(port)

            sock.close()

        except Exception:
            pass

    return open_ports


@app.route("/", methods=["GET", "POST"])
def home():
    open_ports = []
    target = ""

    if request.method == "POST":
        target = request.form.get("target", "").strip()

        if target:
            try:
                socket.gethostbyname(target)
                open_ports = scan_ports(target)
            except socket.gaierror:
                open_ports = []

    return render_template(
        "index.html",
        target=target,
        open_ports=open_ports
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)