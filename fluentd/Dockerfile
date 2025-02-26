FROM fluent/fluentd:v1.14.2-debian-1

USER root

## Install faraday-net_http version 3.0.2 first
#RUN gem install faraday -v 2.8.1

# Remove any default fluent-plugin-elasticsearch if present.
RUN gem uninstall fluent-plugin-elasticsearch -a -x || true

# Now install fluent-plugin-elasticsearch version 5.0.3
RUN gem install fluent-plugin-elasticsearch -v 5.0.3

USER fluent
