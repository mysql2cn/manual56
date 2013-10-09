##  E.04.00_子查询中的约束

* 对于`IN`的子查询优化不如对“=”的优化那样有效。
 
 对于不良`IN`性能的一种典型情况是，当子查询返回少量行，但外部查询返回将与子查询结果相比的大量行。
 
 存在的问题如下：对于IN子查询来讲，优化器会生成相应的子查询，考虑下列语句(不正确的子查询语句)
```sql
 SELECT ... FROM t1 WHERE t1.a IN (SELECT b FROM t2);
```
   优化器会重新生成相应的正确的子查询
```sql
  SELECT ... FROM t1 WHERE EXISTS (SELECT 1 FROM t2 WHERE t2.b = t1.a);
```
 如果内部和外部查询返回M和N行，则子查询的执行时间就是(M×N)，而不是(M+N). 从而可以看到，在返回同样的数据情况下，一个IN 
子查询比IN(value_list)要慢的多。
 
* 一般而言，子查询不能修改表，并对表自身进行选择（同一个子查询）。例如，该限制适用于具有下述形式的语句：
```sql
DELETE FROM t WHERE ... (SELECT ... FROM t ...);
UPDATE t ... WHERE col = (SELECT ... FROM t ...);
{INSERT|REPLACE} INTO t (SELECT ... FROM t ...);
```
例外：如果为FROM子句中更改的表使用子查询，前述限制将不再适用。例如：
```sql
UPDATE t ... WHERE col = (SELECT (SELECT ... FROM t...) AS _t ...);
```
限制在此不适用，这是因为`FROM中`的子查询已被转化为临时表，因此“t”中的相关行已在满足“t”条件的情况下,在更新时被选中。
 
* 仅部分支持行比较操作：
 
  * 对于`expr [NOT] IN (subquery)`，`expr`可以是n-tuple（通过行构造程序语法指定），而且子查询能返回n-tuples个行。可参考        
[row_constructor [NOT] IN table_subquery]()详细语法。
 
  * 对于`expr op {ALL|ANY|SOME} (subquery)`，`expr`必须是标度值，子查询必须是列子查询，不能返回多列行。
 
换句话讲，对于返回n-tuples行的子查询，支持：
 
`(expr_1, ..., expr_n) [NOT] IN ` `table_subquery`
但不支持：
 
`(expr_1, ..., expr_n) op `{ALL|ANY|SOME} `subquery`
支持针对IN的行比较，但不支持针对其他的行比较，原因在于，IN语句的执行是通过将其重新编写为“=”比较和AND操作的序列完成的。该方法 
不能用于ALL、ANY或SOME。
 
* FROM子句的子查询不能被正确的进行关联。因为执行子查询时首先进行实例化查询(预计产生的查询结果），所以并不能对每行的外部查询进行成本评估。对于MySQL5.6.3以前版本，在外部查询前进行实例化查询，对于MySQL5.6.3，优化器至到结果集需要进行实例化查询时，才进行相应的查询，尽量避免实例化查询的使用。
可参考[Section 8.2.1.18.3, “Optimizing Subqueries in the FROM Clause (Derived Tables)”.](./08.02.01_Optimizing_SELECT_Statements.md)
 
* MySQL在有些情况下不支持子查询中的`Limit`用法.
   mysql> `SELECT * FROM t1`
        ->` WHERE s1 IN (SELECT s2 FROM t2 ORDER BY s1 LIMIT 1);`
ERROR 1235 (42000): This version of MySQL doesn't yet support
'LIMIT & IN/ALL/ANY/SOME subquery'

* 与子查询相比，Join（联合）查询执行效率更高，因此，在很多情况下，如果将其改写为join（联合），使用子查询的语句能够更有效地执行。
 
但下述情形例外：`IN`子查询可被改写为`SELECT` `DISTINCT`联合。例如：
```sql
SELECT col FROM t1 WHERE id_col IN (SELECT id_col2 FROM t2 WHERE condition);
```
可将该语句改写为：
```sql
SELECT DISTINCT col FROM t1, t2 WHERE t1.id_col = t2.id_col AND condition;
```
* MySQL支持在子查询中使用存储函数修改数据(如插入数据):
  ```sql
  SELECT ... WHERE x IN (SELECT f() ...);
  ```
  这个选项是MySQL对SQL标准语法的扩展，对于MySQL来说，f()在给定的查询条件下，优化器可能会做出不同的处理，造成f()执行不同的次数，而产生不确定的结果。
 
  对于基于语句复制或者mixed-format 形式的复制形式，可能会在主从服务器上产生不同的结果。
 
* MySQL5.6.3 以前，一个`FROM`子句中的子查询结果会在不使用索引的情况下生成临时表，对于MySQL5.6.3，优化器会使用临时表时，使用索引，从而加快查询执行速度。
 


