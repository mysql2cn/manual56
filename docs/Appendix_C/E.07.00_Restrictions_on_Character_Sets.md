#  E.07.00_字符集中的约束

## E.07.00_字符集中的约束

* `mysql`数据库(`user`, `db`, 等表)中使用`UTF8`(字符集)来存储标识符，标识符只支持在BMP字符中使用，下列字符集不被允许
 
* 使用`ucs2`, `utf16`, `utf16le`, 和 `utf32` 字符集有下列限制：
 
  * 他们不能够在客户端中使用(也就是`SET NAMES` 或者`SET CHARACTER SET` 不会起作用），(可参考[Section 10.1.4, “Connection Character Sets and   Collations”](./10.01.04_Connection_Character_Sets_and_Collations.md))
 
  * 当前的MySQL版本中，不支持在使用`LOAD DATA INFILE` 时，加载这些字符集。
 
  * 不允许在创建全文索引的任何一个列上使用这个字符集，但你可以不使用索引在`IN BOOLEAN MODE` 搜索中使用这些字符集。
 
  * 使用`ENCRYPT()`函数时，不推荐使用这些字符集，因为系统可能因调用零字节而产生异常。
 
* `RegExp[1213]`和`RLIKE[1213]` 操作字符串按单字节进行处理，使用这些多字节字符集可能会产生意想不到的结果。此外，这些操作字符串的函数可能对于一个给定的相等的字符串也会产生不一样的结果。