const harToCurl = require('./har-to-curl');
const fs = require('fs');
const path = require('path');


function fromDir(startPath,filter){

    let filesPath = new Array();

    if (!fs.existsSync(startPath)){
        console.log("no dir ",startPath);
        return;
    }

    let files=fs.readdirSync(startPath);
    for(let i=0;i<files.length;i++){
        let filename=path.join(startPath,files[i]);
        let stat = fs.lstatSync(filename);
        if (stat.isDirectory()){
            fromDir(filename,filter); //recurse
        }
        else if (filename.indexOf(filter)>=0) {
           filesPath.push(filename)
        };
    };

    return filesPath;
};

const args = process.argv.slice(2)
let harDirectory = args[0]
let harFilesPath = fromDir(harDirectory, '.har');

harFilesPath.forEach((value) => {
    let harRawData = fs.readFileSync(value);
    let harString = JSON.parse(harRawData);

    let curlString = harToCurl(harString);
    console.log(value + "---" + curlString.toString())
})


