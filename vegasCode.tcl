
# Simulation Topology
#              n1                  n5
#               \                  /
#   4000Mb,500ms \   1000Mb,50ms  / 4000Mb,500ms
#              n3 --------------- n4
#   4000Mb,800ms /                \ 4000Mb,800ms
#               /                  \
#             n2                   n6 

set ns [new Simulator]

$ns color 1 Blue
$ns color 2 Red

set namfile [open vegas.nam w]
$ns namtrace-all $namfile
set tracefile1 [open vegasTrace.tr w]
$ns trace-all $tracefile1

proc finish {} {
    global ns namfile
    $ns flush-trace
    #Close the NAM trace file
    close $namfile
    #Execute NAM on the trace file
    # exec nam reno.nam &
    exit 0
}

set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

$ns duplex-link $n1 $n3 4000Mb 500ms DropTail
$ns duplex-link $n2 $n3 4000Mb 800ms DropTail 
$ns duplex-link $n3 $n4 1000Mb 50ms DropTail
$ns duplex-link $n4 $n5 4000Mb 500ms DropTail
$ns duplex-link $n4 $n6 4000Mb 800ms DropTail

$ns queue-limit $n3 $n4 10
$ns queue-limit $n4 $n3 10

$ns duplex-link-op $n1 $n3 orient right-down
$ns duplex-link-op $n2 $n3 orient right-up
$ns duplex-link-op $n3 $n4 orient right
$ns duplex-link-op $n4 $n5 orient right-up
$ns duplex-link-op $n4 $n6 orient right-down

set source1 [new Agent/TCP/Vegas]
#$ns at 0 "$source1 select_ca vegas"
$source1 set class_ 2
$source1 set ttl_ 64
$source1 set window_ 1000
$source1 set packet_size_ 1000

$ns attach-agent $n1 $source1
set sink1 [new Agent/TCPSink/Sack1]
$ns attach-agent $n5 $sink1
$ns connect $source1 $sink1
$source1 set fid_ 1

set source2 [new Agent/TCP/Vegas]
#$ns at 0.0 "$source2 select_ca vegas"
$source2 set class_ 1
$source2 set ttl_ 64
$source2 set window_ 1000
$source2 set packet_size_ 1000

$ns attach-agent $n2 $source2
set sink2 [new Agent/TCPSink/Sack1]
$ns attach-agent $n6 $sink2
$ns connect $source2 $sink2
$source2 set fid_ 2

$source1 attach $tracefile1
$source1 tracevar cwnd_ 
$source1 tracevar ssthresh_
$source1 tracevar ack_
$source1 tracevar maxseq_
$source1 tracevar rtt_

$source2 attach $tracefile1
$source2 tracevar cwnd_ 
$source2 tracevar ssthresh_
$source2 tracevar ack_
$source2 tracevar maxseq_
$source2 tracevar rtt_


set myftp1 [new Application/FTP]
$myftp1 attach-agent $source1


set myftp2 [new Application/FTP]
$myftp2 attach-agent $source2


$ns at 0.0 "$myftp2 start"
$ns at 0.0 "$myftp1 start"

$ns at 100.0 "finish"

$ns run
