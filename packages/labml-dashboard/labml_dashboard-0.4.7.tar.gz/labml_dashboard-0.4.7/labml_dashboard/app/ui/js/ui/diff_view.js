var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "./app", "../lib/weya/weya", "./cache", "./run_ui", "./hljs"], function (require, exports, app_1, weya_1, cache_1, run_ui_1, hljs_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class DiffView {
        constructor(experimentName, runUuid) {
            this.experimentName = experimentName;
            this.runUuid = runUuid;
        }
        render() {
            this.elem = weya_1.Weya('div.container', $ => {
                this.diffView = $('div.diff', '');
            });
            this.renderRun().then();
            return this.elem;
        }
        renderRun() {
            return __awaiter(this, void 0, void 0, function* () {
                let experiment = (yield cache_1.getExperiments()).get(this.experimentName);
                this.run = experiment.getRun(this.runUuid);
                this.runUI = run_ui_1.RunUI.create(this.run);
                this.diff = yield this.runUI.loadDiff();
                let info = this.run.info;
                let h = hljs_1.highlight('diff', this.diff, true, null);
                let diffPre;
                weya_1.Weya(this.diffView, $ => {
                    diffPre = $('pre');
                });
                diffPre.innerHTML = h.value;
            });
        }
    }
    class DiffHandler {
        constructor() {
            this.handleRun = (name, runUuid) => {
                app_1.SCREEN.setView(new DiffView(name, runUuid));
            };
            app_1.ROUTER.route('experiment/:name/:runUuid/diff', [this.handleRun]);
        }
    }
    exports.DiffHandler = DiffHandler;
});
