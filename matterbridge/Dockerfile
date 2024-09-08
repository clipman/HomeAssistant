FROM luligu/matterbridge:latest
EXPOSE 8283
EXPOSE 5540

RUN mkdir /app
WORKDIR /app

RUN \
    ln -s /config /root/.matterbridge

COPY run.sh run.sh
RUN chmod a+x run.sh

CMD [ "/app/run.sh" ]
