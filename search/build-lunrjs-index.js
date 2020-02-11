const path = require('path');
const fs = require('fs').promises;
const { promisify } = require('util');
const frontMatterParser = require('parser-front-matter');

const parse = promisify(frontMatterParser.parse.bind(frontMatterParser));

const walk = async (dir, filelist = []) => {
    const files = await fs.readdir(dir);

    for (file of files) {
        const filepath = path.join(dir, file);
        const stat = await fs.stat(filepath);

        if (stat.isDirectory()) {
            filelist = await walk(filepath, filelist);
        } else {
            if (file.endsWith('.md'))
                filelist.push(dir + '/' + file);
        }
    }

    return filelist;
}

async function loadPostsWithFrontMatter(postsDirectoryPath) {

    const postNames = await walk(postsDirectoryPath);
    const posts = await Promise.all(
        postNames.map(async fileName => {
            const fileContent = await fs.readFile(
                `${fileName}`,
                'utf8'
            );
            const { content, data } = await parse(fileContent);
            return {
                content: content.slice(0, 3000),
                ...data
            };
        })
    );
    return posts;
}

const lunrjs = require('lunr');

function makeIndex(posts) {
    return lunrjs(function () {
        this.ref('title');
        this.field('title');
        this.field('content');
        this.field('tags');
        posts.forEach(p => {
            this.add(p);
        });
    });
}

// TODO - by language
async function run() {
    resolve = require('path').resolve
    const here = resolve(`${__dirname}`)
    const ROOT = path.dirname(here);

    // TODO - LANGUAGE
    const posts = await loadPostsWithFrontMatter(ROOT + '/content/en/docs/');
    const index = makeIndex(posts);

    // The index that we pipe to a file
    console.log(JSON.stringify(index));
}

run()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error.stack);
        process.exit(1);
    });
