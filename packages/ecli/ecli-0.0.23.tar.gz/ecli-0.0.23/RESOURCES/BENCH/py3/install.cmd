#!/bin/sh

##!/bin/bash --posix  is same as #!/bin/sh
##!/bin/bash

apt remove python3
apt purge python3
## rpm -qa | egrep python | xargs rpm -ev --allmatches --nodeps
whereis python3
rm /usr/bin/python3
rm /usr/bin/python3.6
rm /usr/bin/python3.6m
rm /usr/bin/pdb3.6
rm /usr/bin/python3m
rm -r /usr/lib/python3
rm -r /usr/lib/python3.6
rm -r /usr/local/lib/python3.6
rm -r /usr/share/python3
rm -r /usr/share/man/man1/python3.1.gz
rm -r /etc/python3.6
which python3

whereis pip3
#rm cooperate pip
#.....
which pip3



wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
tar -zxf Python-3.8.2.tgz
mkdir 382
mv Python-3.8.2 382
rm Python-3.8.2.tgz
cd 382
cd Python-3.8.2.tgz
apt install zlib1g-dev
apt install libffi-dev
apt install libssl-dev
apt install openssl-devel
./configure --help > help.log
cat help.log | egrep with | egrep ssl
./configure --with-ssl-default-suites=openssl --enable-optimizations
make
make install

whereis python3

ln -s /usr/local/bin/python3 /usr/bin/python3
ln -s /usr/local/bin/python3.8 /usr/bin/python3.8
ln -s /usr/local/bin/python3.8 /usr/bin/python382 

which python3

whereis pip3

ln -s /usr/local/bin/pip3      /usr/bin/pip3
ln -s /usr/local/bin/pip3.8    /usr/bin/pip3.8
ln -s /usr/local/bin/pip3.8    /usr/bin/pip382

which pip3

apt install libreadline-dev 
apt install libncurses5-dev
apt install patch
apt install swig
