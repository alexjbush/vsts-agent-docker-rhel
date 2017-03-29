FROM centos:7.2.1511
ENV CENTOS_VERSION=7.2

RUN yum -y install \
       deltarpm \
       epel-release \
       unzip \
       libunwind \
       gettext\
       libcurl-devel \
       openssl-devel \
       zlib \
       libicu-devel \
 && yum -y install \
       jq \
 && yum clean all

WORKDIR /vsts

COPY ./start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
