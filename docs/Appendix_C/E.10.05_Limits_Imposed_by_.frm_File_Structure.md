#  E.10.05_ frm 文件的限制

## E.10.05_ frm 文件的限制

每张表使用`frm`来定义表结构，服务器使用下列公式来计算表的信息大小（不能超过64KB），超过64KB时，无法添加更多的列。

```bash
if (info_length+(ulong) create_fields.elements*FCOMP+288+
n_length+int_length+com_length > 65535L || int_count > 255)
```

* `info_length` is space needed for “screens.” This is related to MySQL's [Unireg](http://twpug.net/docs/mysql323/manual_Unireg.html) heritage.

* `create_fields.elements`列的数量.

* `FCOMP` 值为17.

*  `n_length` is the total length of all column names, including one byte per name as a separator.（列的名字总长度）？
* `int_length` 是指ENUM和SET的值，“int”非整数的意思，而是间隔。

* `int_count` 是指`ENUM`和`SET` 具有独立（特征）的值（见计算公式前提条件）

*  `com_length` 是指列注释的总长度

计算公式有一些前提条件如下所述：

* 使用长的列名会减少列的最大数量（包含ENUM和SET 的值） 
* `ENUM`和`SET`的值在表中不会超过255个，若定义相同则视为同一列，如下表定义所示：
```sql
e1 ENUM('a','b','c')
e2 ENUM('a','b','c')
```
* 表的信息大小（不能超过64KB），理论上`ENUM`列数量会为65,535，实际上会少于3000。
