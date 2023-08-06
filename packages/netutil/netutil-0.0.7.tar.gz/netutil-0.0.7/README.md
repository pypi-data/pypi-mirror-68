# netutil

Python module to check the status of ports for local and websites. 

# Install
```shell
pip install netutil
```

# Usage
```python 
import netutil
google = netutils.PortCheck("google.com", 443)
print(google.isOpen())
```

For extra help I've added in variables to find the hostname and local IP address. 
- To get hostname: netutils.host_name
- To get Local IP: netutils.host_ip