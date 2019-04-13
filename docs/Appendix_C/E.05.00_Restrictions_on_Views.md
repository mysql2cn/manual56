#  E.05.00_视图中约束

## E.05.00_视图中约束

视图处理功能未优化：

* 不能在视图上创建索引。
* 对于使用MERGE算法处理的视图，可以使用索引。但是，对于使用临时表算法处理的视图，不能在其基表上利用索引提供的优点（尽管能够在临时表的生成过程中使用索引）。
 
基本的原则是，读者无法从表自身的子查询中修改自身表，可参考[Section E.4, “Restrictions on Subqueries”.](/E.04.00_Restrictions_on_Subqueries.md)
 
如果从表选择了视图并接着从视图进行了选择，同样的原则也适用，如果在子查询中从表选择了视图并使用MERGE算法评估了视图，也同样。例如：
```sql
CREATE VIEW v1 AS
SELECT * FROM t2 WHERE EXISTS (SELECT 1 FROM t1 WHERE t1.a = t2.a);
UPDATE t1, v2 SET t1.a = 1 WHERE t1.b = v2.b;
```
如果视图是使用临时表评估的，可从视图子查询中的表进行选择，并仍能更改外部查询中的表。在该情况下，视图将被具体化，因此，你实际上不能从子查询的表中进行选择并“同时”更改它（这是你打算强制MySQL使用临时表算法的另一原因，其方法是在视图定义中指定`ALGORITHM = TEMPTABLE`关键字）。

读者可以使用`DROP TABLE`或`ALTER TABLE`来删除或更改视图定义中使用的表（它会使视图失效），而且删除或更改操作不会导致告警。但在以后使用视图时会出错。

视图定义可某些情况下，可能会被冻结：
  如果视图定义中使用了PREPARE，在语句执行后，视图便会固定下来，即使你后来更改了视图的定义。如下所示：
```sql
CREATE VIEW v AS SELECT RAND();
PREPARE s FROM 'SELECT * FROM v';
ALTER VIEW v AS SELECT NOW();
EXECUTE s;
```
语句执行的结果是一个随机数，而不是当前的日期和时间。

对于视图的更新性来讲，理想的目标是任何视图都能够更新，同样包括`UNION`语句的视图，当前理论上并不是所有视图能够更新。视图产生的最初目的是让MySQL更新的尽可能的快。大部分视图在理论上已经能够更新，但还存在部分限制：

 * 其子查询位于WHERE子句之外任何位置的可更新视图。对于某些其子查询位于SELECT列表中的视图，也是可更新的。
 * 不能使用UPDATE来更新定义为Join的视图的1个以上的基表。
 * 不能使用DELETE来更新定义为Join的视图。
 
视图创建完成后也存在一些问题，如果一个用户被授权了创建视图的最低权限(`CREATE VIEW[774]` 和 `SELECT[775]`权限),但(被授权的)用户对当前的对象(表、视图等)无法使用`SHOW CREATE VIEW` ，除非(被授权的)用户被授权为 `SHOW VIEW[775]`权限。
 
此问题会导致使用`mysqldump`备份数据库时失败，此问题在Bug#22062已经提到过。
 
解决此问题的方法是管理员手动为用户授于`SHOW VIEW[775]`权限(已经拥有`CREATE VIEW[774]`权限)，MySQL老的版本在视图创建时默认不会进行此权限的赋予。
 
视图处理中，无索引，也就是说处理视图时，无法使用索引。
 
在`SHOW CREATE VIEW` 子句中使用 `AS alias_name clause` 查看视图列定义时，若列创建时使用了表达式，默认别名(alias)会是Text内容，可能会变的很长。使用 `CREATE VIEW`语句创建列别名时，数据库会检查列别名是否超过了64个字符的最大长度(not the maximum alias length of 256 characters). 如果创建列别名超过64个字符，则在使用`SHOW CREATE VIEW` 输出出列别名时出现以下问题：

   * 视图定义无法复制到新的从库上。
   * 复制的数据库文件在使用`mysqldump`无法加载。
 
解决此问题的办法是修改每个存在问题的视图（使用较短长度的列别名),从而视图能够复制到新的从库，无错误的复制或重新加载数据库文件。修改列别名，可以使用 `DROP VIEW`、`CREATE VIEW` 或者 使用 `CREATE` OR `REPLACE VIEW`替换相应的列别名定义。
