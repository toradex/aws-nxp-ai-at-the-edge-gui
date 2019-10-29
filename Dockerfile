FROM matheuscastello/weston-deps:arm64

# install deps
RUN apt-get -y update && apt-get install -y \
	chromium \
    libgtk2.0-0 \
    libnss3 \
    libgtk-3-0 \
    libxss1 \
    libasound2 \
	&& apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*

# copy the dist
COPY dist/ /app

# made a symlink for bin
RUN ln -s /app/electron/AWS\ Demo\ Local\ UI-linux-arm64/AWS\ Demo\ Local\ UI \
    /usr/bin/aws-app

# cmd to entrypoint
ENV APP="aws-app"
ENV APPARGS="--no-sandbox --enable-logging"

# cmd as argument
#CMD [ "www.toradex.com/pt-br/operating-systems/torizon" ]
