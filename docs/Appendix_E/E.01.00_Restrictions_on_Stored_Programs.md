## E.01.00_存储程序的约束
 
 这些限制同样适用于[Chapter 19 Stored Programs and Views](./Chapter_19.00.00/Stored_Programs_and_Views.md)

 这里介绍的某些限制适用于所有的存储例程，即存储过程和存储函数。某些限制仅适用于存储函数而不是存储程序，同样有些限制仅适用于存储函数而不是存储程序。
 
 存储函数的限制也适用于触发器。也有一些特定的限制只对特定的触发器适用。
 
 存储过程的限制也适用于事务管理中的Do子句，也有一些特定的事件有特定的限制
 
### 存储例程中不允许的SQL语句
 
  存储过程不能包含任意SQL语句。在存储过程中，禁止使用下述语句：

  * 锁相关语句 `LOCK TABLES` 和 `UNLOCK TABLES`
  
  * `ALTER VIEW`
  
  * `LOAD DATA` 和 `LOAD TABLE`
  
  *  SQL预处理语句（`PREPARE`、`EXECUTE`、`DEALLOCATE` `PREPARE`），可以在存储过程中使用，但不能在存储函数或者触发器中使用，因此，不能在存储过程和触发器中使用动态SQL语句（其中，能够以字符串形式构造动态语句，可以以字符串形式执行）。
 
  * 一般来说,不允许使用SQL预处理语句在存储过程中的话，同样不允许在存储程序中使用，关于SQL预处理语句可以参考[Section 13.5, “SQL Syntax for Prepared Statements”](./13.05.00_SQL_Syntax_for_Prepared_Statements.md)。但对于`SIGNAL`,`RESIGNAL`和`GET DIAGNOSTICS`,可以使用存储程序中使用，不能在预处理语句中使用。
 
  * 因局部变量只在创建存储程序中有效，所以在创建存储程序中不允许使用预处理语句。预处理语句有效范围只存在于当前会话中，而不是在存储程序中，也就是说存储程序执行完成后，变量会失效。举例来说：`SELECT ... INTO local_var `语句和中不能使用预处理SQL语句，存储过程和存储函数同样有此限制。可参考 [Section 13.5.1, “PREPARE Syntax”.](./13.05.01_PREPARE_Syntax.md)
 
  * 数据延迟插入并不能做到真正的延迟插入，`INSERT DELAYED` 被视为正常的数据插入动作。
 
  * 在存储程序中(存储过程、存储函数、触发器、事件),解析器以 `BEGIN ... END` 块进行对待.在上下文切换中，使用`START TRANSACTION` 进行事务的开始标志
 
### 存储函数的限制
 
  在存储函数中禁止使用下列语句或操作，但可以在由存储函数或触发器触发的存储过程中使用。举例来说，读者可以在一个存储过程中使用`FLUSH`，此存储过程不可能由存储函数或触发器来触发。尽管能够在存储程序中使用`FLUSH`，但不能从存储函数或触发程序（触发器）调用这类存储程序。
     
  * 执行显式或隐式提交或回滚操作的语句。对这些语句的支持并未包含在标准的SQL标准中，需要由DBMS厂商来决定是否支持。
  * 
  * 返回结果集的语句。包括没有`INFO`子句的`SELECT`语句，以及`SHOW`语句。能够`用SELECT … INTO`，或使用游标和`FETCH`语句处理结果集的函数。参考 [Section 13.2.9.1, “SELECT ... INTO Syntax”,](./13.02.09_SELECT_Syntax.md) 和  [Section 13.6.6, “Cursors“](./13.06.06_Cursors.md)
  * 
  * `FLUSH`语句。
  * 不能以递归方式使用存储函数。
  * 
  * 当对一个表的操作被存储过程或者触发器触发时，无法修改此表(表正在被读或写)。
  * 
  * 临时表被一个存储过程使用多个不同的别名时，会发生 
Can't reopen table: 'tbl_name' 错误 ，即使引用的表在不同的函数中。

  * `HANDER ...READ` 语句 在存储过程中使用时，会引起复制错误。
 
### 触发器的限制
 
对于触发器来说，有以下限制：

  * 触发器不能因外键限制而进行触发。
  * 主服务器在复制时，使用基于行复制时，从服务器中的触发器不能被触发。当从服务器使用基于语句复制时，才能够触发，可参考[Section 16.4.1.31, “Replication and Triggers”](./16.04.01_Replication_Features_and_Issues.md)
 
 * 因为`TURN`语句不能返回一个具体的值，所以不能在触发器中使用，立刻退出一个触发器，可以使用`LEAVE`语句。
 
 * 触发器不能在内置的Mysql数据库的表中使用。
 
 * 触发器使用中对于元数据未进行相应的检查，如果触发器加载缓存前引用的表已经改变，则触发器可能使用过期的元数据。
      
### 存储例程名字冲突
 
 同样的标识可能被用在多个位置，如 存储例程参数，局部变量，表中的一列，同样，相同的局部变量也能被用于内嵌的块中，如下所示：
```sql
CREATE PROCEDURE p (i INT)
BEGIN
  DECLARE i INT DEFAULT 0;
  SELECT i FROM t;
  BEGIN
   DECLARE i INT DEFAULT 1;
   SELECT i FROM t;
  END;
END;
```
 
在此种情况下，标识是任意的，但有一个优先级的规则：
 
  * 局部变量优于例程(routine)参数或者表中的列
  * 例程(routine)参数优于表中的列
  * 局部变量在内部块(Inner block) 优于外部块(outber block) 
 
各种变量优于表中的列，并不是标准的SQL内容。
 
#### 复制问题（Replication Considerations）
 
使用存储例程可能会在数据库复制中引起问题，可参考[Section 19.7,
“Binary Logging of Stored Programs”.](./19.07.00_Binary_Logging_of_Stored_Programs.md)
 
  复制过程的参数 `--replicate-wild-do-table=db_name.tbl_name [2016]` 选项适用于表、视图和触发器，而不适用于存储过程、存储函数和事件。要想过滤此参数，可以使用 `use one or more of the --replicate-*-db` 选项。
    
#### 诊断问题(Debugging Considerations)

没有相应的存储例程应限制
 
#### Unsupported Syntax from the SQL:2003 Standard
 
   MySQL的存储routine 语法是基于SQL:2003 标准，但并不支持 `UNDO` Handlers 和 FOR loops（FOR循环)。
 
#### 并发考虑
 
为防止服务器会话之间互相影响，当客户端发起一个语句时，服务器会使用例程和触发器的快照功能，意味着服务器会首先计算一系列的子程序、函数及触发器为语句执行创建可用资源，当语句执行时，不影响其它会话。
 
为支持尽可能大的并发数，应尽量减少使用存储函数带来的影响。特别是更新表时减少存储函数对并发操作的影响。存储函数在执行前获得表锁，避免出现数据不一致情况(二进制日志中)。当使用基于语句的日志记录(statement-based binary logging)时，随时记录，而不是在存储函数执行过程中进行日志记录，因此，存储函数与更新相同的底层表不
并行执行。与使用二进制日志相比，存储过程执行中不用获得表锁，所有语句执行存储过程时，会写进二进制日志中，而不用理会基于语句的日志记录（statement-based binary logging），可参考 [See Section 19.7, “Binary Logging of Stored Programs”.](./19.07.00_Binary_Logging_of_Stored_Programs.md)
          
#### 事件管理器限制
 
事件管理器有以下限制：
 
* 事件名字不区分大小写，举例来说，你不能在一个数据库中有两个这样的的名字anEvent 和 AnEvent，他们的名字是一样的。
* 
* 存储例程, 触发器和事件不应该创建、删除或改变一个事件 ，一个事件也不应创建、删除或改变例程或触发器。
* 
* 当`LOCK TABLE` 语句起作用时，事件不应出现在数据库的DDL操作。
* 
* 事件定义中，`YEAR`, `QUARTER`, `MONTH`, 和 `YEAR_MONTH` 可以按月份进行定义，其它间隔以秒来定义。没有方法能够以秒来定义事件执行的顺序，另外，事件执行可能会延迟1到2秒的时间，由于受到四舍五入、程序线程等因素影响。但可以从`INFORMATION_SCHEMA.EVENTS` 表中的 `LAST_EXECUTED` 列 或者`mysql.event` 表的 `last_executed` 列得到精确到1秒之内的事件实际执行时间。也可参考[Bug #16522]()
 
* 事件执行过程中，会创建连接，但事件语句对于服务器端的`SHOW STATUS`中的 `Com_select` 和 `Com_insert` 没有影响，这些计数器值会在全局中更新。

* 事件不支持 Unix Epoch(2038年初)的时间，事件管理器中不允许出现这些日期。参考[Bug #16396]()
* 
* 在`CREATE EVENT` 和 `ALTER EVEN`T中，不支持 `ON SCHEDULE`从句中的存储函数、用户自定义函数和表，更多信息参考 [BUG#22830]()
