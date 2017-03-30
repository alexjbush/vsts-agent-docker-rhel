FROM bushnoh/vsts-agent-docker-rhel:centos-7.2-docker-1.13.1-standard

RUN curl -L  -H 'Cookie:oraclelicense=accept-securebackup-cookie' \
         -o jdk-linux-x64.rpm \
         http://download.oracle.com/otn-pub/java/jdk/8u60-b27/jdk-8u60-linux-x64.rpm \
 && yum -y install jdk-linux-x64.rpm \
 && rm -rf jdk-linux-x64.rpm \
 && alternatives --set java /usr/java/jdk1.8.0_60/jre/bin/java
 
# Configure environment variables
ENV JAVA_HOME=/usr/java/jdk1.8.0_60
