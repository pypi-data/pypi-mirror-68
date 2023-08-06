# Wakanda

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This tool is useful to extract data from various african's websites.


# New Features!

  - Hitorical data for stocks from more than 8 africans markets (BRVM, Ghana, Nigeria, Kenya and more)
  - Get real-time data ( at this point this worked only for BRVM 

### Installation

From pypi with pip:
```sh
$ pip install wakanda
```
### Usage example

Use afx.kwayisi as main source of data, ranging up to 7 years.
```sh
$ import wandaka as wkd 
# Initialize market (eg:brvm).you could also choose ghana(gse), nigeria(ngse)..
$ brvm = wkd.stock('brvm')
# now you can collect stock data for all stocks under that market
$ brvm.DataReader('BICC')
 	    Date	close price	
    0	09-16-2013	43000	
    1	09-23-2013	42000
    2	09-26-2013	42000
    3	10-01-2013	42000
    4	10-02-2013	42000

# you may specify start and end dates
$ gse = wkd.stock('gse')
$ gse.DataReader('MTNGH' start='01-09-2020',end='01-13-2020')
        Date	close price
    0	01-09-2020	0.7
    1	01-10-2020	0.7
    2	01-13-2020	0.7
```
Get live quote from markets' official website
```sh
$ from wakanda import wkd
brvm = wkd.stock('brvm')
brvm.get_quote('BICC')
```
License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
