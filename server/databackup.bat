cd ..

IF not exist ";C:\Program Files\MySQL\MySQL Server 5.7\bin;" SET PATH=%PATH%;C:\Program Files\MySQL\MySQL Server 5.7\bin

::for /F "delims= %%L in ('echo %PATH% | find ";C:\Program Files"\MySQL\"MySQL Server 5.7"\bin;" /C /I') do (set "VAR=%L")

::echo %delims%
:: str is the same with path

::set str=%str:;C:\vue\project-a32%
:: ";c:\path\to\add" is now removed from str

::setx Path "%str%;c:\path\to\add" -m
:: proceed with setting the path

mysqldump -u root -p cmuhch > cmuhch_backup.sql;

cd server
