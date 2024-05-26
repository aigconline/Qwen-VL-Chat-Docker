FROM ubuntu:focal  

COPY sources.list /etc/apt/sources.list
RUN apt update && apt install -y --no-install-recommends python3 python3-pip && apt clean all

# pip
RUN mkdir /root/.pip/
COPY pip.conf /root/.pip/pip.conf 

# pytorch
RUN pip install torch torchvision torchaudio transformers matplotlib \
        flask tiktoken einops transformers_stream_generator accelerate

COPY Qwen /data/Qwen
COPY main.py /data/main.py

WORKDIR /data
CMD ["python3", "main.py"]
