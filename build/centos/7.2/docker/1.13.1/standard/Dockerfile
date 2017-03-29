FROM bushnoh/vsts-agent-docker-rhel:centos-7.2-docker-1.13.1

# Install packages
RUN yum -y groupinstall 'Development Tools'
RUN yum install -y \
    # Basic utilities
    curl \
    bind-utils \
    net-tools \
    ftp \
    iproute \
    iputils \
    openssh-clients \
    sudo \
    telnet \
    time \
    unzip \
    wget \
    zip \
    # Python
    python \
    python34 \
    # Java and related build tools
    java-1.8.0-openjdk \
    ant \
    ant-contrib \
    maven \
    curl-devel \
    expat-devel \
    gettext-devel \
    openssl-devel \
    zlib-devel \
    perl-ExtUtils-MakeMaker \
 && yum clean all

RUN wget https://services.gradle.org/distributions/gradle-2.4-all.zip -O /tmp/gradle-2.4-all.zip \
 && mkdir -p /opt/gradle/2.4 \
 && unzip /tmp/gradle-2.4-all.zip -d /tmp \
 && mv /tmp/gradle-2.4/* /opt/gradle/2.4/ \
 && ln -s /opt/gradle/2.4/ /opt/gradle/current \
 && rm -rf /tmp/gradle-2.4-all.zip \
 && rm -rf /tmp/gradle-2.4/

RUN curl -sL https://git.io/n-install | bash -s -- -ny - \
 && ~/n/bin/n stable \
 && npm install -g bower grunt gulp n \
 && rm -rf ~/n

RUN curl -sSL -o dotnet.tar.gz https://go.microsoft.com/fwlink/?linkid=843449 \
 && mkdir -p /opt/dotnet \
 && tar zxf dotnet.tar.gz -C /opt/dotnet \
 && ln -s /opt/dotnet/dotnet /usr/local/bin \
 && rm -rf dotnet.tar.gz

RUN wget https://www.kernel.org/pub/software/scm/git/git-2.12.2.tar.gz \
         -O /tmp/git-2.12.2.tar.gz \
 && cd /tmp/ \
 && tar xzf git-2.12.2.tar.gz \
 && cd /tmp/git-2.12.2 \
 && make prefix=/usr/local/git all \
 && make prefix=/usr/local/git install \
 && rm -rf /tmp/git-2.12.2.tar.gz /tmp/git-2.12.2

# Configure environment variables
ENV ANT_HOME=/usr/share/ant \
    bower=/usr/local/bin/bower \
    dotnet=/usr/bin/dotnet \
    GRADLE_HOME=/opt/gradle/current \
    PATH=/usr/local/git/bin:$PATH:$GRADLE_HOME/bin \
    grunt=/usr/local/bin/grunt \
    JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk \
    M2_HOME=/usr/share/maven \
