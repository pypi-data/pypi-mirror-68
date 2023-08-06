"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const YAML = require("yaml");
const PATH = require("path");
const experiments_1 = require("../../common/experiments");
const consts_1 = require("../consts");
const util_1 = require("../util");
const run_nodejs_1 = require("../run_nodejs");
class CacheEntry {
    constructor() {
        this.minDelay = 5 * 1000; // 5 seconds
        this.maxDelay = 2 * 60 * 60 * 1000; // 2 hours
        this.exponentialFactor = 1.5;
        this.lastLoaded = 0;
        this.delay = this.minDelay;
    }
    get() {
        return __awaiter(this, void 0, void 0, function* () {
            let now = (new Date()).getTime();
            if (this.cached == null || this.lastLoaded + this.delay < now) {
                let loaded = yield this.load();
                if (this.cached == null || this.isUpdated(this.cached, loaded)) {
                    this.delay = Math.max(this.minDelay, this.delay / this.exponentialFactor);
                    // console.log("Reduced checking time to ", this.delay)
                }
                else {
                    this.delay = Math.min(this.maxDelay, this.delay * this.exponentialFactor);
                    // console.log("Extended checking time to ", this.delay)
                }
                this.cached = loaded;
                this.lastLoaded = now;
            }
            return this.cached;
        });
    }
    reset() {
        this.cached = null;
    }
}
class RunModelCacheEntry extends CacheEntry {
    constructor(experimentName, runUuid) {
        super();
        this.experimentName = experimentName;
        this.runUuid = runUuid;
    }
    getMaxStep(run) {
        let maxStep = 0;
        for (let [k, value] of Object.entries(run.values)) {
            maxStep = Math.max(maxStep, value.step);
        }
        return maxStep;
    }
    isUpdated(original, loaded) {
        return this.getMaxStep(original) !== this.getMaxStep(loaded);
    }
    load() {
        return __awaiter(this, void 0, void 0, function* () {
            // console.log("loaded", this.experimentName, this.runUuid)
            let contents = yield util_1.readFile(PATH.join(consts_1.LAB.experiments, this.experimentName, this.runUuid, 'run.yaml'));
            let res = YAML.parse(contents);
            res = experiments_1.Run.fixRunModel(this.experimentName, res);
            res.uuid = this.runUuid;
            res.checkpoints_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.experiments, this.experimentName, this.runUuid, 'checkpoints'));
            res.tensorboard_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.experiments, this.experimentName, this.runUuid, 'tensorboard'));
            res.sqlite_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.experiments, this.experimentName, this.runUuid, 'sqlite.db'));
            res.analytics_size = yield util_1.getDiskUsage(PATH.join(consts_1.LAB.analytics, this.experimentName, this.runUuid));
            let run = run_nodejs_1.RunNodeJS.create(new experiments_1.Run(this.experimentName, res));
            res.values = yield run.getValues();
            res.configs = (yield run.getConfigs()).configs;
            return res;
        });
    }
}
class ExperimentRunsSetCacheEntry extends CacheEntry {
    constructor() {
        super();
        this.maxDelay = 30 * 1000;
    }
    isUpdated(original, loaded) {
        for (let [e, runs] of Object.entries(loaded)) {
            if (runs == null) {
                return true;
            }
            for (let r of runs.keys()) {
                if (original[e][r] == null) {
                    return true;
                }
            }
        }
        return false;
    }
    load() {
        return __awaiter(this, void 0, void 0, function* () {
            let experiments = yield util_1.readdir(consts_1.LAB.experiments);
            let res = {};
            for (let e of experiments) {
                res[e] = new Set(yield util_1.readdir(PATH.join(consts_1.LAB.experiments, e)));
            }
            return res;
        });
    }
}
class Cache {
    constructor() {
        this.experimentRunsSet = new ExperimentRunsSetCacheEntry();
        this.runs = {};
    }
    getRun(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            if (this.runs[experimentName] == null) {
                this.runs[experimentName] = {};
            }
            if (this.runs[experimentName][runUuid] == null) {
                this.runs[experimentName][runUuid] = new RunModelCacheEntry(experimentName, runUuid);
            }
            return yield this.runs[experimentName][runUuid].get();
        });
    }
    getExperiment(name) {
        return __awaiter(this, void 0, void 0, function* () {
            let promises = [];
            for (let r of (yield this.experimentRunsSet.get())[name].keys()) {
                promises.push(this.getRun(name, r));
            }
            let data = yield Promise.all(promises);
            return new experiments_1.Experiment({ name: name, runs: data });
        });
    }
    getAll() {
        return __awaiter(this, void 0, void 0, function* () {
            let promises = [];
            for (let e of Object.keys(yield this.experimentRunsSet.get())) {
                promises.push(this.getExperiment(e));
            }
            let experimentsList = yield Promise.all(promises);
            let experiments = {};
            for (let e of experimentsList) {
                experiments[e.name] = e;
            }
            return new experiments_1.Experiments(experiments);
        });
    }
    resetRun(experimentName, runUuid) {
        if (this.runs[experimentName] != null && this.runs[experimentName][runUuid] != null) {
            // console.log('resetCache', experimentName, runUuid)
            this.runs[experimentName][runUuid].reset();
        }
        this.experimentRunsSet.reset();
    }
}
const _CACHE = new Cache();
class ExperimentsFactory {
    static loadExperiment(name) {
        return __awaiter(this, void 0, void 0, function* () {
            return yield _CACHE.getExperiment(name);
        });
    }
    static load() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield _CACHE.getAll();
        });
    }
    static cacheReset(experimentName, runUuid) {
        // console.log('reset', experimentName, runUuid)
        _CACHE.resetRun(experimentName, runUuid);
    }
}
exports.ExperimentsFactory = ExperimentsFactory;
