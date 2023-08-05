var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "./app", "../lib/weya/weya", "./cache", "./run_ui", "./configs", "./indicators", "./view_components/format"], function (require, exports, app_1, weya_1, cache_1, run_ui_1, configs_1, indicators_1, format_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class RunView {
        constructor(run, isShowExperimentName) {
            this.onClick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                app_1.ROUTER.navigate(`/experiment/${this.run.experimentName}/${this.run.info.uuid}`);
            };
            this.run = run;
            this.isShowExperimentName = isShowExperimentName;
            this.runUI = run_ui_1.RunUI.create(this.run);
        }
        render() {
            this.elem = weya_1.Weya('div.run', {
                on: { click: this.onClick }
            }, $ => {
                let info = this.run.info;
                if (this.isShowExperimentName) {
                    $('h4', this.run.experimentName);
                }
                if (info.comment.trim() !== '') {
                    $('h3', info.comment);
                }
                $('h4', $ => {
                    $('label', `${info.uuid}`);
                });
                $('div', $ => {
                    $('i.fa.fa-history.key_icon');
                    $('span', info.commit_message);
                });
                $('div', $ => {
                    $('i.fa.fa-calendar.key_icon');
                    $('span', info.trial_date);
                    $('span.key_split', '');
                    $('i.fa.fa-clock.key_icon');
                    $('span', info.trial_time);
                });
                $('div', $ => {
                    $('i.fa.fa-save.key_icon');
                    let size = info.sqlite_size +
                        info.analytics_size +
                        info.checkpoints_size +
                        info.tensorboard_size;
                    $('span', format_1.formatSize(size));
                });
                this.indicatorsView = $('div.indicators.block');
                this.configsView = $('div.configs.block');
            });
            return this.elem;
        }
        load() {
            return __awaiter(this, void 0, void 0, function* () {
                this.values = yield this.runUI.loadValues();
                this.configs = yield this.runUI.loadConfigs();
            });
        }
        renderValues() {
            indicators_1.renderValues(this.indicatorsView, this.values);
        }
        renderConfigs(common) {
            configs_1.renderConfigs(this.configsView, this.configs, common);
        }
    }
    class RunsView {
        constructor(runs, isShowExperimentName) {
            this.runs = runs;
            this.isShowExperimentName = isShowExperimentName;
        }
        render(elem) {
            return __awaiter(this, void 0, void 0, function* () {
                this.elem = elem;
                let runViews = [];
                for (let t of this.runs) {
                    let rv = new RunView(t, this.isShowExperimentName);
                    this.elem.append(rv.render());
                    runViews.push(rv);
                }
                if (runViews.length == 0) {
                    return;
                }
                yield Promise.all(runViews.map(rv => rv.load()));
                let configs = {};
                let differentConfigs = new Set();
                for (let [k, v] of Object.entries(runViews[0].configs.configs)) {
                    configs[k] = v.value;
                }
                for (let rv of runViews) {
                    for (let [k, v] of Object.entries(rv.configs.configs)) {
                        if (differentConfigs.has(k)) {
                            continue;
                        }
                        if (configs[k] !== v.value) {
                            differentConfigs.add(k);
                        }
                    }
                }
                let common = new Set();
                for (let k in configs) {
                    if (!differentConfigs.has(k)) {
                        common.add(k);
                    }
                }
                for (let rv of runViews) {
                    rv.renderValues();
                    rv.renderConfigs(common);
                }
            });
        }
    }
    exports.RunsView = RunsView;
    class ExperimentView {
        constructor(name) {
            this.name = name;
        }
        render() {
            this.elem = weya_1.Weya('div.container', $ => {
                this.experimentView = $('div.experiment_single', '');
            });
            this.renderExperiment().then();
            return this.elem;
        }
        renderExperiment() {
            return __awaiter(this, void 0, void 0, function* () {
                this.experiment = (yield cache_1.getExperiments()).get(this.name);
                this.experimentView.append(weya_1.Weya('div.info', $ => {
                    $('h1', this.experiment.name);
                }));
                this.runsView = new RunsView(this.experiment.runs, false);
                this.runsView.render(this.experimentView).then();
            });
        }
    }
    class ExperimentHandler {
        constructor() {
            this.handleExperiment = (name) => {
                app_1.SCREEN.setView(new ExperimentView(name));
            };
            app_1.ROUTER.route('experiment/:name', [this.handleExperiment]);
        }
    }
    exports.ExperimentHandler = ExperimentHandler;
});
