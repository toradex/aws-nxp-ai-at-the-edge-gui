FROM matheuscastello/binutils-deb:64

# install ai2go deps
RUN apt-get -y update && apt-get install -y \
	libgstreamer1.0-0 \
	libgtk-3-0 \
	gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-bad \
	gstreamer1.0-plugins-base \
	v4l-utils \
	gstreamer1.0-tools \
	python3 \
    python3-pip \
	python3-cairo \
	python3-gi-cairo \
	python3-gst-1.0 \
	libatomic1 \
	shared-mime-info \
	&& apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update && apt-get install -y \
    libopenblas-base \
    libopenblas-dev \
    ninja-build \
    libopencv-dev \
    && apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# compile mxnet
RUN git clone --recursive https://github.com/apache/incubator-mxnet.git && \
    cd incubator-mxnet && \
    mkdir build && cd build && \
    cmake -DUSE_BLAS=open -DUSE_CUDA=0 -DUSE_CUDNN=0 -DENABLE_CUDA_RTC=0 -DUSE_JEMALLOC=0 -DUSE_MKL=0 -DUSE_MKLDNN=0 -DUSE_MKL_IF_AVAILABLE=0 -GNinja .. && \
    ninja -v -j12 && \
    ninja -v install

RUN apt-get -y update && apt-get install -y \
    python3-opencv \
    python3-pil \
    python3-nose \
    python3-numpy \
    python3-nose-timer \
    python3-requests \
    python3-h5py \
    python3-scipy \
    python3-boto3 \
    && apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

RUN apt-get -y update && apt-get install -y \
    libfreetype6-dev \
    && apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# copy and install requirements for project
COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /project
WORKDIR /project

# install the mxnet bind for python
RUN cd /incubator-mxnet && \
    cd python && \
    pip3 install -e .

ENTRYPOINT [ "python3", "camtest.py" ]

#CMD [ "bash" ]
