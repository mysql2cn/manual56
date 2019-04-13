# E.10.06. Window平台限制

## E.10.06. Window平台限制
 
MySQL在Winows 平台下有以下限制
 
* 内存限制

    Windows32位平台下，MySQL单个进程最多使用2GB的内存，这是因为在Windows32平台下，4GB的内存默认为系统内核和用户（程序）各分配2个GB内存。一些版本的Windows通过更改启动参数来修改系统内核使用的内存程序，从而使用较大的内存启动应用程序。也可以使用64位版本的Windows来运行MySQL，不受只能使用最多2GB内存的限制。

* 文件系统别名限制

    数据（数据和索引文件）迁移至RAID或其它地方时，配置frm文件的MySQL的data[432]选项。 

    当使用`MyISAM`表时，在MySQL的data[432]配置文件不能使用别名（Windows快捷方式）的形式。

* 端口限制

    Windows 操作系统大概有4000个端口为客户端连接准备，一个端口关闭到能够重新使用，大概需要2到4分钟。如果客户端连接和断开的动作过快的话，可能很快用光可用端口。即使MySQL正常运行，可能看上去什么反应也没有（假死）。更多信息可以参考：[196271](http://support.microsoft.com/default.aspx?scid=kb;enus;196271.)
 
* 数据文件和索引文件限制
 
    Windows平台下，使用`Create Table`语句创建InnoDB表时，支持数据文件和索引文件分开设置的选项，详细参考可以参考[Section 5.4.1.2, “Specifying the Location of a Tablespace”，](./05.04.01_Managing_InnoDB_Tablespaces.md)对于`MyISAM`表，则忽略据文件和索引文件分开设置的选项(包含其它平台中的非功能性`realpath()`调用。

*  删除数据库限制
  不能删除数据库，若数据库在另一会话中使用。
 
* 大小写敏感的限制

    因为Windows平台对于文件大小写不进行区分，所以MySQL数据库和表的名字忽略大小写的区别，但对于数据库和表的名字，必须使用同样的大小写规则（都是大写或小写），详细内容参考：[See Section 9.2.2, “Identifier Case Sensitivity”.](./09.02.02_Identifier_Case_Sensitivity.md)

* 文件和路径名

    Windows平台下，MySQL只支持与当前系统兼容的ANSI编码方式，如下所示的在日文路径在Western locale ，会产生错误：
    datadir="C:/私たちのプロジェクトのデータ"
    此类限制在SQL语句中有相应的限制，如在`LOAD DATA INFILE` 中的数据文件路径。
 
* 关于"\"路径分隔符的限制

    Windows平台下，路径名以"\"进行分隔，同样MySQL的逃逸急键也是此符号。如果使用`LOAD DATA INFILE` 或者 `SELECT ... INTO OUTFILE`语句的话，需要使用类Unix的路径，如下所示：
```bash
mysql> LOAD DATA INFILE 'C:/tmp/skr.txt' INTO TABLE skr;
mysql> SELECT * INTO OUTFILE 'C:/tmp/skr.txt' FROM skr;
```
当然也可以使用以下方式来进行操作。但“\”必须使用 “\\”代替
```bash
mysql> LOAD DATA INFILE 'C:\\tmp\\skr.txt' INTO TABLE skr;
mysql> SELECT * INTO OUTFILE 'C:\\tmp\\skr.txt' FROM skr;
```
 
* 管道的限制
 
    WIndows平台下，命令行如果包含^Z / CHAR(24),Windows可能认为此文件已经结束，从而不执行后续的命令，并中断程序。并不能很好的工作，使用如下命令进行二进制日志分析时，可能会遇到问题 
```bash
C:\> mysqlbinlog binary_log_file | mysql --user=root
```
    如果遇到错误，并且怀疑是^Z / CHAR(24) 字符引起的，可以使用下列方法解决：

```bash
C:\> mysqlbinlog binary_log_file --result-file=/tmp/bin.sql
C:\> mysql --user=root --execute "source /tmp/bin.sql"
```
    最后一种方法，还适用于任何SQL文件（二进制数据)的可靠读取。
