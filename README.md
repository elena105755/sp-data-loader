To run each file in the `./data/` path through the load_data python script run:
```
bash load_data.sh
```

Alternatively run individual files in the `./data/` folder:
```
python3 load_data.py data/20230101.csv
```

NB: The script will log out all rows that failed validation and will specify what field caused it.