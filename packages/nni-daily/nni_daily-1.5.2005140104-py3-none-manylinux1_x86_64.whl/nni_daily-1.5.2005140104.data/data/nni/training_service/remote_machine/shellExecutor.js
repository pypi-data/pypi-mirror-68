'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const os = require("os");
const path = require("path");
const fs = require("fs");
const ssh2_1 = require("ssh2");
const ts_deferred_1 = require("ts-deferred");
const linuxCommands_1 = require("./extends/linuxCommands");
const log_1 = require("../../common/log");
const errors_1 = require("../../common/errors");
const util_1 = require("../common/util");
const utils_1 = require("../../common/utils");
class ShellExecutor {
    constructor() {
        this.sshClient = new ssh2_1.Client();
        this.usedConnectionNumber = 0;
        this.pathSpliter = '/';
        this.multiplePathSpliter = new RegExp(`\\${this.pathSpliter}{2,}`);
    }
    async initialize(rmMeta) {
        const deferred = new ts_deferred_1.Deferred();
        const connectConfig = {
            host: rmMeta.ip,
            port: rmMeta.port,
            username: rmMeta.username,
            tryKeyboard: true
        };
        if (rmMeta.passwd !== undefined) {
            connectConfig.password = rmMeta.passwd;
        }
        else if (rmMeta.sshKeyPath !== undefined) {
            if (!fs.existsSync(rmMeta.sshKeyPath)) {
                deferred.reject(new Error(`${rmMeta.sshKeyPath} does not exist.`));
            }
            const privateKey = fs.readFileSync(rmMeta.sshKeyPath, 'utf8');
            connectConfig.privateKey = privateKey;
            connectConfig.passphrase = rmMeta.passphrase;
        }
        else {
            deferred.reject(new Error(`No valid passwd or sshKeyPath is configed.`));
        }
        this.sshClient.on('ready', async () => {
            const result = await this.execute("ver");
            if (result.exitCode == 0 && result.stdout.search("Windows") > -1) {
                throw new Error("not implement Windows commands yet.");
            }
            else {
                this.osCommands = new linuxCommands_1.LinuxCommands();
            }
            deferred.resolve();
        }).on('error', (err) => {
            deferred.reject(new Error(err.message));
        }).on("keyboard-interactive", (name, instructions, lang, prompts, finish) => {
            finish([rmMeta.passwd]);
        }).connect(connectConfig);
        return deferred.promise;
    }
    close() {
        this.sshClient.end();
    }
    get getUsedConnectionNumber() {
        return this.usedConnectionNumber;
    }
    addUsedConnectionNumber() {
        this.usedConnectionNumber += 1;
    }
    minusUsedConnectionNumber() {
        this.usedConnectionNumber -= 1;
    }
    async createFolder(folderName, sharedFolder = false) {
        const commandText = this.osCommands && this.osCommands.createFolder(folderName, sharedFolder);
        const commandResult = await this.execute(commandText);
        const result = commandResult.exitCode >= 0;
        return result;
    }
    async allowPermission(isRecursive = false, ...folders) {
        const commandText = this.osCommands && this.osCommands.allowPermission(isRecursive, ...folders);
        const commandResult = await this.execute(commandText);
        const result = commandResult.exitCode >= 0;
        return result;
    }
    async removeFolder(folderName, isRecursive = false, isForce = true) {
        const commandText = this.osCommands && this.osCommands.removeFolder(folderName, isRecursive, isForce);
        const commandResult = await this.execute(commandText);
        const result = commandResult.exitCode >= 0;
        return result;
    }
    async removeFiles(folderOrFileName, filePattern = "") {
        const commandText = this.osCommands && this.osCommands.removeFiles(folderOrFileName, filePattern);
        const commandResult = await this.execute(commandText);
        const result = commandResult.exitCode >= 0;
        return result;
    }
    async readLastLines(fileName, lineCount = 1) {
        const commandText = this.osCommands && this.osCommands.readLastLines(fileName, lineCount);
        const commandResult = await this.execute(commandText);
        let result = "";
        if (commandResult !== undefined && commandResult.stdout !== undefined && commandResult.stdout.length > 0) {
            result = commandResult.stdout;
        }
        return result;
    }
    async isProcessAlive(pidFileName) {
        const commandText = this.osCommands && this.osCommands.isProcessAliveCommand(pidFileName);
        const commandResult = await this.execute(commandText);
        const result = this.osCommands && this.osCommands.isProcessAliveProcessOutput(commandResult);
        return result !== undefined ? result : false;
    }
    async killChildProcesses(pidFileName) {
        const commandText = this.osCommands && this.osCommands.killChildProcesses(pidFileName);
        const commandResult = await this.execute(commandText);
        return commandResult.exitCode == 0;
    }
    async extractFile(tarFileName, targetFolder) {
        const commandText = this.osCommands && this.osCommands.extractFile(tarFileName, targetFolder);
        const commandResult = await this.execute(commandText);
        return commandResult.exitCode == 0;
    }
    async executeScript(script, isFile, isInteractive = false) {
        const commandText = this.osCommands && this.osCommands.executeScript(script, isFile);
        const commandResult = await this.execute(commandText, undefined, isInteractive);
        return commandResult.exitCode == 0;
    }
    async copyFileToRemote(localFilePath, remoteFilePath) {
        const log = log_1.getLogger();
        log.debug(`copyFileToRemote: localFilePath: ${localFilePath}, remoteFilePath: ${remoteFilePath}`);
        const deferred = new ts_deferred_1.Deferred();
        this.sshClient.sftp((err, sftp) => {
            if (err !== undefined && err !== null) {
                log.error(`copyFileToRemote: ${err.message}, ${localFilePath}, ${remoteFilePath}`);
                deferred.reject(err);
                return;
            }
            assert(sftp !== undefined);
            sftp.fastPut(localFilePath, remoteFilePath, (fastPutErr) => {
                sftp.end();
                if (fastPutErr !== undefined && fastPutErr !== null) {
                    deferred.reject(fastPutErr);
                }
                else {
                    deferred.resolve(true);
                }
            });
        });
        return deferred.promise;
    }
    async copyDirectoryToRemote(localDirectory, remoteDirectory, remoteOS) {
        const tmpSuffix = utils_1.uniqueString(5);
        const localTarPath = path.join(os.tmpdir(), `nni_tmp_local_${tmpSuffix}.tar.gz`);
        const remoteTarPath = utils_1.unixPathJoin(utils_1.getRemoteTmpDir(remoteOS), `nni_tmp_remote_${tmpSuffix}.tar.gz`);
        await util_1.tarAdd(localTarPath, localDirectory);
        await this.copyFileToRemote(localTarPath, remoteTarPath);
        await util_1.execRemove(localTarPath);
        await this.extractFile(remoteTarPath, remoteDirectory);
        await this.removeFiles(remoteTarPath);
    }
    async getRemoteFileContent(filePath) {
        const deferred = new ts_deferred_1.Deferred();
        this.sshClient.sftp((err, sftp) => {
            if (err !== undefined && err !== null) {
                log_1.getLogger()
                    .error(`getRemoteFileContent: ${err.message}`);
                deferred.reject(new Error(`SFTP error: ${err.message}`));
                return;
            }
            try {
                const sftpStream = sftp.createReadStream(filePath);
                let dataBuffer = '';
                sftpStream.on('data', (data) => {
                    dataBuffer += data;
                })
                    .on('error', (streamErr) => {
                    sftp.end();
                    deferred.reject(new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, streamErr.message));
                })
                    .on('end', () => {
                    sftp.end();
                    deferred.resolve(dataBuffer);
                });
            }
            catch (error) {
                log_1.getLogger()
                    .error(`getRemoteFileContent: ${error.message}`);
                sftp.end();
                deferred.reject(new Error(`SFTP error: ${error.message}`));
            }
        });
        return deferred.promise;
    }
    async execute(command, processOutput = undefined, useShell = false) {
        const log = log_1.getLogger();
        log.debug(`remoteExeCommand: command: [${command}]`);
        const deferred = new ts_deferred_1.Deferred();
        let stdout = '';
        let stderr = '';
        let exitCode;
        const callback = (err, channel) => {
            if (err !== undefined && err !== null) {
                log.error(`remoteExeCommand: ${err.message}`);
                deferred.reject(err);
                return;
            }
            channel.on('data', (data) => {
                stdout += data;
            });
            channel.on('exit', (code) => {
                exitCode = code;
                log.debug(`remoteExeCommand exit(${exitCode})\nstdout: ${stdout}\nstderr: ${stderr}`);
                let result = {
                    stdout: stdout,
                    stderr: stderr,
                    exitCode: exitCode
                };
                if (processOutput != undefined) {
                    result = processOutput(result);
                }
                deferred.resolve(result);
            });
            channel.stderr.on('data', function (data) {
                stderr += data;
            });
            if (useShell) {
                channel.stdin.write(`${command}\n`);
                channel.end("exit\n");
            }
            return;
        };
        if (useShell) {
            this.sshClient.shell(callback);
        }
        else {
            this.sshClient.exec(command !== undefined ? command : "", callback);
        }
        return deferred.promise;
    }
}
exports.ShellExecutor = ShellExecutor;
