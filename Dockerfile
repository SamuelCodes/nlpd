FROM ubuntu:trusty

# Set the default locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install dependencies for text analysis
RUN apt-get update && apt-get install -y locales python-pip ipython python-dev curl
RUN pip install pymongo numpy pattern

# Create application directories
RUN mkdir -p /app/data
WORKDIR /app
ADD app/ /app

# Add our binaries to the path
ENV "PATH=/app/bin:$PATH"

# Export the data volume
VOLUME /app/data

# Expose language services on port 8000
EXPOSE 8000

# Start the HTTP service by default
ENTRYPOINT ["nlp"]
CMD ["start"]
