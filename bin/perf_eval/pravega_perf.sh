# With Pravega-Benchmark Tools
# <<< Producer >>>
# Test on events number
for EVENTS_SIZE in 1 10 100 1000 10000
do
    ./run/pravega-benchmark/bin/pravega-benchmark  \
    -controller tcp://127.0.0.1:9090  \
    -stream test \
    -producers 1 \
    -segments 1 \
    -size $EVENTS_SIZE \
    -throughput -1  \
    -events 100000 >> pravega_pperf_100K_size.txt
done
