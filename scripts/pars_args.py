import argparse
import logging as log

def parse_args():
    parser = argparse.ArgumentParser(description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086, help='port of InfluxDB http API')
    log.info('PARSER: ' + str(parser.parse_args()))
    log.info(parser.parse_args().host)
    log.info(parser.parse_args().port)
    return parser.parse_args()
