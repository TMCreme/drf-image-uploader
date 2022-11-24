# pull official base image
FROM python:3.9.6-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATABASE=postgres

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Set the working directory
WORKDIR /opt/michalproj

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /opt/michalproj/
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /opt/michalproj/

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /opt/michalproj/entrypoint.sh
RUN chmod +x /opt/michalproj/entrypoint.sh

# EXPOSE 5433
# EXPOSE 9011

# run entrypoint.sh
ENTRYPOINT ["/opt/michalproj/entrypoint.sh"]
