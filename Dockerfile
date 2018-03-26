FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
python3-numpy python3-scipy python3-matplotlib python3-pandas

RUN apt-get update && apt-get install -y \
curl apt-utils apt-transport-https debconf-utils gcc build-essential unixodbc-dev\
&& rm -rf /var/lib/apt/lists/*

# python libraries
RUN apt-get update && apt-get install -y \
python3-pip python3-dev python3-setuptools \
--no-install-recommends \
&& rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pyodbc peakutils

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/14.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql 

# install SQL Server tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8     
# install necessary locales
RUN apt-get update && apt-get install -y locales \
&& echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
&& locale-gen en_US.UTF-8
RUN dpkg-reconfigure locales

#install Kusto
RUN python3 -m pip install azure==2.0.0rc6 
RUN python3 -m pip install http://52.173.187.55/simple/kusto_client-0.4.0-py2.py3-none-any.whl
RUN python3 -m pip install http://52.173.187.55/simple/kusto_ingest_client-0.3.3-py2.py3-none-any.whl

RUN apt-get update
RUN mkdir /home/PerfDetect
ADD ./PerfDetect /home/PerfDetect

RUN mkdir /home/PerfDetect/log

