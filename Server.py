#IMPORTS
import socket
import threading

#CONNECTION
HOST = "0.0.0.0"
PORT = 5000

shutdown_event = threading.Event()


# Valid units for each category
CATEGORY_UNITS = {
    "TEMP": ["C", "F"],
    "LENGTH": ["KM", "MI"],
    "WEIGHT": ["KG", "LB"],
    "CURRENCY": ["USD", "CAD", "EUR", "GBP"],
}

# Fixed currency rates: how many units of each currency equal 1 USD
USD_RATE = {"USD": 1.0, "CAD": 1.37, "EUR": 0.92, "GBP": 0.79}


def convert(category, from_unit, to_unit, value):
    # Convert a value from from_unit to to_unit within one category
    if from_unit == to_unit:
        return value

    if category == "TEMP":
        if from_unit == "C":
            return value * 9 / 5 + 32       # C -> F
        else:
            return (value - 32) * 5 / 9     # F -> C

    if category == "LENGTH":
        if from_unit == "KM":
            return value / 1.60934          # KM -> MI
        else:
            return value * 1.60934          # MI -> KM

    if category == "WEIGHT":
        if from_unit == "KG":
            return value / 0.453592         # KG -> LB
        else:
            return value * 0.453592         # LB -> KG

    if category == "CURRENCY":
        value_in_usd = value / USD_RATE[from_unit]
        return value_in_usd * USD_RATE[to_unit]


def handle_request(line):
    # Parse one request line and return the response string
    parts = line.split()

    if len(parts) != 5 or parts[0].upper() != "CONVERT":
        return "ERROR Malformed request"

    category = parts[1].upper()
    from_unit = parts[2].upper()
    to_unit = parts[3].upper()
    value_text = parts[4]

    if category not in CATEGORY_UNITS:
        return "ERROR Invalid category"

    if from_unit not in CATEGORY_UNITS[category] or to_unit not in CATEGORY_UNITS[category]:
        return "ERROR Invalid unit"

    try:
        value = float(value_text)
    except ValueError:
        return "ERROR Invalid numeric value"

    result = convert(category, from_unit, to_unit, value)
    return f"RESULT {result:.2f} {to_unit}"


def handle_client(conn, addr):
    print("Client connected:", addr)
    conn.settimeout(1.0)  # wake up every second to check shutdown_event

    while not shutdown_event.is_set():
        try:
            data = conn.recv(1024)
        except socket.timeout:
            continue  # no data yet, loop back and check shutdown_event
        except ConnectionResetError:
            break

        if not data:
            break

        line = data.decode().strip()
        if line == "":
            continue

        response = handle_request(line)
        print(f"[{addr}] Request: {line}  ->  Response: {response}")
        conn.sendall((response + "\n").encode())

    print("Client disconnected:", addr)
    conn.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.settimeout(1.0)

    print(f"Server listening on {HOST}:{PORT}")
    print("Press Ctrl+C to stop the server.")

    try:
        while True:
            try:
                conn, addr = server_socket.accept()
            except socket.timeout:
                continue
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        shutdown_event.set()  # signal all client threads to stop
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()