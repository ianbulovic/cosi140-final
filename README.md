# cosi140-final

## Annotation
We are using [ud-annotatrix](https://github.com/jonorthwash/ud-annotatrix).
To use the annotation tool, either run it yourself with npm or use the provided Dockerfile.

### Using npm
1. Install [npm](https://docs.npmjs.com/cli/v7/configuring-npm/install) if you haven't already.
2. Clone the ud-annotatrix repository:
```sh
git clone https://github.com/jonorthwash/ud-annotatrix.git
```
3. Build the program using npm. It also requires another package to be installed. All in one command:
```sh
npm install https://github.com/TryGhost/node-sqlite3/tarball/master
```
4. Run the server.
```sh
npm run dev-server
```

### Using Docker
1. Install [Docker](https://docs.docker.com/get-docker/) if you haven't already.
2. Build the image (make sure to run from the root of this project).
```sh
docker build -t ud-annotatrix .
```
3. Run the container using the provided script for convenience.
```sh
chmod +x run_server.sh
./run_server.sh
```

Either method of running will save any files you upload as json in `corpora/` in the currect directory.
You still have to download them separately when you are finished annotating to get them in a readable format.
