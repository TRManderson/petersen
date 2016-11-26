FROM python:3.5-alpine
WORKDIR /srv
ADD petersen-0.0.1-py3-none-any.whl /opt/petersen-0.0.1-py3-none-any.whl
RUN python setup.py /opt/petersen-0.0.1-py3-none-any.whl && rm /opt/petersen-0.0.1-py3-none-any.whl
CMD python -m petersen