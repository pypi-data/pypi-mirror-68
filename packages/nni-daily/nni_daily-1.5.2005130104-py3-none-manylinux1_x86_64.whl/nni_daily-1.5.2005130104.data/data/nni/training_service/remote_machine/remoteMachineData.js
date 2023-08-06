'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const shellExecutor_1 = require("./shellExecutor");
class RemoteMachineMeta {
    constructor() {
        this.ip = '';
        this.port = 22;
        this.username = '';
        this.passwd = '';
        this.useActiveGpu = false;
    }
}
exports.RemoteMachineMeta = RemoteMachineMeta;
function parseGpuIndices(gpuIndices) {
    if (gpuIndices !== undefined) {
        const indices = gpuIndices.split(',')
            .map((x) => parseInt(x, 10));
        if (indices.length > 0) {
            return new Set(indices);
        }
        else {
            throw new Error('gpuIndices can not be empty if specified.');
        }
    }
}
exports.parseGpuIndices = parseGpuIndices;
class RemoteCommandResult {
    constructor(stdout, stderr, exitCode) {
        this.stdout = stdout;
        this.stderr = stderr;
        this.exitCode = exitCode;
    }
}
exports.RemoteCommandResult = RemoteCommandResult;
class RemoteMachineTrialJobDetail {
    constructor(id, status, submitTime, workingDirectory, form) {
        this.id = id;
        this.status = status;
        this.submitTime = submitTime;
        this.workingDirectory = workingDirectory;
        this.form = form;
        this.tags = [];
        this.gpuIndices = [];
    }
}
exports.RemoteMachineTrialJobDetail = RemoteMachineTrialJobDetail;
class ExecutorManager {
    constructor(executorArray, maxTrialNumberPerConnection, rmMeta) {
        this.rmMeta = rmMeta;
        this.executorArray = executorArray;
        this.maxTrialNumberPerConnection = maxTrialNumberPerConnection;
    }
    async getAvailableExecutor() {
        for (const index of this.executorArray.keys()) {
            const connectionNumber = this.executorArray[index].getUsedConnectionNumber;
            if (connectionNumber < this.maxTrialNumberPerConnection) {
                this.executorArray[index].addUsedConnectionNumber();
                return this.executorArray[index];
            }
        }
        return await this.initNewShellExecutor();
    }
    addNewShellExecutor(executor) {
        this.executorArray.push(executor);
    }
    getFirstExecutor() {
        return this.executorArray[0];
    }
    closeAllExecutor() {
        for (const executor of this.executorArray) {
            executor.close();
        }
    }
    releaseConnection(executor) {
        if (executor === undefined) {
            throw new Error(`could not release a undefined executor`);
        }
        for (const index of this.executorArray.keys()) {
            if (this.executorArray[index] === executor) {
                this.executorArray[index].minusUsedConnectionNumber();
                break;
            }
        }
    }
    async initNewShellExecutor() {
        const executor = new shellExecutor_1.ShellExecutor();
        await executor.initialize(this.rmMeta);
        return executor;
    }
}
exports.ExecutorManager = ExecutorManager;
var ScheduleResultType;
(function (ScheduleResultType) {
    ScheduleResultType[ScheduleResultType["SUCCEED"] = 0] = "SUCCEED";
    ScheduleResultType[ScheduleResultType["TMP_NO_AVAILABLE_GPU"] = 1] = "TMP_NO_AVAILABLE_GPU";
    ScheduleResultType[ScheduleResultType["REQUIRE_EXCEED_TOTAL"] = 2] = "REQUIRE_EXCEED_TOTAL";
})(ScheduleResultType = exports.ScheduleResultType || (exports.ScheduleResultType = {}));
exports.REMOTEMACHINE_TRIAL_COMMAND_FORMAT = `#!/bin/bash
export NNI_PLATFORM=remote NNI_SYS_DIR={0} NNI_OUTPUT_DIR={1} NNI_TRIAL_JOB_ID={2} NNI_EXP_ID={3} \
NNI_TRIAL_SEQ_ID={4} export MULTI_PHASE={5}
cd $NNI_SYS_DIR
sh install_nni.sh
echo $$ >{6}
python3 -m nni_trial_tool.trial_keeper --trial_command '{7}' --nnimanager_ip '{8}' --nnimanager_port '{9}' \
--nni_manager_version '{10}' --log_collection '{11}' 1>$NNI_OUTPUT_DIR/trialkeeper_stdout 2>$NNI_OUTPUT_DIR/trialkeeper_stderr
echo $? \`date +%s%3N\` >{12}`;
exports.HOST_JOB_SHELL_FORMAT = `#!/bin/bash
cd {0}
echo $$ >{1}
eval {2} >stdout 2>stderr
echo $? \`date +%s%3N\` >{3}`;
