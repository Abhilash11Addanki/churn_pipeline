	.Ȗ���?.Ȗ���?!.Ȗ���?	;�l�}� @;�l�}� @!;�l�}� @"e
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails$.Ȗ���?����K�?AnR�X�;�?Y���-��?*�t�^[@����>�@2�
xIterator::Model::Prefetch::Rebatch::Prefetch::Map::ParseExampleV2::BatchV2::ShuffleAndRepeat::LegacyParallelInterleaveV2@��bg
�?!a����:@)��bg
�?1a����:@:Preprocessing2T
Iterator::Prefetch::Generator��Z���?!M�g�4@)��Z���?1M�g�4@:Preprocessing2�
JIterator::Model::Prefetch::Rebatch::Prefetch::Map::ParseExampleV2::BatchV2eU�����?!�y��1L@)	m9���?1G�h7I2@:Preprocessing2�
\Iterator::Model::Prefetch::Rebatch::Prefetch::Map::ParseExampleV2::BatchV2::ShuffleAndRepeat@���O��?!9��Z41C@)ߩ�{�?�?1 8�(P�'@:Preprocessing2�
�Iterator::Model::Prefetch::Rebatch::Prefetch::Map::ParseExampleV2::BatchV2::ShuffleAndRepeat::LegacyParallelInterleaveV2[0]::FlatMap@m���5�?!n�2�0@)�Y�b+h�?1�pӮ/�"@:Preprocessing2�
�Iterator::Model::Prefetch::Rebatch::Prefetch::Map::ParseExampleV2::BatchV2::ShuffleAndRepeat::LegacyParallelInterleaveV2[0]::FlatMap[0]::TFRecord@��)�?!��Em5�@)��)�?1��Em5�@:Advanced file read2Y
"Iterator::Model::Prefetch::RebatchaQ���?!�Ycg�?)y$^���?1E���|�?:Preprocessing2F
Iterator::Model��@�S�?!?}�z��?)'N�w(
�?1�o��(l�?:Preprocessing2h
1Iterator::Model::Prefetch::Rebatch::Prefetch::Mapj1x���?!_5=� ��?)횐�t�?1d�kwW��?:Preprocessing2x
AIterator::Model::Prefetch::Rebatch::Prefetch::Map::ParseExampleV20�AC��?!�_�A�u�?)0�AC��?1�_�A�u�?:Preprocessing2I
Iterator::Prefetch�䠄��?!![C
�?)�䠄��?1![C
�?:Preprocessing2c
,Iterator::Model::Prefetch::Rebatch::Prefetch����a�}?!v�h���?)����a�}?1v�h���?:Preprocessing2P
Iterator::Model::Prefetch��#�&}?!�=�F��?)��#�&}?1�=�F��?:Preprocessing:�
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
�Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
�Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
�Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
�Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)�
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis�
both�Your program is MODERATELY input-bound because 8.5% of the total step time sampled is waiting for input. Therefore, you would need to reduce both the input time and other time.no*high2t26.2 % of the total step time sampled is spent on 'All Others' time. This could be due to Python execution overhead.9;�l�}� @>Look at Section 3 for the breakdown of input time on the host.B�
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown�
	����K�?����K�?!����K�?      ��!       "      ��!       *      ��!       2	nR�X�;�?nR�X�;�?!nR�X�;�?:      ��!       B      ��!       J	���-��?���-��?!���-��?R      ��!       Z	���-��?���-��?!���-��?JCPU_ONLYY;�l�}� @b 