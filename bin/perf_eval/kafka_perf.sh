# <<< Producer >>>

# Test on message size
for RECORD_SIZE in 1 10 100 1000 10000
do
    echo "Record Size $RECORD_SIZE:" >> kafka_pperf_1M_size.txt
    kafka-producer-perf-test --topic test --num-records 1000000 --throughput -1 --producer-props bootstrap.servers=localhost:9092 batch.size=1000 acks=1 linger.ms=100000  request.timeout.ms=300000 --record-size $RECORD_SIZE >> kafka_pperf_1M_size.txt
done

# Test on message number
for NUM_RECORD in 100 1000 10000 100000 1000000
do
    echo "Record Num $NUM_RECORD" >> kafka_pperf_1KB_num.txt
    kafka-producer-perf-test --topic test --num-records $NUM_RECORD --throughput -1 --producer-props bootstrap.servers=localhost:9092 batch.size=1000 acks=1 linger.ms=100000  request.timeout.ms=300000 --record-size 1000 >> kafka_pperf_1KB_num.txt
done

# Test on size and number
for RECORD_SIZE in 1 10 100 1000 10000
do
    echo "Record Size $RECORD_SIZE, Record Num $(1000 * 1024 * 1024 / $RECORD_SIZE):" >> kafka_pperf_1GB_sizeNum.txt
    kafka-producer-perf-test --topic test --num-records $(1000 * 1024 * 1024 / $RECORD_SIZE) --throughput -1 --producer-props bootstrap.servers=localhost:9092 batch.size=1000 acks=1 linger.ms=100000  request.timeout.ms=300000 --record-size $RECORD_SIZE >> kafka_pperf_1GB_sizeNum.txt
done

# Test on batch size
for BATCH_SIZE in 1000 5000 10000 50000 100000
do
    echo "Batch Size $BATCH_SIZE" >> kafka_pperf_1GB_batchsize.txt
    kafka-producer-perf-test --topic test --num-records 100000 --throughput -1 --producer-props bootstrap.servers=localhost:9092 batch.size=$BATCH_SIZE acks=1 linger.ms=100000  request.timeout.ms=300000 --record-size 1000 >> kafka_pperf_1GB_batchsize.txt
done

# Test on partition number
for PART_NUM in 1 2 3 5 10 50
do
    echo "PART NUM $PART_NUM" >> kafka_pperf_1GB_partnum.txt
    kafka-producer-perf-test --topic test_p$PART_NUM --num-records 100000 --throughput -1 --producer-props bootstrap.servers=localhost:9092 batch.size=$BATCH_SIZE acks=1 linger.ms=100000  request.timeout.ms=300000 --record-size 1000 >> kafka_pperf_1GB_partnum.txt
done


# <<< Consumer >>>
# Test on message size
for MSG_SIZE in 1 10 100 1000 10000
do
    kafka-consumer-perf-test --topic test_s$MSG_SIZE --bootstrap-server localhost:9092 --messages 100000 >> kafka_cperf_100K_size.txt
done

# Test on message number
for MSG_NUM in 100 1000 10000 100000 1000000
do
    kafka-consumer-perf-test --topic test --bootstrap-server localhost:9092 --messages $MSG_NUM >> kafka_cperf_1K_num.txt
done

# Test on threads number
for THREAD_NUM in 1 2 3 5 10 50
do
    kafka-consumer-perf-test --topic test --bootstrap-server localhost:9092 --messages 100000 --threads >> kafka_cperf_1GB_tnum.txt
done

