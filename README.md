To activate the virtual environment run:
```
poetry shell
```

To run each file in the `./src/main/data/` path through the load_data python script run:
```
cd src/main
bash load_data.sh
```

Alternatively run individual files in the `./src/main/data/` folder:
```
python3 load_data.py data/20230101.csv
```

NB: The script will log out all rows that failed validation and will specify what field(s) caused it.