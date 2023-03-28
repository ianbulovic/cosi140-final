FROM node

WORKDIR /app
RUN git clone https://github.com/jonorthwash/ud-annotatrix.git
WORKDIR /app/ud-annotatrix
RUN npm install https://github.com/TryGhost/node-sqlite3/tarball/master

CMD ["npm", "run", "dev-server"]
