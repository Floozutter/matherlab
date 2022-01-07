const randomPhrase7 = require("./randomPhrase7");
const process = require("process");

function main(args) {
    // get number of short IDs to generate
    const n = parseInt(args[0], 10);
    // run simulation
    const collided = (() => {
        const ret = [];
        const seen = new Set();
        for (let i = 0; i < n; ++i) {
            const sid = randomPhrase7();
            ret.push(seen.has(sid));
            seen.add(sid);
        };
        return ret;
    })();
    // print results
    collided.forEach(c => {
        process.stdout.write(c ? "1" : "0");
    });
    process.stdout.write("\n");
}

main(process.argv.slice(2));
