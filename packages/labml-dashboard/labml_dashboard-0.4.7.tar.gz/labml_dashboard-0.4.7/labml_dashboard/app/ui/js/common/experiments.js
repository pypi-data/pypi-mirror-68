define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class Indicators {
        constructor(indicators) {
            this.indicators = indicators;
        }
        toJSON() {
            return this.indicators;
        }
    }
    exports.Indicators = Indicators;
    class Configs {
        constructor(configs) {
            for (let [k, v] of Object.entries(configs)) {
                if (v.is_explicitly_specified == null) {
                    v.is_explicitly_specified = false;
                }
            }
            this.configs = configs;
        }
        toJSON() {
            return this.configs;
        }
    }
    exports.Configs = Configs;
    exports.DEFAULT_RUN_MODEL = {
        uuid: '',
        comment: '',
        tags: [],
        commit: '',
        commit_message: '',
        notes: '',
        is_dirty: false,
        python_file: '',
        start_step: 0,
        trial_date: '2000-01-01',
        trial_time: '00:00:00',
        tensorboard_size: 0,
        checkpoints_size: 0,
        sqlite_size: 0,
        analytics_size: 0
    };
    class Run {
        constructor(experimentName, info) {
            this.experimentName = experimentName;
            this.info = info;
        }
        toJSON() {
            return this.info;
        }
        hash() {
            return `${this.experimentName}-${this.info.uuid}`;
        }
        static fixRunModel(experimentName, run) {
            let copy = JSON.parse(JSON.stringify(exports.DEFAULT_RUN_MODEL));
            if (run == null) {
                return copy;
            }
            if (run.tags == null) {
                run.tags = experimentName.split('_');
            }
            for (let k of Object.keys(exports.DEFAULT_RUN_MODEL)) {
                if (run[k] == null) {
                    run[k] = copy[k];
                }
            }
            return run;
        }
    }
    exports.Run = Run;
    class Experiment {
        constructor(experiment) {
            this.name = experiment.name;
            this.runs = experiment.runs.map(t => new Run(this.name, t));
            this.runs.sort((a, b) => {
                if (a.info.trial_date < b.info.trial_date) {
                    return -1;
                }
                else if (a.info.trial_date > b.info.trial_date) {
                    return +1;
                }
                else {
                    if (a.info.trial_time < b.info.trial_time) {
                        return -1;
                    }
                    else if (a.info.trial_time > b.info.trial_time) {
                        return +1;
                    }
                    else {
                        return 0;
                    }
                }
            });
        }
        get lastRun() {
            if (this.runs.length > 0) {
                return this.runs[this.runs.length - 1];
            }
            return null;
        }
        getRun(uuid) {
            for (let run of this.runs) {
                if (run.info.uuid === uuid) {
                    return run;
                }
            }
            throw Error(`Unknown run ${uuid}`);
        }
        toJSON() {
            return {
                name: this.name,
                runs: this.runs.map(t => t.toJSON())
            };
        }
    }
    exports.Experiment = Experiment;
    class Experiments {
        constructor(experiments) {
            this.experiments = {};
            for (let [k, e] of Object.entries(experiments)) {
                this.experiments[k] = new Experiment(e);
            }
        }
        sorted() {
            let res = [];
            for (let k in this.experiments) {
                res.push(this.experiments[k]);
            }
            return res.sort((a, b) => a.name < b.name ? -1 : a.name > b.name ? 1 : 0);
        }
        toJSON() {
            let res = {};
            for (let k in this.experiments) {
                res[k] = this.experiments[k].toJSON();
            }
            return res;
        }
        get(experimentName) {
            return this.experiments[experimentName];
        }
        getByTag(name) {
            let runs = [];
            for (let k in this.experiments) {
                let exp = this.experiments[k];
                for (let r of exp.runs) {
                    if (r.info.tags.includes(name)) {
                        runs.push(r);
                    }
                }
            }
            return runs;
        }
    }
    exports.Experiments = Experiments;
});
