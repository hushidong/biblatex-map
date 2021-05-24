title %date% %time% make-pkg-github

cd ..

mkdir bibmap

cd bibmap

mkdir test

mkdir example

mkdir binary

cd ..

copy biblatex-map-master\*.* bibmap\*.* /Y

copy biblatex-map-master\test\*.* bibmap\test\*.* /Y

copy biblatex-map-master\example\*.* bibmap\example\*.* /Y

copy biblatex-map-master\binary\*.* bibmap\binary\*.* /Y

cd bibmap

call makeclear

cd ..

zip.exe -r -q -v bibmap-github.zip bibmap

pause