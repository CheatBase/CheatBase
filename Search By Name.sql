select *
from ROMs
where romFileName like '%Blue Dragon%.nds';

select *
from ROMs
where romID = 73709;

select *
from ROMs
where romSerial like 'BBU%'

select *
from CHEATS
where romID in (select romID from ROMs where romFileName like '%HeartGold%')
