#!/usr/bin/expect

set timeout 5
spawn ssh michihiro@10.4.134.209
expect "Password: "
send "xxxxxx enter your password xxxxxx\n"
expect "da3>"
send "ena\n"
expect "da3#"
send "start-shell\n"
expect "sh-4.2$ "
send "su\n"
expect "da3>"
send "ena\n"
expect "da3#"
send "start-shell\n"

expect "sh-4.2# "
send "scp /media/card/sysmon.log michihiro@10.4.162.226:/home/michihiro/aeroz-logs/\n"
expect "password:"
send "xxxxxx enter your password xxxxxx\n"
expect "sh-4.2# "
send "exit\n"
expect "da3#"
send "exit\n"
expect "sh-4.2$ "
send "exit\n"
expect "da3#"
send "exit\n"
interact
