# Network-watcher

A command-line tool to record network activity that makes you able to plot a graph of the available traffic in the database. It uses SQLite to store all the traffic.

## Getting Started :page_facing_up:

### Prerequisites 
There are a couple of libraries that you have to install before running the tool. Be sure to have all of them installed by running this:

```
pip3 install -r requirements.txt 
```

### Running the tool :heavy_check_mark:

To run the tool in the intercept mode, you just have to type the following line in your shell:

```
python MainSniffer.py
```

And eventually, if you need some help:

```
python MainSniffer.py -h
```

that gives you:

```
optional arguments:
  -h, --help            show this help message and exit
  --n_packets N_PACKETS Limit the max number of packets to log. Default is 0,
                        which means infinity.
  -g, --graph           Creates a network activity graph based on current
                        database and exit. Default is 0, which means no graph.
  -v, --verbose
```

## Built With

* Python 3.5.5

## License

This project is licensed under the MIT License
