FROM odoo:17.0
LABEL Aashim Bajracharya. <ashimbazracharya@gmail.com>

USER root
RUN mkdir -p /mnt/custom
RUN apt-get update \
    && apt-get install
RUN chown -R odoo /mnt
RUN chown -R odoo /mnt/*
RUN pip3 install --upgrade pip

