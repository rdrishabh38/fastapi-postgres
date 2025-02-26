#FROM fluent/fluentd:v1.12.0-debian-1.0
#
#USER root
#
### Install faraday-net_http version 3.0.2 first
##RUN gem install faraday -v 2.8.1
#
### Remove any default fluent-plugin-elasticsearch if present.
##RUN gem uninstall fluent-plugin-elasticsearch -a -x || true
##
### Now install fluent-plugin-elasticsearch version 5.0.3
##RUN gem install fluent-plugin-elasticsearch -v 5.0.3
#
#RUN gem uninstall -I elasticsearch && gem install elasticsearch -v 7.17.0
#
#RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document", "--version", "5.0.3"]
#
#USER fluent


#FROM fluent/fluentd:v1.16-debian-2
#
#USER root
#RUN gem install fluent-plugin-elasticsearch
#USER fluent


FROM fluent/fluentd:edge-debian
USER root
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document", "--version", "5.4.3"]
USER fluent