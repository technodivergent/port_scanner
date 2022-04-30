# Port Scanner
This is a simple, multi-threaded port scanner written in Python 3

## Usage
Use `python port_scanner.py -h` to get a full list of arguments

```
usage: port_scanner.py [-h] -s START [-e END] [-t THREADS] HOST

Perform a basic port scan

positional arguments:
  HOST                  Specify the host to scan

optional arguments:
  -h, --help            show this help message and exit        
  
  -s START, --start     START
                        Specify the start of the port range 

  -e END, --end END     Specify the end of the port range   

  -t THREADS, --threads THREADS
                        Specify the number of threads to spawn
```

## Example
To run a scan against port 80:

`python port_scanner.py -s 80`

To run a scan against a range of ports from 80 up to (and including) 443:

`python port_scanner.py -s 80 -e 443`