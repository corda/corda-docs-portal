// Run this from the themes/r3 folder - we look up two folders for the site.

const { spawn } = require('child_process');

const yarn = spawn('yarn', [ '--cwd', '.', 'start', '--watch'], {stdio: "inherit"});
yarn.on('connected', () => {
  yarn.stdout.on('data', data => { console.log(`${data}`); });
  yarn.stderr.on('data', data => { console.error(`ERROR: ${data}`); });
});
yarn.on('close', code => { console.log(`Yarn exited with code ${code}`); });

const hugo = spawn('hugo', ['--source','../..','serve'], {stdio: "inherit"});
hugo.on('connected', () => {
  hugo.stdout.on('data', data => { console.log(`${data}`); });
  hugo.stderr.on('data', data => { console.error(`ERROR: ${data}`); });
});
hugo.on('close', code => { console.log(`Hugo exited with code ${code}`); });
