#  E.03.00_服务端游标的约束

## E.03.00_服务端游标的约束

通过`mysql_stmt_attr_set()` C API函数实现了服务器端游标。同时可应用在存储例程中。服务器端游标允许在服务器端生成结果集，但不会将其传输到客户端，除非客户端请求这些行。例如，如果客户端执行了查询，但仅对第1行感兴趣，那么不会传输剩余的行。
 
MySQL中，服务端游标由内部临时表来维护。开始时，此表是一个MEMORY表，当系统变量值超过max_heap_table_size 和 tmp_table_size时，可转化为MyISAM表。 特别要注意的是，此限制同样适用于使用游标来创建的内部临时表生成的结果集。可参考 [Section 8.4.3.3, “How MySQL Uses Internal Temporary Tables”.](./08.04.03_Optimizing_for_Many_Tables.md) 当使用游标对大的结果集进行取值时，速度可能会变慢。
 
* 游标是只读的，不能使用游标来更新行数据。
 
* 不支持`UPDATE` `WHERE` `CURRENT` `OF`和`DELETE` `WHERE` `CURRENT` `OF` 语句，这是因为不支持可更新的游标。
 
* 游标是不可保持的（提交后不再保持打开）。
 
* 游标是不敏感的。
 
* 游标是不可滚动的。
 
* 游标是未命名的。语句处理程序起着游标ID的作用。
 
* 对于每条预处理语句，仅能打开1个游标。如果需要多个游标，必须处理多条语句。
 
* 如果在预处理模式下不支持此类语句产生的结果集（包括`CHECK TABLES`、`HANDLER READ`和`SHOW BINLOG EVENTS`等语句）则不能使用游标。


