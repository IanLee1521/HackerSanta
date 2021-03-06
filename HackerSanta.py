#!/usr/bin/env python3

import csv
import sys
import time
import random
import argparse
from datetime import datetime


class SecretSanta():

    BOLD = '\x1b[1m'
    RESET = '\x1b[0m'
    quotes = []
    names = {}
    giverphrases = []

    def __init__(self, filename, quotesfile="quotes.txt", giverphrasesfile="giverphrases.txt"):
        self.chosen = {}
        fh = open(quotesfile, 'rt')
        for line in fh:
            line = line.strip().strip('"')
            line = line.replace(r'\n', '\n')
            if line:
                self.quotes.append(line)
        fh.close()

        fh = open(giverphrasesfile, 'rt')
        for line in fh:
            line = line.strip().strip('"')
            line = line.replace(r'\n', '\n')
            if line:
                self.giverphrases.append(line)
        fh.close()

        ch = open(filename, 'rt')
        csvfile = csv.reader(ch, delimiter=',')
        for row in csvfile:
            self.names[row[1]] = row[0]
        ch.close()


    def random_crap(self):
        phrases = [
            'Thinking', 'Calculating', 'Growing Random Decision Trees',
            'Harvesting the Neural Network', 'Leveraging Core Competancies',
            'Letting the Smoke Out',
            'Flipping bits pseudo-randomly',
            'Leveraging quantum computing',
            'Plugging in my Tesla',
            'My CPU hurts'
        ]
        print('\x1b[2J\x1b[H\r\n\r\n\r\n\r\n\r\n')
        i = 0
        print('\x1b[3m    {} '.format(random.choice(phrases)), end='')
        while i < random.randint(6,24):
            print('.', end='')
            sys.stdout.flush()
            time.sleep(random.random() + 0.1)
            i += 1
        print('\x1b[0m')

    def run(self):
        print('''
>>>> PRESS ENTER TO BEGIN <<<<
''')
        input()
        while True:
            self.random_crap()
            quote = random.choice(self.quotes)
            name, giver = self.choose_name()
            if not name:
                break
            print('_' * 78)
            print('''
\x1b[2m    The Sorting Hat Chooses: \x1b[0m[\x1b[1m{}\x1b[0m]

    \x1b[{}m{}\x1b[0m
'''.format(name, random.randint(31, 36), self.format_quote(quote)))
            print('_' * 78)
            sys.stdin.flush()
            print('{} names remaining. <Enter to reveal giver...>'.format(len(self.names)))
            input('')
            statement = random.choice(self.giverphrases)
            print(' --<[ \x1b[{}m{}\x1b[0m {} \x1b[{}m{}\x1b[0m ]>--\r\n'.format(
                random.randint(41, 46), giver, statement,
                random.randint(41, 46), name))
            ans = input('What next (r=repeat choice, enter=continue): ')
            if ans.startswith('r'):
                del self.chosen[name]
                self.names[name] = giver
        self.results()

    def format_quote(self, quote):
        if len(quote) <= 70:
            return quote
        newq = ''
        l = 70
        for word in quote.split():
            newq += word + ' '
            if len(newq) > l:
                newq += '\r\n    '
                l += 70
        return newq

    def results(self):
        print("\x1b[2J\x1b[H" + r"""
      __,_,_,___)          _______
    (--| | |             (--/    ),_)        ,_)
       | | |  _ ,_,_        |     |_ ,_ ' , _|_,_,_, _  ,
     __| | | (/_| | (_|     |     | ||  |/_)_| | | |(_|/_)___,
    (      |___,   ,__|     \____)  |__,           |__,

                            |                         _...._
                         \  _  /                    .::o:::::.
                          (\o/)                    .:::'''':o:.
                      ---  / \  ---                :o:_    _:::
                           >*<                     `:}_>()<_{:'
                          >0<@<                 @    `'//\\'`    @
                         >>>@<<*              @ #     //  \\     # @
                        >@>*<0<<<           __#_#____/'____'\____#_#__
                       >*>>@<<<@<<         [__________________________]
                      >@>>0<<<*<<@<         |=_- .-/\ /\ /\ /\--. =_-|
                     >*>>0<<@<<<@<<<        |-_= | \ \\ \\ \\ \ |-_=-|
                    >@>>*<<@<>*<<0<*<       |_=-=| / // // // / |_=-_|
      \*/          >0>>*<<@<>0><<*<@<<      |=_- |`-'`-'`-'`-'  |=_=-|
  ___\\U//___     >*>>@><0<<*>>@><*<0<<     | =_-| o          o |_==_|
  |\\ | | \\|    >@>>0<*<<0>>@<<0<<<*<@<    |=_- | !     (    ! |=-_=|
  | \\| | _(UU)_ >((*))_>0><*<0><@<<<0<*<  _|-,-=| !    ).    ! |-_-=|_
  |\ \| || / //||.*.*.*.|>>@<<*<<@>><0<<@</=-((=_| ! __(:')__ ! |=_==_-\
  |\\_|_|&&_// ||*.*.*.*|_\\db//__     (\_/)-=))-|/^\=^=^^=^=/^\| _=-_-_\
  ''''|'.'.'.|~~|.*.*.*|     ____|_   =('.')=//   ,------------.
      |'.'.'.|   ^^^^^^|____|>>>>>>|  ( ~~~ )/   (((((((())))))))
      ~~~~~~~~         '''''`------'  `w---w`     `------------'""")
        input('Press ANY key to continue...')
        sortednames = sorted(self.chosen, key=lambda x: int(self.chosen[x][0].strftime('%s')))
        pos = 1
        for i in sortednames:
            when = self.chosen[i][0].strftime('%H:%M:%S')
            print('Choice {:02d} at {} UTC: \x1b[1m{}\x1b[0m'.format(pos, when, i))
            pos += 1

    def choose_name(self):
        if len(self.names) == 0:
            return '', ''
        while True:
            name = random.choice(list(self.names.keys()))
            if name not in self.chosen:
                self.chosen[name] = datetime.utcnow(), name, self.names[name]
                giver = self.names[name]
                del self.names[name]
                break
        return name.strip(), giver.strip()

if __name__ == '__main__':
    print('''
<><><><><><><><><><><><><><><><><><><><><><>
     ____  ____  ___  ____  ____  ____ 
    / ___)(  __)/ __)(  _ \(  __)(_  _)
    \___ \ ) _)( (__  )   / ) _)   )(  
    (____/(____)\___)(__\_)(____) (__) 
     ____   __   __ _  ____  __        
    / ___) / _\ (  ( \(_  _)/ _\       
    \___ \/    \/    /  )( /    \      
    (____/\_/\_/\_)__) (__)\_/\_/ 
\x1b[1m
    Version 0.0.1 Elfa Ho Ho Ho
    AI, Machine Learned, Neural Network
    Enhanced Mega Code
    Author: Joff Thyer Copyright (c) 2020
\x1b[0m
<><><><><><><><><><><><><><><><><><><><><><>''')
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-q', '--quotes',
        default='quotes.txt',
        help='funny quotes file (one line per quote)'
    )
    parser.add_argument(
        '-gp', '--giverphrases',
        default='giverphrases.txt',
        help='funny giver phrases file (one line per)'
    )
    parser.add_argument('filename')
    args = parser.parse_args()
    ss = SecretSanta(
        args.filename,
        quotesfile=args.quotes,
        giverphrasesfile=args.giverphrases)
    ss.run()
