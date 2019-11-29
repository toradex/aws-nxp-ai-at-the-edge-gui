FROM matheuscastello/weston-deps:arm64

# install deps
RUN apt-get -y update && apt-get install -y \
    chromium \
    libgtk2.0-0 \
    libnss3 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
    wget bzip2 \
    && apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# we have to do it to gpu features
RUN wget https://www.nxp.com/lgfiles/NMG/MAD/YOCTO/imx-gpu-viv-6.2.4.p4.0-aarch64.bin && \
    chmod +x ./imx-gpu-viv-6.2.4.p4.0-aarch64.bin && \
    ./imx-gpu-viv-6.2.4.p4.0-aarch64.bin --auto-accept && \
    cd imx-gpu-viv-6.2.4.p4.0-aarch64 && \
    cp -r --preserve=links gpu-core/usr/lib/* /usr/lib/aarch64-linux-gnu && \
    cp gpu-core/etc/* /etc/ && \
    cd /usr/lib/aarch64-linux-gnu/ && \
    ln -sf libEGL-wl.so libEGL.so && \
    ln -sf libEGL-wl.so libEGL.so.1 && \
    ln -sf libEGL-wl.so libEGL.so.1.0 && \
    ln -sf libGAL-wl.so libGAL.so && \
    ln -sf libGLESv2-wl.so libGLESv2.so && \
    ln -sf libGLESv2-wl.so libGLESv2.so.2 && \
    ln -sf libGLESv2-wl.so libGLESv2.so.2.0.0 && \
    ln -sf libVDK-wl.so libVDK.so && \
    ln -sf libvulkan-wl.so libvulkan.so && \
    rm -rf libgbm.so.1 && \
    ln -s libgbm.so libgbm.so.1

# copy the dist
COPY dist/ /app

# made a symlink for bin
RUN ln -s /app/electron/AWS\ Demo\ Local\ UI-linux-arm64/AWS\ Demo\ Local\ UI \
    /usr/bin/aws-app

COPY run_after.sh /usr/bin

# cmd to entrypoint
ENV APP="run_after.sh"
ENV APPARGS=""

# cmd as argument
#CMD [ "www.toradex.com/pt-br/operating-systems/torizon" ]
