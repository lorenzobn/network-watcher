from scapy.all import *
from NetworkPlot import plotGraph
from Database import Handler
import socket
import sys
import logging
import argparse

#globals
search_filter = ""
is_verbose = False
pck_cnt = 0

#configurations
LOG_PATH = "./report.log"
DEFAULT_DATABASE_PATH = "./database.sqlite"
db_handler = None


def exit_f():
    print('Closing caputure with {} packets captured'.format(pck_cnt))
    logging.info("Closing caputure with {} packets captured".format(pck_cnt))
    sys.exit(0)


def is_validIP(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False


def pck_callback(packet):
    try:
        global pck_cnt
        global is_verbose
        global db_handler
        pck_cnt += 1
        if packet.haslayer(DNS):
            if packet.ancount > 0 and packet.qd.qtype == 1:
                for x in range(packet.ancount):
                    if not is_validIP(packet.an[x].rdata): continue
                    db_handler.setIPAddress(packet.an[x].rdata,packet.qd.qname.decode("utf-8")[:-1])
                    if is_verbose:
                        print("[+] DNS ANS: {} is at {}".format(packet.qd.qname[:-1], packet.an[x].rdata))
                    
            if DNSQR in packet:
                query_name = packet[DNSQR].qname.decode("utf-8")[:-1]
                if db_handler.checkDomain(query_name): 
                    db_handler.updateCount(query_name)
                else:
                    db_handler.insertNew(query_name)

                if is_verbose: 
                    print("[+] DNS QR: {}".format(packet[DNSQR].qname))

            if is_verbose:
                db_handler.printTable()
            
            
        if packet.haslayer(TCP):
            if packet is not None:
                p = packet[0][1]
                from_ip = p.src
                to_ip = p.dst
                #if this TCP packet is incomining traffic
                check_in = db_handler.checkIP(from_ip)
                check_out = db_handler.checkIP(to_ip)
                
                if check_in is not None:
                    #inbound traffic
                    db_handler.updateTraffic(check_in[0],"in",len(packet))
                if check_out is not None:
                    #outbound traffic
                    db_handler.updateTraffic(check_out[0],"out",len(packet))

    
    except Exception as e:
        print("Error occurred. See "+LOG_PATH)
        logging.error("Sniffing activity stopped due to error:  ",str(e))
        sys.exit(1)

def main(count):
    logging.info("Sniffing started with filter: ",search_filter)
    try:
        print("Press Ctrl-C to stop the sniffing activity")
        sniff(filter=search_filter, prn=pck_callback, store=0, count=count)
    except KeyboardInterrupt:
        exit_f()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network traffic logging that store the ingoing/outgoing traffic from all interfaces in SQLite database.')
    parser.add_argument('--n_packets', default=0, help='Limit the max number of packets to log. Default is 0, which means infinity.', type=int, dest='n_packets')
    parser.add_argument('-g', '--graph', default=0, action='count', help='Creates a network activity graph based on current database and exit. Default is 0, which means no graph.', dest='create_graph')
    parser.add_argument('-v', '--verbose', default=0, action='count', dest='verbose')

    args = parser.parse_args()
    if(args.create_graph != 0):
        plotGraph(DEFAULT_DATABASE_PATH)
        sys.exit(0)

    logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    try:
        db_handler = Handler(DEFAULT_DATABASE_PATH)
    except Exception as e:
        print("Error occurred. See "+LOG_PATH)
        logging.error("Database init failed. Error report: ",str(e))
        sys.exit(1)

    if(args.verbose != 0): 
        is_verbose = True


    main(args.n_packets)
