select *
from ROMs
where romFileName like '%Castlevania%.nds';

select *
from RELEASES
where releaseTitleName like '%Black Ops%';

select *
from ROMs
where romID = 74352;

select *
from ROMs
where romSerial like 'BDY%';

select * from ROMs where systemID = 1;

select *
from CHEATS
where romID in (select romID from ROMs where romFileName like '%HeartGold%');
