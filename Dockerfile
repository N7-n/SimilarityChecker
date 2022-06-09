FROM public.ecr.aws/lambda/python:3.8
 
# install build libs
RUN yum groupinstall -y "Development Tools" \
    && yum install -y which openssl
 
# install mecab, ipadic, ipadic-neologd
WORKDIR /tmp
RUN  curl -L "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE" -o mecab-0.996.tar.gz \
    && tar xzf mecab-0.996.tar.gz \
    && cd mecab-0.996 \
    && ./configure \
    && make \
    && make check \
    && make install \
    && cd .. \
    && rm -rf mecab-0.996*
 
WORKDIR /tmp
RUN curl -L "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM" -o mecab-ipadic-2.7.0-20070801.tar.gz \
    && tar -zxvf mecab-ipadic-2.7.0-20070801.tar.gz \
    && cd mecab-ipadic-2.7.0-20070801 \
    && ./configure --with-charset=utf8 \
    && make \
    && make install \
    && cd .. \
    && rm -rf mecab-ipadic-2.7.0-20070801
 
WORKDIR /tmp
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd \
    && ./bin/install-mecab-ipadic-neologd -n -a -y \
    && rm -rf mecab-ipadic-neologd
 
# setup python
COPY ./requirement.txt /opt/
RUN pip install --upgrade pip && pip install -r /opt/requirement.txt

# set function code
WORKDIR /var/task
COPY learn.py .
CMD ["learn.lambda_handler"]