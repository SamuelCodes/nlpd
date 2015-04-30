FROM ubuntu:trusty

# Set the default locale
ENV LANG en_US.UTF-8

# Install dependencies for text analysis
RUN apt-get update && apt-get install -y locales python-pip ipython gfortran liblapack-dev python-dev

# Install gensim for maintaining continuous corpa
RUN pip install --upgrade numpy scipy sympy
RUN pip install --upgrade beautifulsoup
RUN pip install --upgrade simserver
RUN pip install --upgrade gensim nltk
RUN pip install --upgrade sqlitedict
RUN pip install --upgrade Pyro4
RUN pip install --upgrade web.py gunicorn

# Create application directories
RUN mkdir -p /app/data
WORKDIR /app
ADD app/ /app

# Add our binaries to the path
ENV "PATH=/app/bin:$PATH"
ENV "NLTK_DATA=/app/data:$NLTK_DATA"

# Export the data volume
VOLUME /app/data

# Expose language services on port 8000
EXPOSE 8000

# Start the HTTP service by default
ENTRYPOINT ["nlp"]
CMD ["start"]
