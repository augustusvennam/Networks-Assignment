#IMPORTS
import socket

#CONNECTION
HOST = "localhost"
PORT = 5000

# each test case
TEST_CASES = [
    # Temperature
    ("CONVERT TEMP C F 25", "RESULT 77.00 F"),
    ("CONVERT TEMP F C -40", "RESULT -40.00 C"),
    ("CONVERT TEMP C C 25", "RESULT 25.00 C"),  # same unit testing

    # Length
    ("CONVERT LENGTH KM MI 10", "RESULT 6.21 MI"),
    ("CONVERT LENGTH MI KM 1", "RESULT 1.61 KM"),
    ("CONVERT LENGTH KM KM 10", "RESULT 10.00 KM"),

    # Weight
    ("CONVERT WEIGHT KG LB 5", "RESULT 11.02 LB"),
    ("CONVERT WEIGHT LB KG 10", "RESULT 4.54 KG"),
    ("CONVERT WEIGHT LB LB 5", "RESULT 5.00 LB"),

    # Currency
    ("CONVERT CURRENCY USD CAD 100", "RESULT 137.00 CAD"),
    ("CONVERT CURRENCY EUR GBP 50", "RESULT 42.93 GBP"),
    ("CONVERT CURRENCY GBP EUR 20", "RESULT 23.29 EUR"),
    ("CONVERT CURRENCY CAD CAD 100", "RESULT 100.00 CAD"),

    # Case-insensitivity
    ("convert temp c f 25", "RESULT 77.00 F"),

    # Error cases
    ("CONVERT MASS KG LB 5", "ERROR Invalid category"),
    ("CONVERT TEMP K F 25", "ERROR Invalid unit"),
    ("CONVERT TEMP KM MI 5", "ERROR Invalid unit"),
    ("CONVERT WEIGHT KG LB abc", "ERROR Invalid numeric value"),
    ("CONVERT TEMP C F", "ERROR Malformed request"),
    ("CONVERT TEMP C F 25 EXTRA", "ERROR Malformed request"),
    ("CALCULATE TEMP C F 25", "ERROR Malformed request"),
]


def run_tests():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    passed = 0
    failed = 0

    for request, expected in TEST_CASES:
        client_socket.sendall((request + "\n").encode())
        actual = client_socket.recv(1024).decode().strip()

        if actual == expected:
            print(f"PASS  | {request}")
            passed += 1
        else:
            print(f"FAIL  | {request}")
            print(f"        expected: {expected}")
            print(f"        actual:   {actual}")
            failed += 1

    client_socket.close()

    print()
    print(f"Results: {passed} passed, {failed} failed, {len(TEST_CASES)} total")


if __name__ == "__main__":
    run_tests()