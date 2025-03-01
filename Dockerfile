FROM oraclelinux:7
WORKDIR /app
# Define variables for Oracle Instant Client
ARG release=19
ARG update=10
# Install Development Tools and Dependencies for cx-Oracle
RUN yum -y update && \
    yum groups mark convert && \
    yum -y groupinstall "Development Tools" && \
    yum -y install gcc gcc-c++ libaio-devel python3-devel make
# Enable repo & install Oracle Instant Client
RUN yum clean all && yum makecache fast && \
    yum -y install oracle-release-el7 && yum-config-manager --enable ol7_oracle_instantclient && \
    yum -y install oracle-instantclient${release}.${update}-basic oracle-instantclient${release}.${update}-devel oracle-instantclient${release}.${update}-sqlplus && \
    rm -rf /var/cache/yum
# Install Python 3.6
RUN yum install -y oracle-softwarecollection-release-el7 && \
    yum-config-manager --enable ol7_latest ol7_optional_latest && \
    yum install -y scl-utils rh-python36 && \
    ln -sf /opt/rh/rh-python36/root/usr/bin/python3.6 /usr/bin/python3 && \
    ln -sf /opt/rh/rh-python36/root/usr/bin/pip3 /usr/bin/pip3
# Add Instant Client to path
ENV PATH=$PATH:/usr/lib/oracle/${release}.${update}/client64/bin
ENV TNS_ADMIN=/usr/lib/oracle/${release}.${update}/client64/lib/network/admin
# Ensure wallet directory exists and copy wallet files
RUN mkdir -p /usr/lib/oracle/${release}.${update}/client64/lib/network/admin
ADD ./wallet/* /usr/lib/oracle/${release}.${update}/client64/lib/network/admin/
# Copy application files
COPY ./requirements.txt /app/requirements.txt
COPY ./app.py ./config.py ./forms.py ./models.py ./Procfile ./README /app/
COPY ./static /app/static
COPY ./templates /app/templates
# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
# Expose app port
EXPOSE 8080
# Start application
CMD ["gunicorn", "app:app", "--config=config.py", "--bind", "0.0.0.0:8080"]
