# Jalal Khan
# 9/1/16
# This program uses regular expressions to find all links in an html doc grabbed from a url input by the user
# Outputs a list of all the relative links and absolute links, with counts
import urllib2, re

# connect to url and construct regular expressions to use
# use one regex for each type of url we want to count
url = raw_input('Enter a url:')
html = urllib2.urlopen(url).read()
# find an expression beginning with href=[containing 0 or 1 of ' or "] 
# (returning everything until one of \,',", ,> is found)
abs_expr = r'<a (href)=[\'"]?http([^\'" >]+)'
rel_expr = r'<a href=[\'"]?/([^\'" >]+)'

# read/write to file
f = open('hw_1.txt', 'r+')
f.write(html)
f.seek(0)
abs_links = re.findall(abs_expr, f.read())
f.seek(0)
rel_links = re.findall(rel_expr, f.read())
f.close()

print 'absolute urls: ' + str(len(abs_links))
print abs_links

print 'relative urls: ' + str(len(rel_links)) + '\n'  
print '\n'.join(rel_links)
