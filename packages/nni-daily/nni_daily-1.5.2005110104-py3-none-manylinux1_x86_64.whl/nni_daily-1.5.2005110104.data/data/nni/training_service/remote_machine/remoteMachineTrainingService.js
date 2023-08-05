'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const events_1 = require("events");
const fs = require("fs");
const path = require("path");
const ts_deferred_1 = require("ts-deferred");
const typescript_string_operations_1 = require("typescript-string-operations");
const component = require("../../common/component");
const errors_1 = require("../../common/errors");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const observableTimer_1 = require("../../common/observableTimer");
const utils_1 = require("../../common/utils");
const containerJobData_1 = require("../common/containerJobData");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const util_1 = require("../common/util");
const gpuScheduler_1 = require("./gpuScheduler");
const remoteMachineData_1 = require("./remoteMachineData");
const remoteMachineJobRestServer_1 = require("./remoteMachineJobRestServer");
let RemoteMachineTrainingService = class RemoteMachineTrainingService {
    constructor(timer) {
        this.MAX_TRIAL_NUMBER_PER_EXECUTOR = 5;
        this.stopping = false;
        this.isMultiPhase = false;
        this.versionCheck = true;
        this.remoteOS = 'linux';
        this.metricsEmitter = new events_1.EventEmitter();
        this.trialJobsMap = new Map();
        this.trialExecutorMap = new Map();
        this.machineExecutorManagerMap = new Map();
        this.jobQueue = [];
        this.expRootDir = utils_1.getExperimentRootDir();
        this.remoteExpRootDir = this.getRemoteExperimentRootDir();
        this.timer = timer;
        this.log = log_1.getLogger();
        this.trialSequenceId = -1;
        this.logCollection = 'none';
        this.log.info('Construct remote machine training service.');
    }
    async run() {
        const restServer = component.get(remoteMachineJobRestServer_1.RemoteMachineJobRestServer);
        await restServer.start();
        restServer.setEnableVersionCheck = this.versionCheck;
        this.log.info('Run remote machine training service.');
        while (!this.stopping) {
            while (this.jobQueue.length > 0) {
                this.updateGpuReservation();
                const trialJobId = this.jobQueue[0];
                const prepareResult = await this.prepareTrialJob(trialJobId);
                if (prepareResult) {
                    this.jobQueue.shift();
                }
                else {
                    break;
                }
            }
            if (restServer.getErrorMessage !== undefined) {
                throw new Error(restServer.getErrorMessage);
                this.stopping = true;
            }
            await utils_1.delay(3000);
        }
        this.log.info('Remote machine training service exit.');
    }
    async allocateExecutorForTrial(trial) {
        if (trial.rmMeta === undefined) {
            throw new Error(`rmMeta not set in trial ${trial.id}`);
        }
        const executorManager = this.machineExecutorManagerMap.get(trial.rmMeta);
        if (executorManager === undefined) {
            throw new Error(`executorManager not initialized`);
        }
        const shellExecutor = await executorManager.getAvailableExecutor();
        this.trialExecutorMap.set(trial.id, shellExecutor);
    }
    releaseTrialExecutor(trial) {
        if (trial.rmMeta === undefined) {
            throw new Error(`rmMeta not set in trial ${trial.id}`);
        }
        const executorManager = this.machineExecutorManagerMap.get(trial.rmMeta);
        if (executorManager === undefined) {
            throw new Error(`executorManager not initialized`);
        }
        executorManager.releaseConnection(this.trialExecutorMap.get(trial.id));
    }
    async listTrialJobs() {
        const jobs = [];
        const deferred = new ts_deferred_1.Deferred();
        for (const [key,] of this.trialJobsMap) {
            jobs.push(await this.getTrialJob(key));
        }
        deferred.resolve(jobs);
        return deferred.promise;
    }
    async getTrialJob(trialJobId) {
        const trialJob = this.trialJobsMap.get(trialJobId);
        if (trialJob === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.NOT_FOUND, `trial job id ${trialJobId} not found`);
        }
        if (trialJob.status === 'RUNNING' || trialJob.status === 'UNKNOWN') {
            if (trialJob.rmMeta === undefined) {
                throw new Error(`rmMeta not set for submitted job ${trialJobId}`);
            }
            const executor = this.trialExecutorMap.get(trialJob.id);
            if (executor === undefined) {
                throw new Error(`Invalid job id: ${trialJobId}, cannot find executor`);
            }
            return this.updateTrialJobStatus(trialJob, executor);
        }
        else {
            return trialJob;
        }
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    async submitTrialJob(form) {
        if (this.trialConfig === undefined) {
            throw new Error('trial config is not initialized');
        }
        const trialJobId = utils_1.uniqueString(5);
        const trialWorkingFolder = utils_1.unixPathJoin(this.remoteExpRootDir, 'trials', trialJobId);
        const trialJobDetail = new remoteMachineData_1.RemoteMachineTrialJobDetail(trialJobId, 'WAITING', Date.now(), trialWorkingFolder, form);
        this.jobQueue.push(trialJobId);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        return Promise.resolve(trialJobDetail);
    }
    async updateTrialJob(trialJobId, form) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`updateTrialJob failed: ${trialJobId} not found`);
        }
        await this.writeParameterFile(trialJobId, form.hyperParameters);
        return trialJobDetail;
    }
    get isMultiPhaseJobSupported() {
        return true;
    }
    async cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const trialJob = this.trialJobsMap.get(trialJobId);
        if (trialJob === undefined) {
            throw new Error(`trial job id ${trialJobId} not found`);
        }
        const index = this.jobQueue.indexOf(trialJobId);
        if (index >= 0) {
            this.jobQueue.splice(index, 1);
        }
        if (trialJob.rmMeta !== undefined) {
            const executor = this.trialExecutorMap.get(trialJob.id);
            if (executor === undefined) {
                throw new Error(`Invalid job id ${trialJobId}, cannot find executor`);
            }
            if (trialJob.status === 'UNKNOWN') {
                this.releaseTrialExecutor(trialJob);
                trialJob.status = 'USER_CANCELED';
                return;
            }
            const jobpidPath = this.getJobPidPath(trialJob.id);
            try {
                trialJob.isEarlyStopped = isEarlyStopped;
                await executor.killChildProcesses(jobpidPath);
                this.releaseTrialExecutor(trialJob);
            }
            catch (error) {
                this.log.error(`remoteTrainingService.cancelTrialJob: ${error.message}`);
            }
        }
        else {
            assert(isEarlyStopped === false, 'isEarlyStopped is not supposed to be true here.');
            trialJob.status = utils_1.getJobCancelStatus(isEarlyStopped);
        }
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIpConfig = JSON.parse(value);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.MACHINE_LIST:
                await this.setupConnections(value);
                this.gpuScheduler = new gpuScheduler_1.GPUScheduler(this.machineExecutorManagerMap);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG: {
                const remoteMachineTrailConfig = JSON.parse(value);
                if (remoteMachineTrailConfig === undefined) {
                    throw new Error('trial config parsed failed');
                }
                if (!fs.lstatSync(remoteMachineTrailConfig.codeDir)
                    .isDirectory()) {
                    throw new Error(`codeDir ${remoteMachineTrailConfig.codeDir} is not a directory`);
                }
                try {
                    await util_1.validateCodeDir(remoteMachineTrailConfig.codeDir);
                }
                catch (error) {
                    this.log.error(error);
                    return Promise.reject(new Error(error));
                }
                this.trialConfig = remoteMachineTrailConfig;
                break;
            }
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.MULTI_PHASE:
                this.isMultiPhase = (value === 'true' || value === 'True');
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.VERSION_CHECK:
                this.versionCheck = (value === 'true' || value === 'True');
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.LOG_COLLECTION:
                this.logCollection = value;
                break;
            default:
                throw new Error(`Uknown key: ${key}`);
        }
    }
    async getClusterMetadata(_key) {
        return "";
    }
    async cleanUp() {
        this.log.info('Stopping remote machine training service...');
        this.stopping = true;
        await Promise.race([utils_1.delay(10000), this.cleanupConnections()]);
    }
    updateGpuReservation() {
        if (this.gpuScheduler) {
            for (const [key, value] of this.trialJobsMap) {
                if (!['WAITING', 'RUNNING'].includes(value.status)) {
                    this.gpuScheduler.removeGpuReservation(key, this.trialJobsMap);
                }
            }
        }
    }
    async cleanupConnections() {
        try {
            for (const [rmMeta, executorManager] of this.machineExecutorManagerMap.entries()) {
                const jobpidPath = utils_1.unixPathJoin(this.getRemoteScriptsPath(rmMeta.username), 'pid');
                const executor = executorManager.getFirstExecutor();
                if (executor !== undefined) {
                    await executor.killChildProcesses(jobpidPath);
                    await executor.removeFolder(this.getRemoteScriptsPath(rmMeta.username));
                }
                executorManager.closeAllExecutor();
            }
        }
        catch (error) {
            this.log.error(`Cleanup connection exception, error is ${error.message}`);
        }
        return Promise.resolve();
    }
    async setupConnections(machineList) {
        this.log.debug(`Connecting to remote machines: ${machineList}`);
        const deferred = new ts_deferred_1.Deferred();
        const rmMetaList = JSON.parse(machineList);
        let connectedRMNum = 0;
        rmMetaList.forEach(async (rmMeta) => {
            rmMeta.occupiedGpuIndexMap = new Map();
            const executorManager = new remoteMachineData_1.ExecutorManager([], this.MAX_TRIAL_NUMBER_PER_EXECUTOR, rmMeta);
            const executor = await executorManager.getAvailableExecutor();
            this.machineExecutorManagerMap.set(rmMeta, executorManager);
            await this.initRemoteMachineOnConnected(rmMeta, executor);
            if (++connectedRMNum === rmMetaList.length) {
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
    async initRemoteMachineOnConnected(rmMeta, executor) {
        const nniRootDir = utils_1.unixPathJoin(utils_1.getRemoteTmpDir(this.remoteOS), 'nni');
        await executor.createFolder(this.remoteExpRootDir);
        const remoteGpuScriptCollectorDir = this.getRemoteScriptsPath(rmMeta.username);
        await executor.createFolder(remoteGpuScriptCollectorDir, true);
        await executor.allowPermission(false, nniRootDir, `${nniRootDir}/*`, `${nniRootDir}/scripts/*`);
        const script = util_1.getGpuMetricsCollectorBashScriptContent(remoteGpuScriptCollectorDir);
        executor.executeScript(script, false, true);
        const disposable = this.timer.subscribe(async () => {
            const cmdresult = await executor.readLastLines(utils_1.unixPathJoin(remoteGpuScriptCollectorDir, 'gpu_metrics'));
            if (cmdresult !== "") {
                rmMeta.gpuSummary = JSON.parse(cmdresult);
                if (rmMeta.gpuSummary.gpuCount === 0) {
                    this.log.warning(`No GPU found on remote machine ${rmMeta.ip}`);
                    this.timer.unsubscribe(disposable);
                }
            }
        });
    }
    async prepareTrialJob(trialJobId) {
        const deferred = new ts_deferred_1.Deferred();
        if (this.trialConfig === undefined) {
            throw new Error('trial config is not initialized');
        }
        if (this.gpuScheduler === undefined) {
            throw new Error('gpuScheduler is not initialized');
        }
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.INVALID_JOB_DETAIL, `Invalid job detail information for trial job ${trialJobId}`);
        }
        if (trialJobDetail.status !== 'WAITING') {
            deferred.resolve(true);
            return deferred.promise;
        }
        const rmScheduleResult = this.gpuScheduler.scheduleMachine(this.trialConfig.gpuNum, trialJobDetail);
        if (rmScheduleResult.resultType === remoteMachineData_1.ScheduleResultType.REQUIRE_EXCEED_TOTAL) {
            const errorMessage = `Required GPU number ${this.trialConfig.gpuNum} is too large, no machine can meet`;
            this.log.error(errorMessage);
            deferred.reject();
            throw new errors_1.NNIError(errors_1.NNIErrorNames.RESOURCE_NOT_AVAILABLE, errorMessage);
        }
        else if (rmScheduleResult.resultType === remoteMachineData_1.ScheduleResultType.SUCCEED
            && rmScheduleResult.scheduleInfo !== undefined) {
            const rmScheduleInfo = rmScheduleResult.scheduleInfo;
            const trialWorkingFolder = utils_1.unixPathJoin(this.remoteExpRootDir, 'trials', trialJobId);
            trialJobDetail.rmMeta = rmScheduleInfo.rmMeta;
            await this.allocateExecutorForTrial(trialJobDetail);
            await this.launchTrialOnScheduledMachine(trialJobId, trialWorkingFolder, trialJobDetail.form, rmScheduleInfo);
            trialJobDetail.status = 'RUNNING';
            trialJobDetail.url = `file://${rmScheduleInfo.rmMeta.ip}:${trialWorkingFolder}`;
            trialJobDetail.startTime = Date.now();
            this.trialJobsMap.set(trialJobId, trialJobDetail);
            deferred.resolve(true);
        }
        else if (rmScheduleResult.resultType === remoteMachineData_1.ScheduleResultType.TMP_NO_AVAILABLE_GPU) {
            this.log.info(`Right now no available GPU can be allocated for trial ${trialJobId}, will try to schedule later`);
            deferred.resolve(false);
        }
        else {
            deferred.reject(`Invalid schedule resutl type: ${rmScheduleResult.resultType}`);
        }
        return deferred.promise;
    }
    async launchTrialOnScheduledMachine(trialJobId, trialWorkingFolder, form, rmScheduleInfo) {
        if (this.trialConfig === undefined) {
            throw new Error('trial config is not initialized');
        }
        const cudaVisibleDevice = rmScheduleInfo.cudaVisibleDevice;
        const executor = this.trialExecutorMap.get(trialJobId);
        if (executor === undefined) {
            assert(false, 'ShellExecutor is undefined.');
            return;
        }
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`Can not get trial job detail for job: ${trialJobId}`);
        }
        const trialLocalTempFolder = path.join(this.expRootDir, 'trials-local', trialJobId);
        await executor.createFolder(trialWorkingFolder);
        await executor.createFolder(utils_1.unixPathJoin(trialWorkingFolder, '.nni'));
        let command;
        if (this.trialConfig.gpuNum === undefined) {
            command = this.trialConfig.command;
        }
        else {
            if (typeof cudaVisibleDevice === 'string' && cudaVisibleDevice.length > 0) {
                command = `CUDA_VISIBLE_DEVICES=${cudaVisibleDevice} ${this.trialConfig.command}`;
            }
            else {
                command = `CUDA_VISIBLE_DEVICES=" " ${this.trialConfig.command}`;
            }
        }
        const nniManagerIp = this.nniManagerIpConfig ? this.nniManagerIpConfig.nniManagerIp : utils_1.getIPV4Address();
        if (this.remoteRestServerPort === undefined) {
            const restServer = component.get(remoteMachineJobRestServer_1.RemoteMachineJobRestServer);
            this.remoteRestServerPort = restServer.clusterRestServerPort;
        }
        const version = this.versionCheck ? await utils_1.getVersion() : '';
        const runScriptTrialContent = typescript_string_operations_1.String.Format(remoteMachineData_1.REMOTEMACHINE_TRIAL_COMMAND_FORMAT, trialWorkingFolder, trialWorkingFolder, trialJobId, experimentStartupInfo_1.getExperimentId(), trialJobDetail.form.sequenceId.toString(), this.isMultiPhase, utils_1.unixPathJoin(trialWorkingFolder, '.nni', 'jobpid'), command, nniManagerIp, this.remoteRestServerPort, version, this.logCollection, utils_1.unixPathJoin(trialWorkingFolder, '.nni', 'code'));
        await util_1.execMkdir(path.join(trialLocalTempFolder, '.nni'));
        await util_1.execCopydir(this.trialConfig.codeDir, trialLocalTempFolder);
        const installScriptContent = containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT;
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'install_nni.sh'), installScriptContent, { encoding: 'utf8' });
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run.sh'), runScriptTrialContent, { encoding: 'utf8' });
        await this.writeParameterFile(trialJobId, form.hyperParameters);
        await executor.copyDirectoryToRemote(trialLocalTempFolder, trialWorkingFolder, this.remoteOS);
        executor.executeScript(utils_1.unixPathJoin(trialWorkingFolder, 'run.sh'), true, true);
    }
    getRmMetaByHost(host) {
        for (const rmMeta of this.machineExecutorManagerMap.keys()) {
            if (rmMeta.ip === host) {
                return rmMeta;
            }
        }
        throw new Error(`Host not found: ${host}`);
    }
    async updateTrialJobStatus(trialJob, executor) {
        const deferred = new ts_deferred_1.Deferred();
        const jobpidPath = this.getJobPidPath(trialJob.id);
        const trialReturnCodeFilePath = utils_1.unixPathJoin(this.remoteExpRootDir, 'trials', trialJob.id, '.nni', 'code');
        try {
            const isAlive = await executor.isProcessAlive(jobpidPath);
            if (!isAlive) {
                const trialReturnCode = await executor.getRemoteFileContent(trialReturnCodeFilePath);
                this.log.debug(`trailjob ${trialJob.id} return code: ${trialReturnCode}`);
                const match = trialReturnCode.trim()
                    .match(/^(\d+)\s+(\d+)$/);
                if (match !== null) {
                    const { 1: code, 2: timestamp } = match;
                    if (parseInt(code, 10) === 0) {
                        trialJob.status = 'SUCCEEDED';
                    }
                    else {
                        if (trialJob.isEarlyStopped === undefined) {
                            trialJob.status = 'FAILED';
                        }
                        else {
                            trialJob.status = utils_1.getJobCancelStatus(trialJob.isEarlyStopped);
                        }
                    }
                    trialJob.endTime = parseInt(timestamp, 10);
                    this.releaseTrialExecutor(trialJob);
                }
                this.log.debug(`trailJob status update: ${trialJob.id}, ${trialJob.status}`);
            }
            deferred.resolve(trialJob);
        }
        catch (error) {
            this.log.error(`Update job status exception, error is ${error.message}`);
            if (error instanceof errors_1.NNIError && error.name === errors_1.NNIErrorNames.NOT_FOUND) {
                deferred.resolve(trialJob);
            }
            else {
                trialJob.status = 'UNKNOWN';
                deferred.resolve(trialJob);
            }
        }
        return deferred.promise;
    }
    getRemoteScriptsPath(userName) {
        return utils_1.unixPathJoin(utils_1.getRemoteTmpDir(this.remoteOS), userName, 'nni', 'scripts');
    }
    getHostJobRemoteDir(jobId) {
        return utils_1.unixPathJoin(this.remoteExpRootDir, 'hostjobs', jobId);
    }
    getRemoteExperimentRootDir() {
        return utils_1.unixPathJoin(utils_1.getRemoteTmpDir(this.remoteOS), 'nni', 'experiments', experimentStartupInfo_1.getExperimentId());
    }
    get MetricsEmitter() {
        return this.metricsEmitter;
    }
    getJobPidPath(jobId) {
        const trialJobDetail = this.trialJobsMap.get(jobId);
        if (trialJobDetail === undefined) {
            throw new errors_1.NNIError(errors_1.NNIErrorNames.INVALID_JOB_DETAIL, `Invalid job detail information for trial job ${jobId}`);
        }
        return utils_1.unixPathJoin(trialJobDetail.workingDirectory, '.nni', 'jobpid');
    }
    async writeParameterFile(trialJobId, hyperParameters) {
        const executor = this.trialExecutorMap.get(trialJobId);
        if (executor === undefined) {
            throw new Error('ShellExecutor is undefined.');
        }
        const trialWorkingFolder = utils_1.unixPathJoin(this.remoteExpRootDir, 'trials', trialJobId);
        const trialLocalTempFolder = path.join(this.expRootDir, 'trials-local', trialJobId);
        const fileName = utils_1.generateParamFileName(hyperParameters);
        const localFilepath = path.join(trialLocalTempFolder, fileName);
        await fs.promises.writeFile(localFilepath, hyperParameters.value, { encoding: 'utf8' });
        await executor.copyFileToRemote(localFilepath, utils_1.unixPathJoin(trialWorkingFolder, fileName));
    }
};
RemoteMachineTrainingService = __decorate([
    component.Singleton,
    __param(0, component.Inject),
    __metadata("design:paramtypes", [observableTimer_1.ObservableTimer])
], RemoteMachineTrainingService);
exports.RemoteMachineTrainingService = RemoteMachineTrainingService;
