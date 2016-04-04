FROM ubuntu

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get clean

RUN apt-get install git autoconf libtool make -y

RUN apt-get update -y && apt-get upgrade -y

RUN git clone https://github.com/balabit/eventlog && cd eventlog && libtoolize --force && aclocal && autoheader && automake --force-missing --add-missing && autoconf && ./configure &&  make install

RUN apt-get install checkinstall -y

RUN cd eventlog && checkinstall --pkgversion=0.2.13 -y

