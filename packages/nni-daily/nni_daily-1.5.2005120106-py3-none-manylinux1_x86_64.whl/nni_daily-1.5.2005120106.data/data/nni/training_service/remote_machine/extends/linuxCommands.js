'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const osCommands_1 = require("../osCommands");
class LinuxCommands extends osCommands_1.OsCommands {
    createFolder(folderName, sharedFolder = false) {
        let command;
        if (sharedFolder) {
            command = `umask 0; mkdir -p '${folderName}'`;
        }
        else {
            command = `mkdir -p '${folderName}'`;
        }
        return command;
    }
    allowPermission(isRecursive = false, ...folders) {
        const folderString = folders.join("' '");
        let command;
        if (isRecursive) {
            command = `chmod 777 -R '${folderString}'`;
        }
        else {
            command = `chmod 777 '${folderString}'`;
        }
        return command;
    }
    removeFolder(folderName, isRecursive = false, isForce = true) {
        let flags = '';
        if (isForce || isRecursive) {
            flags = `-${isRecursive ? 'r' : 'd'}${isForce ? 'f' : ''} `;
        }
        const command = `rm ${flags}'${folderName}'`;
        return command;
    }
    removeFiles(folderName, filePattern) {
        const files = this.joinPath(folderName, filePattern);
        const command = `rm '${files}'`;
        return command;
    }
    readLastLines(fileName, lineCount = 1) {
        const command = `tail -n ${lineCount} '${fileName}'`;
        return command;
    }
    isProcessAliveCommand(pidFileName) {
        const command = `kill -0 \`cat '${pidFileName}'\``;
        return command;
    }
    isProcessAliveProcessOutput(commandResult) {
        let result = true;
        if (commandResult.exitCode !== 0) {
            result = false;
        }
        return result;
    }
    killChildProcesses(pidFileName) {
        const command = `pkill -P \`cat '${pidFileName}'\``;
        return command;
    }
    extractFile(tarFileName, targetFolder) {
        const command = `tar -oxzf '${tarFileName}' -C '${targetFolder}'`;
        return command;
    }
    executeScript(script, isFile) {
        let command;
        if (isFile) {
            command = `bash '${script}'`;
        }
        else {
            script = script.replace('"', '\\"');
            command = `bash -c "${script}"`;
        }
        return command;
    }
}
exports.LinuxCommands = LinuxCommands;
