const functions = require("firebase-functions");
const admin = require("firebase-admin");

admin.initializeApp();
const bucket = admin.storage().bucket();

exports.downloadFiles = functions.storage.object().onFinalize((object) => {
    const filePath = object.name;
    const destinationPath = `./${filePath}`;
    const file = bucket.file(filePath);
    return file.download({ destination: destinationPath }).then(() => {
        console.log(`File ${filePath} downloaded to ${destinationPath}.`);
    });
});
