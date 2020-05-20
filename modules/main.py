from beancount import loader
import argparse
from beancount_plac import beancount_plac
from beancount.query import query

def main():
    parser = argparse.ArgumentParser(description='filename')
    parser.add_argument('filename', help='path to beancount journal file')
    args = parser.parse_args()  
    entries, errors, options_map = loader.load_file(args.filename)
    test = beancount_plac(entries, options_map)
    print(test.plac_tables())
    
#print(actuals)
if __name__ == '__main__':
    main()
