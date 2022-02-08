title %date% %time% make-pkg-github

cd ..

mkdir bibmap

cd bibmap

mkdir backendtest

mkdir backendtesttabbib

mkdir mapbibtest

mkdir binary

mkdir bibfiles

cd ..

copy biblatex-map-master\*.* bibmap\*.* /Y

copy biblatex-map-master\backendtest\*.* bibmap\backendtest\*.* /Y

copy biblatex-map-master\backendtesttabbib\*.* bibmap\backendtesttabbib\*.* /Y

copy biblatex-map-master\mapbibtest\*.* bibmap\mapbibtest\*.* /Y

copy biblatex-map-master\binary\*.* bibmap\binary\*.* /Y

copy biblatex-map-master\bibfiles\*.* bibmap\bibfiles\*.* /Y

cd bibmap

call makeclear

cd ..

zip.exe -r -q -v bibmap-github.zip bibmap

pause