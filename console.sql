select *
from ROMs
where romFileName like '%Cars - %.nds';

select *
from RELEASES
where releaseTitleName like '%Black Ops%';

select *
from ROMs
where romID = 86150;

select *
from ROMs
where romSerial like 'BDY%';

select * from ROMs where systemID = 1;

select *
from CHEATS
where romID in (select romID from ROMs where romFileName like '%HeartGold%');

insert into ROMs
(systemID, regionID, romHashCRC, romHashMD5, romHashSHA1, romSize, romFileName, romExtensionlessFileName, romSerial, romLanguage, romDumpSource) values
/*(24,4,'CDF33AD4','58DDFF08BA51075CAF7556EDB7DD5B3B','C9A6F28D3C356810A8D2DF48C540A48A0B80263D',67108864,'007 - Blood Stone (Canada).nds','007 - Blood Stone (Canada)','BJBX','French','No-Intro'),*/
(24,4,'9731CA72','77F6A9EE5FB0E8C21B74B4A51E1557B7','7EA1FDFE27EBB5C322BE620EB0938FA6E5AB07C1',67108864,'Call of Duty - Black Ops (Canada).nds','Call of Duty - Black Ops (Canada)','BDYX','French','No-Intro');

insert into RELEASES
(romID, releaseTitleName, regionLocalizedID) values
/*(86150,'007: Blood Stone',4),*/
(86151,'Call of Duty: Black Ops',4);
