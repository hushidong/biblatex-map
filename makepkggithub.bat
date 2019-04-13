title %date% %time% make-pkg-github

cd ..

mkdir bibmap

cd bibmap

mkdir test

cd ..

copy biblatex-map-master\*.* bibmap\*.* /Y

copy biblatex-map-master\test\*.* bibmap\test\*.* /Y

cd bibmap

call makeclear

cd ..

zip.exe -r -q -v bibmap-github.zip bibmap

pause