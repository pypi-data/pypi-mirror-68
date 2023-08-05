'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const fs = require("fs");
const chai = require("chai");
const chaiAsPromised = require("chai-as-promised");
const shellExecutor_1 = require("../shellExecutor");
const utils_1 = require("../../../common/utils");
const LOCALFILE = '/tmp/localSshclientUTData';
const REMOTEFILE = '/tmp/remoteSshclientUTData';
const REMOTEFOLDER = '/tmp/remoteSshclientUTFolder';
async function copyFile(executor) {
    await executor.copyFileToRemote(LOCALFILE, REMOTEFILE);
}
async function copyFileToRemoteLoop(executor) {
    for (let i = 0; i < 10; i++) {
        await executor.copyFileToRemote(LOCALFILE, REMOTEFILE);
    }
}
async function getRemoteFileContentLoop(executor) {
    for (let i = 0; i < 10; i++) {
        await executor.getRemoteFileContent(REMOTEFILE);
    }
}
describe('ShellExecutor test', () => {
    let skip = false;
    let rmMeta;
    try {
        rmMeta = JSON.parse(fs.readFileSync('../../.vscode/rminfo.json', 'utf8'));
        console.log(rmMeta);
    }
    catch (err) {
        console.log(`Please configure rminfo.json to enable remote machine test.${err}`);
        skip = true;
    }
    before(async () => {
        chai.should();
        chai.use(chaiAsPromised);
        await cpp.exec(`echo '1234' > ${LOCALFILE}`);
        utils_1.prepareUnitTest();
    });
    after(() => {
        utils_1.cleanupUnitTest();
        fs.unlinkSync(LOCALFILE);
    });
    it('Test mkdir', async () => {
        if (skip) {
            return;
        }
        const shellExecutor = new shellExecutor_1.ShellExecutor();
        await shellExecutor.initialize(rmMeta);
        let result = await shellExecutor.createFolder(REMOTEFOLDER, false);
        chai.expect(result).eq(true);
        result = await shellExecutor.removeFolder(REMOTEFOLDER);
        chai.expect(result).eq(true);
    });
    it('Test ShellExecutor', async () => {
        if (skip) {
            return;
        }
        const shellExecutor = new shellExecutor_1.ShellExecutor();
        await shellExecutor.initialize(rmMeta);
        await copyFile(shellExecutor);
        await Promise.all([
            copyFileToRemoteLoop(shellExecutor),
            copyFileToRemoteLoop(shellExecutor),
            copyFileToRemoteLoop(shellExecutor),
            getRemoteFileContentLoop(shellExecutor)
        ]);
    });
});
