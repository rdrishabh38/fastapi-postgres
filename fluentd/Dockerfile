FROM fluent/fluentd:v1.12.0-debian-1.0

USER root

# Remove any default fluent-plugin-elasticsearch if present.
RUN gem uninstall fluent-plugin-elasticsearch -a -x || true

# Install the compatible version of fluent-plugin-elasticsearch.
RUN gem install fluent-plugin-elasticsearch -v 5.0.3

USER fluent
