## Control sphero sprk+

### Setup

Requires

```
pip install sphero_sprk
```

which only works on linux. Repo: https://github.com/CMU-ARM/sphero_sprk

Get sphero bluetooth address with

```
sudo hcitool lescan
```

### Control sphero over LAN

Only use this on trusted LAN!

```
./sphero-client.py hostname
```
