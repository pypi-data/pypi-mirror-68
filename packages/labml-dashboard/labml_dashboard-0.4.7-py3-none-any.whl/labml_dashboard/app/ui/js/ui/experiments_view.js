/*
This is not used anymore
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "./app", "../lib/weya/weya", "./cache", "./run_ui", "./indicators"], function (require, exports, app_1, weya_1, cache_1, run_ui_1, indicators_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class ExperimentView {
        constructor(e) {
            this.onClick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                app_1.ROUTER.navigate(`/experiment/${this.experiment.name}`);
            };
            this.experiment = e;
        }
        render() {
            let run = this.experiment.lastRun;
            this.elem = weya_1.Weya('div.experiment', {
                on: { click: this.onClick }
            }, $ => {
                $('h3', this.experiment.name);
                if (run != null) {
                    this.renderRun(run).then();
                }
            });
            return this.elem;
        }
        renderRun(run) {
            return __awaiter(this, void 0, void 0, function* () {
                let runUI = run_ui_1.RunUI.create(run);
                let values = yield runUI.loadValues();
                // let configs = await runUI.getConfigs()
                weya_1.Weya(this.elem, $ => {
                    $('div', $ => {
                        $('i.fa.fa-calendar.key_icon');
                        $('span', ` ${run.info.trial_date} `);
                        $('span.key_split', '');
                        $('i.fa.fa-clock.key_icon');
                        $('span', ` ${run.info.trial_time}`);
                    });
                    let indicatorsView = $('div.indicators.block');
                    // let configsView = <HTMLDivElement>$('div.configs.block')
                    indicators_1.renderValues(indicatorsView, values);
                    // renderConfigs(configsView, configs)
                });
            });
        }
    }
    class ExperimentsView {
        render() {
            this.elem = weya_1.Weya('div.container', $ => {
                $('h1', 'Experiments');
                this.experimentsList = $('div.experiments_list', '');
            });
            this.renderExperiments().then();
            return this.elem;
        }
        renderExperiments() {
            return __awaiter(this, void 0, void 0, function* () {
                this.experiments = yield cache_1.getExperiments();
                let views = [];
                for (let e of this.experiments.sorted()) {
                    views.push(new ExperimentView(e));
                }
                for (let v of views) {
                    this.experimentsList.append(v.render());
                }
            });
        }
    }
    class ExperimentsHandler {
        constructor() {
            this.handleExperiments = () => {
                app_1.ROUTER.navigate('table', { replace: true, trigger: true });
            };
            app_1.ROUTER.route('', [this.handleExperiments]);
        }
    }
    exports.ExperimentsHandler = ExperimentsHandler;
});
