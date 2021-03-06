import ROOT
import pickle
import os,sys
from fnmatch import fnmatch

#
# Read results from the log file:
#   compare mass info with file name
#   read dictionary string with results
#
def parseLogFile(fn,smglu,smlsp):
    fields = None
    for i,l in enumerate(open(fn)):
        if i>1:
            print "*** log file parsing failed 1 for ",fn
            return None
        idx = l.find("{")
        if idx<0:
            print "*** log file parsing failed 2 for ",fn
            return None
        hdr = l[:idx]
        lims = eval(l[idx:-1])
        fields = hdr.split()
        if not ( len(fields)==7 and fields[0]=="Result" ):
            print "*** log file parsing failed 3 for ",fn
            return None
        if not ( fields[4]==smglu and fields[5]==smlsp ):
            print "*** log file parsing failed 4 for ",fn
            return None
    if fields==None:
        print "No results for ",fn
        return None
    return [ int(fields[4]), int(fields[5]), lims ]

#
# define full set of mass points
#
expLimits = [ ]

binCombis = [ ]
for d in os.listdir(sys.argv[1]):
    if fnmatch(d,"[0-9]*") and os.path.isdir(sys.argv[1]+"/"+d):
        binCombis.append(d)

for b in binCombis:

    results = parseLogFile(sys.argv[1]+"/"+b+"/limit_"+sys.argv[2]+"_"+sys.argv[3]+".log", 
                           sys.argv[2],sys.argv[3])
    if len(results[2]) != 5:
        continue
    expLimits.append((b,results[2]["0.160"],results[2]["0.500"],results[2]["0.840"]))

expLimits.sort(key=lambda x: x[0])
for x in expLimits:
    if type(x[0])==type(0):
        print "{0:30d}   {1:8.2f} {2:8.2f} {3:8.2f}".format(x[0],x[1],x[2],x[3])
    else:
        print "{0:30s}   {1:8.2f} {2:8.2f} {3:8.2f}".format(x[0],x[1],x[2],x[3])


