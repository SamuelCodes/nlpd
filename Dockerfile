FROM ubuntu:trusty

# Set the default locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install dependencies for text analysis
RUN apt-get update && apt-get install -y locales python3-pip unzip \
    ipython3 gfortran liblapack-dev python3-dev curl openjdk-7-jre

# Install gensim for maintaining continuous corpa
RUN pip3 install --upgrade numpy scipy sympy
RUN pip3 install --upgrade beautifulsoup4
RUN pip3 install --upgrade gensim nltk
RUN pip3 install --upgrade sqlitedict
RUN pip3 install --upgrade Pyro4
RUN pip3 install --upgrade tornado
RUN pip3 install --upgrade uwsgi
RUN pip3 install --upgrade pymongo
RUN pip3 install --upgrade scikit-learn

# Install the stanford parser
RUN mkdir -p /tmp/stanford-parser
WORKDIR /tmp/stanford-parser
RUN curl -O http://nlp.stanford.edu/software/stanford-parser-full-2015-04-20.zip
RUN unzip stanford-parser-full-2015-04-20.zip
RUN mkdir -p /app/lib
RUN mv /tmp/stanford-parser/stanford-parser-full-2015-04-20 /app/lib/stanford-parser
RUN rm -rf /tmp/stanford-parser

# Create application directories
RUN mkdir -p /app/data
WORKDIR /app
ADD app/ /app

# Add our binaries to the path
ENV "PATH=/app/bin:$PATH"
ENV "NLTK_DATA=/app/data:$NLTK_DATA"
ENV "CLASSPATH=/app/lib/stanford-parser"

# Export the data volume
VOLUME /app/data

# Expose language services on port 8000
EXPOSE 8000

# Start the HTTP service by default
ENTRYPOINT ["nlp"]
CMD ["start"]
