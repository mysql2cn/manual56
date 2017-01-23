## E.01.00_条件语句的约束

预处理SQL语句 中，不允许出现`SIGNAL`, `RESIGNAL`, 和 `GET DIAGNOSTICS`语句，如下所示，语句是无法执行的(无效)：
```sql
     PREPARE stmt1 FROM 'SIGNAL SQLSTATE "02000"';
``` 
对于SQLSTATE的值 '04' ，进行同样的处理(也是无效的).
 
标准的SQL有一个诊断的堆栈（包含上下文执行内嵌的诊断)。标准的SQL语法使用`GET STACKED DIAGNOSTICS`进行区域堆栈诊断。
 
MySQL不支持`STACKED`关键字，因为已经有区域堆栈诊断进行了诊断信息的收集。可参考[See also Section 13.6.7.7, “The MySQL
Diagnostics Area”](./13.06.07_Condition_Handling.md)
 
标准的SQL中，第一个条件语句的的执行情况要由`SQLSTATE`的值来决定。但在MYSQL中，并不保证能够获得此值。想要得到主要的错误信息，可以使用以下方法：
```sql
GET DIAGNOSTICS CONDITION 1 @errno = MYSQL_ERRNO;
``` 
  或者使用以下方法
```sql
GET DIAGNOSTICS @cno = NUMBER;
GET DIAGNOSTICS CONDITION @cno @errno = MYSQL_ERRNO;
``` 