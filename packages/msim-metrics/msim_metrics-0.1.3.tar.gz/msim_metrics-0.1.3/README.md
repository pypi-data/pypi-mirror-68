1.库依赖

    zmq
    logging 
    os
2.安装

    python3 -m pip install msim_metrics


3.使用方法

MetricSetter

    MetricSetter的功能是连接远端时序数据库Influxdb，指向指定表，并上传数据。使用方法：

a）导入

    from metrics.metrics import MetricSetter

b）指定表（无则创建）

    table = MetricSetter("table_name")

c）上传数值(value为float类型)

    table.set_status(value)

MetricCounter

     MetricCounter的功能是连接远端时序数据库Influxdb，指向指定表，并完成打点操作。使用方法：

a）导入

    from metrics.metrics import MetricCounter

b）指定表（无则创建）

    table = MetricCounter("table_name")

c）打点加一(上传数值1)

    table.add()

d）打点减一(上传数值-1)

    table.sub()

e）保持不变(上传数值0)

    table.keep()# msim_metrics

