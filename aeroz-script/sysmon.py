#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import datetime

output  = '/media/card/sysmon.log'
pidfile = '/var/run/sysmon.pid'
wait    = 30


def readPID( remove ):
    """ Read a PID
    Args:
        None

    Returns:
        Int: pid
        False: Failed
    """
    global pidfile
    try:
        fd = open( pidfile, 'r' )
    except:
        return False

    try:
        pid = int( fd.read( 1024 ) )
        fd.close()
        if remove is True:
            os.unlink( pidfile )
    except:
        fd.close()
        os.unlink( pidfile )
        return False

    return pid

def writePID( pid ):
    """ Write a PID
    Args:
        Write PID number

    Returns:
        True:  Success
        False: Failed
    """
    global pidfile
    try:
        fd = open( pidfile, 'w' )
    except:
        return False

    try:
        fd.write( str( pid ) )
    except:
        fd.close()
        return False

    fd.close()
    return True


def popen( cmd, fd ):
    """ Execute command and write log
    Args:
        cmd: Execute command
        fd:  Write file handle

    Returns:
        None
    """
    try:
        fd.write( "-- " + cmd + "\n" )
        p = os.popen( cmd )
    except:
        return

    try:
        for line in p:
            fd.write( line )
    except:
        pass

    p.close()

def main():
    """ Main function
    Args:
        None

    Returns:
        None
    """
    global output
    try:
        fd = open( output, 'a' )
    except:
        return

    try:
        fd.write( "----- " )
        fd.write( datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") )
        fd.write( "----- \n" )
        popen( '/bin/df -h', fd )
        popen( '/usr/bin/top -b -n 1', fd )
        popen( '/usr/bin/free -k', fd )
        popen( '/bin/ps axh -o comm,rss --sort -rss | /usr/bin/head -n 5', fd )
        popen( '/bin/ps axh -o comm,vsz --sort -vsz | /usr/bin/head -n 5', fd )
        fd.write( "--------------------------------------------------- \n" )
    except:
        pass

    fd.close()


if len( sys.argv ) > 1:
    if sys.argv[ 1 ].lower() == "stop":
        pid = readPID( True )
        if pid is False:
            print "Can't read pid..."
            exit( 1 )
        os.kill( pid, 9 )
        exit ( 0 )
    elif sys.argv[ 1 ].lower() == "start":
        pid = readPID( False )
        if pid is not False:
            print "PID file found."
            print "execute 'rm -f %s' command if it's not running." % pidfile
            exit( 1 )
    else:
        print "Unkown command"
else:
    print """Usage: %s [start|stop]
    """ % sys.argv[ 0 ]
    exit( 0 )


pid = os.fork()
if pid < 0:
    exit( 1 )
elif pid > 0:
    if writePID( pid ) is False:
        print "Can't write PID file. pid=%d" % pid
    exit( 0 )
os.setsid()

while True:
    main()
    time.sleep( wait )
