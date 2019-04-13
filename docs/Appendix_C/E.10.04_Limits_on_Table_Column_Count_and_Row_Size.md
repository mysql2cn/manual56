#  E.10.04_表中列数量和大小的限制

## E.10.04_表中列数量和大小的限制

每个表最多4096列，但有效列可能会受到下列因素的影响：

* 每张表中行最大值为65,535 bytes（与数据库引擎无关），数据库引擎可能会有另外的信息存储，影响了最大行的大小。

 * 最大行值受制于列的总长度，如对于`CHAR(255) CHARACTER` (在`UTF8`编码下的固定长度字符串)所在列,一个字符串需要3byte 来表示，则服务器必须为每个列值分配255 *3 = 765 bytes 的空间，由此推算出一个表最多有 65,535/765=85列。

 * 存储可变长的字符串 (在`UTF8`编码下的 变长字符串，其中包括存储列长度的bytes)，使用两个字节存储列的长度，则每列长度可达到767 bytes.
 * BLOB和TEXT列，需要2、4甚至8字节来存储信息，因为他们的内容在其它行中进行分开存储。

 * 列值设定为`NULL`，会减少列的最大数目。对于`MyISAM`表来说，`NULL`列还需要额外的信息来存储`NULL`的值，行最大长度可以采取下列方式计算：
```bash		
row length = 1 
\+ (sum of column lengths)
\+ (number of NULL columns + delete_flag + 7)/8
\+ (number of variable-length columns)
```
此标志存储在动态行的行头部,在动态行中，`delete_flag`值为0，静态表使用一个比特(a bit)在行中记录行是否已经删除，`delete_flag`在静态行的值为1，更多信息参考 [Section 14.3.3, “MyISAM Table Storage Formats”.](./14.03.03_MyISAM_Table_Storage_Formats.md)  

 * 对于`InnoDB`表来讲，`NULL`与 `NOT NULL`列值一样，计算公式不适用。
 
 * 下列语句能够创建表1成功，是因为 32,765 + 2bytes 和 32,766 + 2bytes, 都未超过行最大值 65,535 bytes。
 ```sql
mysql> CREATE TABLE t1
-> (c1 VARCHAR(32765) NOT NULL, c2 VARCHAR(32766) NOT NULL)
-> ENGINE = MyISAM CHARACTER SET latin1;
```
Query OK, 0 rows affected (0.02 sec)
下列语句能够创建表2失败，是因为在`MyISA`M中，`NULL`值需要另外的空间进行存储, 已超过行最大值 65,535 bytes。
 ```sql
mysql> CREATE TABLE t2
-> (c1 VARCHAR(32765) NULL, c2 VARCHAR(32766) NULL)
-> ENGINE = MyISAM CHARACTER SET latin1;
```sql
ERROR 1118 (42000): Row size too large. The maximum row size for the
used table type, not counting BLOBs, is 65535. You have to change some
columns to TEXT or BLOBs
下列语句能够创建表3失败，因为存储可变长列字符串时，需要另外2个字节的空间记录列长度信息。已超过行最大值 65,535 bytes。
```sql
mysql> CREATE TABLE t3
-> (c1 VARCHAR(65535) NOT NULL)
-> ENGINE = MyISAM CHARACTER SET latin1;
```
ERROR 1118 (42000): Row size too large. The maximum row size for the
used table type, not counting BLOBs, is 65535. You have to change some
columns to TEXT or BLOBs
 
* 不同的数据库引擎可能会对列的数量有不同的影响 

    * `InnoDB` 最大可达到1000列。
    * `InnoDB` 限制行值最大值为数据库页值的一半（接近8000bytes),并不包含`VARBINARY`, `VARCHAR`, `BLOB`, 或者 `TEXT` 列。       
    * 不同的InnoDB数据库存储格式（COMPRESSED, REDUNDANT）使用不同的页首和页尾数据格式，从而影响可用行的数量。
    * 每张表包含一个.frm文件格式来确定表的结构，此文件内容同样影响每个表的行数，更多信息参考：[Section E.10.5, “Limits Imposed by .frm File Structure”.](./E.10.05_Limits_Imposed_by_.frm_File_Structure.md)
