###  8.7. Optimizing for MEMORY Tables
在频繁访问的非关键表上，考虑使用[MEMORY](#)表，并且是只读或者极少更新。在实际负载下，以对等的[InnoDB](#)或者[MyISAM](#)表作为基准，额外的性能增加是否值得丢失数据的风险，或者是应用程序启动时从磁盘拷贝数据的消耗。

为获得[MEMORY](#)表最好性能，检查每个表的查询类型，并且明确每个相关索引的使用类型，要么B-tree或者hash tree。[CREATE](#) [INDEX](#)语句，使用子句[USING](#) [BTREE](#)或者[USING](#) [HASH](#)。B-tree索引通过比较操作符或者[BETWEEN](#)执行大于或者小于比较查询很快。Hash索引仅通过=操作符执行单列查询很快，或者通过[IN](#)操作符查找有限集。使用[USING](#) [BTREE](#)相比缺省的[USING](#) [HASH](#)更好的选择的原因，查看
[Section 8.2.1.20, "How to Avoid Full Table Scans"][8.2.1.20]。不同[MEMORY](#)索引实现细节，查看[Section 8.3.8, "Comparison of B-Tree and Hash Indexes"][8.3.8]。


[8.2.1.20]: ./docs/Chapter_08/8.2.1_How_to_Avoid_Full_Table_Scans.md#8.2.1.20

[8.3.8]: ./docs/Chapter_08/8.3.8_Comparison_of_B-Tree_and_Hash_Indexes.md

