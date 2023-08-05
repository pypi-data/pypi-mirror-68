This is the official python (websocket) repo for TrueData.
-------


**What have we covered so far ?**
* Websocket APIs
  *  Live data
  *  Historical data

**How do you use it ?**

**For beginners**

* Installing from PyPi
```shell script
python3.7 -m pip install truedata_ws
```

* Connecting 
```python
from truedata_ws.websocket.TD import TD
td_app = TD('<enter_your_login_id>', '<enter_your_password>')
```

* Running tests to ensure everything is in order 
```shell script
python3.7 -m truedata_ws run_all_tests <enter_your_login_id> <enter_your_password>
```


* Starting live data

For Single Symbols
```python
req_ids = td_app.start_live_data(['<enter_symbol>'])
# Example:
# req_id = start_live_data(['CRUDEOIL-I'])
# This returns an single element list that can be used later to reference the data
```
For Multiple symbols
<p>

```python
req_ids = td_app.start_live_data(['<symbol_1>', '<symbol_2>', '<symbol_3>', ...])
# Example:
# req_ids = td_app.start_live_data(['CRUDEOIL-I', 'BANKNIFTY-I', 'RELIANCE', 'ITC'])
# This returns a list that can be used to reference data later
```

* Getting touchline data
```python
import time
time.sleep(1)
for req_id in req_ids:
    print(td_app_ip.touchline_data[req_id])
# You MAY have to wait until for 1 sec for all of the touchline data to populate
```

* Sample code for testing market data
```python
from copy import deepcopy
live_data_objs = {}
for req_id in req_ids:    
    live_data_objs[req_id] = deepcopy(td_app_ip.live_data[req_id])

while True:
    for req_id in req_ids:
        if live_data_objs[req_id] != td_app_ip.live_data[req_id]:
            print(td_app_ip.live_data[req_id])
            live_data_objs[req_id] = deepcopy(td_app_ip.live_data[req_id])
```
<br>
<br>
You can also provide your own list of req

<br>
<br>
<br>

* Getting Historical data

Using no parameters
```python
hist_data_1 = td_app.get_historic_data('BANKNIFTY-I')
# This returns 1 minute bars from the start of the present day until current time
```
Using a given starting time
```python
from datetime import datetime
hist_data_2 = td_app.get_historic_data('BANKNIFTY-I', query_time=datetime(2020, 5, 5, 12, 30))
# Any time can be given here
```
Using a given duration (For available duration options, please read the limitations section)
```python
hist_data_3 = td_app.get_historic_data('BANKNIFTY-I', duration='3 D')
```
Using a specified bar_size (For available bar_size options, please read the limitations section)
```python
hist_data_4 = td_app.get_historic_data('BANKNIFTY-I', bar_size='30 mins')
```
Using start time INSTEAD of duration
```python
from dateutil.relativedelta import relativedelta
hist_data_5 = td_app.get_historic_data('BANKNIFTY-I', start_time=datetime.now()-relativedelta(days=3))
```
IMPORTANT NOTE:
Now that we have covered the basic parameters, you can mix and match the parameters as you please... If parameter is not specified, the defaults are as follows
```python
query_time = datetime.now()
duration = "1 D"
bar_size = "1 min"
```

Convert historical data to Pandas DataFrames with a single line
```python
import pandas as pd
df = pd.DataFrame(hist_data_1)
```

<br>
<br>

Example of mix and match
```python
hist_data_6 = td_app.get_historic_data('BANKNIFTY-I', duration='3 D', bar_size='15 mins')
```

* Limitations and caveats for historical data
<ol>
<li>If you provide both duration and start time, duration will be used and start time will be ignored...</li>
<li>If you provide neither duration nor start time, duration = "1 D" will be used</li>
<li>
    ONLY the following BAR_SIZES are available
    <ul>
    <li>tick</li>
    <li>1 min</li>
    <li>5 mins</li>
    <li>15 mins</li>    
    <li>30 mins</li>    
    </ul>
</li>
<li>
    Following symbols can be used for DURATION
    <ul>
    <li>D = Days</li>
    <li>W = Weeks</li>
    <li>M = Months</li>
    <li>Y = Years</li>
    </ul>
</li>
</ol>
<br>
<br>
<br>
<br>
<br>
<br>

<!---
**For advanced users**
* Installing from PyPi
```shell script
python -m pip install truedata==xx.xx.xx # Pick your version number from available versions on PyPi
```
* Installing from source

Download the sources

Make "truedata" the working directory using cd
```
python3 setup.py install
```

* Connecting 
```
from truedata.websocket.TD import TD
td_app = TD('<enter_your_login_id>', '<enter_your_password>, live_port=8080, historical_port=8090)  # historical_port should be None, if you do not have access to historical data...
```

* Starting live data
```
td_app.start_live_data('<enter_symbol>', req_id=2000)  # Example: td_app.start_live_data('CRUDEOIL-I')
count = 0
while count < 60:
    print(td_app.live_data[2000].__dict__)
    sleep(1)
    count = count + 1
```
-->
  
**What is the plan going forward ?**
* Ease of contract handling
* Improved error handling
