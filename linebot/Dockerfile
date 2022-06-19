FROM public.ecr.aws/lambda/python:3.8
 
RUN yum groupinstall -y "Development Tools" \
    && yum install -y which openssl
 
COPY ./requirement.txt /opt/
RUN pip install --upgrade pip && pip install -r /opt/requirement.txt

WORKDIR /var/task
COPY linebot.py .

CMD ["linebot.lambda_handler"]