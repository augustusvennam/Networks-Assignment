# CP372 – Multi-Service Converter Server

**by:** Harjeet Singh (169092409)  |  Augustus (169105552)

### Programming Language
Python 3 (standard library only: `socket`, `threading`).
Tested on Python 3.10+.

### Files
- `Server.py` - the TCP server
- `Client.py` - the interactive TCP client
- `Tests.py` - test script and error case verification against server



## How to Compile
Python is an interpreted language, so there is no compilation step.
Just make sure Python 3 is installed:
 
```bash
python3 --version
```



## How to Run the Server
```bash
python3 Server.py
```
 
This starts the server on `0.0.0.0:5000`. The host and port are set as constants (`HOST`, `PORT`) at the top of `Server.py`. edit them directly in the file if you need different values.

The server runs until you stop it with `Ctrl+C`. **Note:** Ctrl+C is
noticed immediately, even if clients are still connected. Each
connected client gets a brief window (up to about 1.2 seconds) to
notice the shutdown and disconnect cleanly; after that the process
exits regardless.



## How to Run the Client 
In a separate terminal, with the server already running:
 
```bash
python3 Client.py
```
It connects to `localhost:5000` by default (also a constant at the top
of `Client.py`). You can run multiple clients in separate terminals at
the same time. The server handles each one in its own thread.



## How to Run the Automated Tests
With the server running, in another terminal:
 
```bash
python3 Tests.py
```
This sends 21 predefined requests covering every category
 


## Supported Commands
 
All requests use the format:
```
CONVERT <CATEGORY> <FROM_UNIT> <TO_UNIT> <VALUE>
```
 
| Category | Units              | Example                          |
|----------|--------------------|----------------------------------|
| TEMP     | C, F               | `CONVERT TEMP C F 25`            |
| LENGTH   | KM, MI             | `CONVERT LENGTH KM MI 10`        |
| WEIGHT   | KG, LB             | `CONVERT WEIGHT KG LB 5`         |
| CURRENCY | USD, CAD, EUR, GBP | `CONVERT CURRENCY USD CAD 100`   |
 
Category and unit names are case-insensitive (`temp`, `Temp`, and `TEMP`
all work).
 
 Type `EXIT` or `QUIT` in the client to close the connection.
 


### Sample Session
 
```
Enter request: CONVERT TEMP C F 25
Server response: RESULT 77.00 F
 
Enter request: CONVERT CURRENCY USD CAD 100
Server response: RESULT 137.00 CAD
 
Enter request: CONVERT FOO C F 25
Server response: ERROR Invalid category
 
Enter request: EXIT
Connection closed.
```
 
### Error Responses
 
| Condition                               | Response                      |
|-----------------------------------------|-------------------------------|
| Unknown category                        | `ERROR Invalid category`      |
| Unit not valid for the given category   | `ERROR Invalid unit`          |
| Value is not a valid number             | `ERROR Invalid numeric value` |
| Wrong number of fields / bad keyword    | `ERROR Malformed request`     |
 



## Server Logging
Every connection and every request/response is printed to the server's
console.
```
Client connected: ('127.0.0.1', 55842)
[('127.0.0.1', 55842)] Request: CONVERT TEMP C F 25  ->  Response: RESULT 77.00 F
Client disconnected: ('127.0.0.1', 55842)
```
 


## Known Limitations
 
- **Host/port are hardcoded constants**, not command-line flags.

- **Currency rates are hardcoded**, not pulled from a live
  exchange-rate API. They are there from example only.

- **Single-line requests only**, and each request is assumed to arrive
  in one `recv()` call. This works correctly for our client (it sends
  one line and waits for the reply before sending the next), but a
  more defensive server would buffer partial/split TCP data instead of
  assuming this.

- **Connections are dropped abruptly on server shutdown.** Client
  handler threads run as daemon threads so the server can exit
  immediately on Ctrl+C even with clients still connected; this means
  no graceful "server is shutting down" message is sent to connected
  clients first.

- **No authentication or encryption.** This is a plain-text TCP
  protocol intended for local/educational use, not production
  deployment.