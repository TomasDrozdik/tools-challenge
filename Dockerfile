FROM ubuntu:latest
RUN apt-get update -y && apt-get install -y cbmc python3 cmake make gcc g++
CMD ["bash"]