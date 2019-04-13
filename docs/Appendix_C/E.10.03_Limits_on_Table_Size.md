# Limits_on_Table_Size


MySQL数据库的最大有效表尺寸通常是由操作系统对文件大小的限制决定的，而不是由MySQL内部限制决定的。在下面的表格中，列出了一些关于操作系统文件大小限制的示例。这仅是初步指南，并不是最终的。要想了解最新信息，请参阅关于操作系统的文档。
<table border="1" cellpadding="0" id="table1">
				<tr>
					<td>操作系统</td>
					<td>文件大小限制</td>
				</tr>
					<td>win32 w/ FAT/FAT32</td>
					<td>2GB/4GB</td>
				</tr>
					<td>win32 w/ NTFS</td>
					<td>2TB（可能更大）</td>
				</tr>
				<tr>
					<td>Linux 2.2-Intel32-bit</td>
					<td>2GB (LFS: 4GB)</td>
				</tr>
				<tr>
					<td>Linux 2.4+</td>
					<td>(using ext3 filesystem) 4TB</td>
				</tr>
				<tr>
					<td>Solaris 9/10</td>
					<td>16TB</td>
				</tr>
				<tr>
					<td>MacOS X w/ HFS+</td>
					<td>2TB/td>
				</tr>
			</table>
 
Windows用户请注意： FAT和VFAT (FAT32)不适合MySQL的生产环境中使用。应使用NTFS代替。 
 
在Linux 2.2平台下，通过使用对ext2文件系统的大文件支持（LFS）补丁，可以获得超过2GB的`MyISAM`表。在Linux 2.4平台下，存在针对ReiserFS的补丁，可支持大文件（高达2TB）。目前发布的大多数Linux版本均基于2.4内核，包含所有所需的LFS补丁。使用JFS和XFS，petabyte（千兆兆）和更大的文件也能在Linux上实现。然而，最大可用的文件容量仍取决于多项因素，其中之一就是用于存储MySQL表的文件系统。
 
 关于Linux中LFS的详细介绍，请参见Andreas Jaeger的“[Linux中的大文件支持”页面](http://www.suse.de/~aj/linux_lfs.html)。
 
 如果遇到表空间已满的错误，可能是以下原因引起的 
 
  * 磁盘空间已经满了
  * InnoDB存储引擎将InnoDB表保存在一个表空间内，该表空间可由数个文件创建。这样，表的大小就能超过单独文件的最大容量。表空间可包括原始磁盘分区，从而使得很大的表成为可能。表空间的最大容量为64TB。
  
    如果InnoDB表空间已经过完时，可以扩展InnoDB表空间，可参考[14.2.2.2, “Adding, Removing, or Resizing
InnoDB Data and Log Files](./14.02.02_Administering_InnoDB.md)

  * 在操作系统支持的最大文件（数据文件或索引文件）为2GB上使用`MyISAM`表。
   
  * `MyISAM`表默认情况下可达到246TB（数据和索引文件），如果正在使用`MyISAM`表和表所需的空间超过了所允许的内部指针的大小,可以通过修改指针达到65536TB。

  * `MyISAM`表默认可以支持256TB，通过`CREATE TABLE` 语句中设置`AVG_ROW_LENGTH` and `MAX_ROWS` 选项来修改表的默认大小限制，如果默认的表指针太小，可修改表指针来修改表大小，详细语法可参考[13.1.17, “CREATE TABLE Syntax”.](./13.01.07_ALTER_TABLE_Syntax.md) 
```aql
ALTER TABLE tbl_name MAX_ROWS=1000000000 AVG_ROW_LENGTH=nnn;
```
当列值类型为`BLOB` 或者 `TEXT`类型时，你必须指定`AVG_ROW_LENGTH`，在以上的例子中，MySQL不会优化数据库空间。

 
    为了改变MyISAM默认表尺寸限制，若未指定`MAX_ROWS` 选项值，可设置`myisam_data_pointer_size[525]` ，来改变默认表尺寸，`myisam_data_pointer_size[525]` 值可为2到7，值为2时，默认表为最大为4GB，当值为7时，默认表可达到256TB。
 
 读者使用以下语句检查数据文件和索引文件的大小：
```sql				
SHOW TABLE STATUS FROM db_name LIKE 'tbl_name';
``` 
  读者同时也可以使用 `myisamchk -dv /path/to/table-index-file.` 参考 [Section 13.7.5, “SHOW Syntax”,](./13.07.05_SHOW_Syntax.md) 或者 [Section 4.6.3, “myisamchk — MyISAM Table-Maintenance Utility”.](./04.06.03_myisamchk_MyISAM_Table-Maintenance_Utility.md)
 
  还有很多处理MyISAM表的方法，如下所说：
 
    * 如果大尺寸表以只读方式存在的话，可以使用`myisampack`对表进行压缩，至少减少压缩为表的一半大小，实际上，对于更大的表，`myisampack` 可以将多个表合并成一个表，可参考[Section 4.6.5, “myisampack — Generate Compressed, Read-Only MyISAM Tables”.](./04.06.05_myisampack_Generate_Compressed_Read-Only_MyISAM_Tables.md)
   
    * MySQL文件中，包含一个MERGE库文件，能够处理许多同样表结构的表当作一个MERGE表进行处理，可参考 [Section 14.8, “The MERGE Storage Engine”.](./14.08.00_The_MERGE_Storage_Engine.md)
   
 * 读者可以使用`MERGE（HEAP）`数据库引擎，但需要更改`max_heap_table_size [519]` 系纺变量。可参考 [Section 5.1.4, “Server System Variables”.](./05.01.04_Server_System_Variables.md)
