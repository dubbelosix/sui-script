# sui-script
sui script for some epoch metrics.
feel free to fork, modify

## deps
```
pip install virtualenv
virtualenv -p python3 .venv
. .venv/bin/activate
```
## python deps
```
(.venv) dubbelosix@warsong sui-script % pip install -r requirements.txt
## run

```
(.venv) dubbelosix@warsong sui-script % ADDR=0xaa10cfd6e38c4cf3ea1f7a99bd7c75b0a3d3f4c8 python main.py 
pending validator self stake: 2290624339 MIST
pending validator delegated stake: 95900705784 MIST
pending validator total stake: 98191330123 MIST
----
pending everyone self stake: 120157871571 MIST
pending everyone delegated stake: 8552450885004 MIST
pending everyone total stake: 8672608756575 MIST
----
next epoch share: 1.13%
current gas price: 120
----
current epoch progress = 58.58%
num txns so far: 761584
projected txn count: 1300098.4725965858
current compute units per txn (excl storage) : 863.4056
storage total: 392449941 MIST
storage rebate: 377967426 MIST
```

