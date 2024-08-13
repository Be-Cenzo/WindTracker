FROM node:20.10.0

RUN mkdir /home/web-app
COPY . /home/web-app
RUN cd /home/web-app
RUN echo '#!/bin/bash\n\
echo "Starting deployment..."\n\
npm install\n\
npm run dev' > /home/web-app/deploy.shv

WORKDIR /home/web-app
CMD [ "sh", "deploy.shv" ]
