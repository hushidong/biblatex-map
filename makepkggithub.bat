title %date% %time% make-pkg-github

cd ..

mkdir bibmap

cd bibmap

mkdir backendtest

mkdir backendtest-tabbib

mkdir backendtest-lanparal

mkdir mapbibtest

mkdir mapbibtest-addpinyinkey

mkdir mapbibtest-authoran

mkdir mapbibtest-tobibtex

mkdir mapbibtest-casetransfer

mkdir binary

mkdir bibfiles

cd ..

copy biblatex-map-master\*.* bibmap\*.* /Y

copy biblatex-map-master\backendtest\*.* bibmap\backendtest\*.* /Y

copy biblatex-map-master\backendtest-tabbib\*.* bibmap\backendtest-tabbib\*.* /Y

copy biblatex-map-master\backendtest-lanparal\*.* bibmap\backendtest-lanparal\*.* /Y

copy biblatex-map-master\mapbibtest\*.* bibmap\mapbibtest\*.* /Y

copy biblatex-map-master\mapbibtest-addpinyinkey\*.* bibmap\mapbibtest-addpinyinkey\*.* /Y

copy biblatex-map-master\mapbibtest-authoran\*.* bibmap\mapbibtest-authoran\*.* /Y

copy biblatex-map-master\mapbibtest-tobibtex\*.* bibmap\mapbibtest-tobibtex\*.* /Y

copy biblatex-map-master\mapbibtest-casetransfer\*.* bibmap\mapbibtest-casetransfer\*.* /Y


copy biblatex-map-master\binary\*.* bibmap\binary\*.* /Y

copy biblatex-map-master\bibfiles\*.* bibmap\bibfiles\*.* /Y

cd bibmap

call makeclear

cd ..

zip.exe -r -q -v bibmap-github.zip bibmap

pause