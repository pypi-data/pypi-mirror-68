# FileTransfer

## A python module that makes file transfer slightly easier

### `pip install FileTransfer`

## Syntax

`FileTransfer.send(filepath="", socket=s)`<br>
`FileTransfer.receive(destination_folder_path="", socket=s)`

## Usage

### **Sending**

```python
import socket
import FileTransfer as ft

# Setup socket for use in file transfer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect("ip.address", port)

ft.send(filepath, s) # Specify filepath as str and use client socket object
```

### **Receiving**

```python
import socket
import FileTransfer as ft

# Setup simple socket receive
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", port))
s.listen(1)
conn, addr = s.accept()

result = ft.receive("C:\\destination\\folder\\path\\", conn) # Invoke receive function
# Result is a tuple with the file contents being index 0 and filename being index 1
print("Filename: ", result[1], "File Contents: ", result[0])
```

## Protocol (TCP)

| Filename Length  | Filename | Payload Length (File Contents Length) | Payload (File Contents) |
| --- | --- | --- | --- |
| `4 Bytes` | `Filename encoded (utf8)` | `4 bytes` | `Payload bytes` |
