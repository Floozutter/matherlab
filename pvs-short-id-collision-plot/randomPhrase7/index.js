const fs = require("fs");
const path = require("path");

// filtered WordNet 3.1 words
const words = fname => fs.readFileSync(path.resolve(__dirname, fname), "utf8").trim().split("\n");
const adjs3 = words("wn3.1-adjs3.txt");
const adjs4 = words("wn3.1-adjs4.txt");
const nouns3 = words("wn3.1-nouns3.txt");
const nouns4 = words("wn3.1-nouns4.txt");

function capitalizeFirst(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}
function randomPhrase7() {
    // choose any adjective
    const i = Math.floor((adjs3.length+adjs4.length) * Math.random());
    const adj = i < adjs3.length ? adjs3[i] : adjs4[i-adjs3.length];
    // choose a noun from only those that will result in a phrase with length 7
    const validNouns = adj.length === 3 ? nouns4 : nouns3;
    const j = Math.floor(validNouns.length * Math.random())
    const noun = validNouns[j];
    return capitalizeFirst(adj) + capitalizeFirst(noun);
}

module.exports = randomPhrase7;
