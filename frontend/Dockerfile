FROM node:14

WORKDIR /usr/src/app

COPY ./frontend/package.json /usr/src/app/
COPY ./frontend/yarn.lock /usr/src/app/
COPY ./frontend/packages/api/package.json /usr/src/app/packages/api/
COPY ./frontend/packages/utils/package.json /usr/src/app/packages/utils/
COPY ./frontend/packages/web-console/package.json /usr/src/app/packages/web-console/
COPY ./frontend/packages/web-shop/package.json /usr/src/app/packages/web-shop/
COPY ./frontend/packages/web-mypage/package.json /usr/src/app/packages/web-mypage/
COPY ./frontend/packages/web-card/package.json /usr/src/app/packages/web-card/

RUN yarn install

COPY ./ /usr/src/app
