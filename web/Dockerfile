# pull official base image
FROM python:latest

RUN apt-get update && apt-get install -y cron
# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip


COPY requirements.txt /code
RUN pip install -r requirements.txt

# copy project
COPY . /code

RUN chmod 755 entrypoint.sh


ENTRYPOINT [ "/code/entrypoint.sh" ]