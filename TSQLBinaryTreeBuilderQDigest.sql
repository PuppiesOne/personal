--QDigest Builder

DECLARE @COUNTER int
DECLARE @COUNTERABC nvarchar(10)
DECLARE @MAXID int
DECLARE @SQL nvarchar(4000)
DECLARE @PARENTNODE nvarchar(10)
DECLARE @MINID int
DECLARE @ASCI int
DECLARE @ASCINEXT  int
DECLARE @CHAR nvarchar(1)
DECLARE @CHARNEXT nvarchar(1)
DECLARE @PARENTCOUNTER int
DECLARE @MAXPARENTID int
DECLARE @SIGMA int
DECLARE @COUNTERFORCOLUMN int
DECLARE @MAXTC int
DECLARE @MAXTCABC nvarchar(10)

SET @PARENTCOUNTER = 0
SET @SIGMA = (select       substring(
                                                              Tuple,charindex(
                                                                                         ',',Tuple
                                                                                         ) + 1, 10
                                                              )
                                         FROM [dbo].[United_QDigest_T]
                                         WHERE [TC] = 0)
SET @MAXPARENTID = log(@SIGMA,2)
SET @ASCI = 64 -- The value right before A 
SET @ASCINEXT = @ASCI + 1
SET @CHAR = (select char(@ASCI))
SET @CHARNEXT = (select char(@ASCINEXT))

WHILE @PARENTCOUNTER < @MAXPARENTID

       BEGIN

                     SET @PARENTCOUNTER = @PARENTCOUNTER + 1
                     SET @ASCI = @ASCINEXT --Cycles to A first, then through ASCI characters
                     SET @ASCINEXT = @ASCINEXT + 1 --Cycles to B first, then through ASCI characters
                     SET @CHAR = (select char(@ASCI))
                     SET @CHARNEXT = (select char(@ASCINEXT))
                     
                     --IF @CHAR = 'A' SET @MAXID = (select cast(count(*) as int) + 1 FROM [dbo].[United_QDigest_T] WHERE Substring([Node],1,1) = @CHAR) ELSE
                     SET @MAXID = (select cast(count(*) as int) FROM [dbo].[United_QDigest_T] WHERE Substring([Node],1,1) = @CHAR)
                     SET @COUNTER = 0
                     SET @COUNTERFORCOLUMN = 0

                     WHILE @COUNTER < @MAXID 

                     BEGIN
                           
                           SET @COUNTER = @COUNTER + 1
                           SET @COUNTERABC = @COUNTER
                           SET @PARENTNODE = @CHAR + @COUNTERABC
                           SET @COUNTERFORCOLUMN = @COUNTERFORCOLUMN + 1
                           SET @COUNTERABC = @COUNTERFORCOLUMN
                           SET @MAXTC = (select max([TC]) FROM [dbo].[United_QDigest_T])
                           SET @MAXTC = @MAXTC + 1
                           SET @MAXTCABC = @MAXTC

                           SET @SQL = '
                           INSERT INTO [dbo].[United_QDigest_T]
                           select '''+@MAXTCABC+'''
                                                       ,cast(
                                                                                  Min(
                                                                                         substring(
                                                                                                       Tuple,1,charindex(
                                                                                                                                  '','',Tuple
                                                                                                                                         ) - 1
                                                                                                       )
                                                                                         )
                                                                                         as nvarchar(6)
                                                                                  ) 
                                                                                         + '','' + 
                                                       cast(
                                                                                         (Max(
                                                                                                substring(
                                                                                                              Tuple,1,charindex(
                                                                                                                                  '','',Tuple
                                                                                                                                         ) - 1
                                                                                                              )
                                                                                                ) / 2
                                                                                         )
                                                                                         +
                                                                                         (Min(
                                                                                                substring(
                                                                                                              Tuple,charindex(
                                                                                                                                         '','',Tuple
                                                                                                                                                ) + 1, 10
                                                                                                              )
                                                                                                ) / 2
                                                                                         ) - 1

                                                              as nvarchar(6)
                                                              )      
                                                              AS ''Tuple''
                           , [Node] = '''+@CHARNEXT+''' + ''' + @COUNTERABC + '''
                           , [Parent Node] = '''+@PARENTNODE+'''
                           , 0
                           FROM [dbo].[United_QDigest_T]
                           WHERE [Node] = '''+@PARENTNODE+'''
                           'exec(@sql)

                           SET @COUNTERFORCOLUMN = @COUNTERFORCOLUMN + 1
                           SET @COUNTERABC = @COUNTERFORCOLUMN
                           SET @MAXTC = (select max([TC]) FROM [dbo].[United_QDigest_T])
                           SET @MAXTC = @MAXTC + 1
                           SET @MAXTCABC = @MAXTC

                           SET @SQL = '
                           INSERT INTO [dbo].[United_QDigest_T]
                           select '''+@MAXTCABC+'''
                                         ,cast(
                                                       (Max(
                                                              substring(
                                                                           Tuple,1,charindex(
                                                                                                '','',Tuple
                                                                                                       ) - 1
                                                                           )
                                                              ) / 2
                                                       )
                                                       +
                                                      (Min(
                                                              substring(
                                                                           Tuple,charindex(
                                                                                                       '','',Tuple
                                                                                                              ) + 1, 10
                                                                           )
                                                              ) / 2
                                                       )
                           as nvarchar(6)
                           ) 
                                         + '','' + 
                                         cast(
                                                Max(
                                                       substring(
                                                                     Tuple,charindex(
                                                                                                '','',Tuple
                                                                                                       ) + 1, 10
                                                                     )
                                                       )
                                                       as nvarchar(6)
                                                ) 
                           AS ''Tuple''
                           , [Node] = '''+@CHARNEXT+''' + ''' + @COUNTERABC + '''
                           , [Parent Node] = '''+@PARENTNODE+'''
                           , 0
                           FROM [dbo].[United_QDigest_T]
                           WHERE [Node] = '''+@PARENTNODE+'''
                           'exec(@sql)

                     END

       END
