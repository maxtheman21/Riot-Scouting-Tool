const fs = require('fs'); // Node.js file system module

let championByIdCache = {};
let championJson = {};

async function getLatestChampionDDragon(language = "en_US") {
    if (championJson[language]) return championJson[language];

    let response;
    let versionIndex = 0;
    do { // I loop over versions because 9.22.1 is broken
        const version = (await fetch("http://ddragon.leagueoflegends.com/api/versions.json").then(async (r) => await r.json()))[versionIndex++];

        response = await fetch(`https://ddragon.leagueoflegends.com/cdn/${version}/data/${language}/champion.json`);
    } while (!response.ok)

    championJson[language] = await response.json();
    return championJson[language];
}

async function getChampionByKey(key, language = "en_US") {
    if (!championByIdCache[language]) {
        let json = await getLatestChampionDDragon(language);

        championByIdCache[language] = {};
        for (var championName in json.data) {
            if (!json.data.hasOwnProperty(championName))
                continue;

            const champInfo = json.data[championName];
            championByIdCache[language][champInfo.key] = champInfo;
        }
    }

    return championByIdCache[language][key];
}

async function getChampionByID(name, language = "en_US") {
    return await getLatestChampionDDragon(language)[name];
}

async function saveChampionsToFile() {
    const json = await getLatestChampionDDragon("en_US");

    fs.writeFileSync('./championKey/champion.json', JSON.stringify(json, null, 4), 'utf-8');
    console.log("Champion data has been written to 'champion.json'");
}

saveChampionsToFile();
