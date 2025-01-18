FROM python:3.13.1

# Create static & media folders and set dir
ENV HOME=/var/www/algopath
RUN mkdir /var/www && mkdir $HOME
RUN mkdir $HOME/static && mkdir $HOME/media
WORKDIR $HOME

# Set up python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade packages
RUN pip install --upgrade pip

# Create a local virtual environment
RUN pip install virtualenv && virtualenv src/venv

# Install all requirements
COPY src/requirements.txt src
RUN . src/venv/bin/activate && pip install -r src/requirements.txt

RUN apt-get update && apt-get -y install gettext

# Copy project files
COPY . $HOME

#COPY --chown=root . /var/www/algopath
#RUN chmod +x /var/www/algopath/entrypoint.sh
ENTRYPOINT ["/var/www/algopath/deploy/prod/entrypoint.sh"]