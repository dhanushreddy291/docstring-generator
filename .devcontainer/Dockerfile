FROM python:3.10-alpine

# Install Git and Dependencies
RUN apk add --no-cache git
RUN pip install --upgrade pip && pip install openai redbaron autoflake black

# Upgrade
RUN apk upgrade