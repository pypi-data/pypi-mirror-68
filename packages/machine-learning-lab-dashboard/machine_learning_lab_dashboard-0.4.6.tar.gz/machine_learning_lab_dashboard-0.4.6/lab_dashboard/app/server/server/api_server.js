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
const api_1 = require("../common/api");
const cache_1 = require("./experiments/cache");
const run_nodejs_1 = require("./run_nodejs");
const tensorboard_1 = require("./tensorboard");
const jupyter_1 = require("./jupyter");
const PATH = require("path");
const consts_1 = require("./consts");
const util_1 = require("./util");
const YAML = require("yaml");
let TENSORBOARD = null;
let JUPYTER = null;
function getRun(experimentName, runUuid) {
    return __awaiter(this, void 0, void 0, function* () {
        let experiment = yield cache_1.ExperimentsFactory.loadExperiment(experimentName);
        return run_nodejs_1.RunNodeJS.create(experiment.getRun(runUuid));
    });
}
class ApiServer extends api_1.Api {
    getExperiments() {
        return __awaiter(this, void 0, void 0, function* () {
            let experiments = yield cache_1.ExperimentsFactory.load();
            return experiments.toJSON();
        });
    }
    getIndicators(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(experimentName, runUuid);
            let indicators = yield run.getIndicators();
            return indicators.toJSON();
        });
    }
    getConfigs(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(experimentName, runUuid);
            let configs = yield run.getConfigs();
            return configs.toJSON();
        });
    }
    getDiff(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(experimentName, runUuid);
            return yield run.getDiff();
        });
    }
    getValues(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(experimentName, runUuid);
            return yield run.getValues();
        });
    }
    launchTensorboard(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let experiment = yield cache_1.ExperimentsFactory.loadExperiment(experimentName);
            let run = experiment.getRun(runUuid);
            if (TENSORBOARD != null) {
                TENSORBOARD.stop();
            }
            TENSORBOARD = new tensorboard_1.Tensorboard([run]);
            try {
                yield TENSORBOARD.start();
                return 'http://localhost:6006';
            }
            catch (e) {
                console.log(e);
                TENSORBOARD = null;
                return '';
            }
        });
    }
    launchTensorboards(runs) {
        return __awaiter(this, void 0, void 0, function* () {
            let runsList = [];
            for (let r of runs) {
                let experiment = yield cache_1.ExperimentsFactory.loadExperiment(r.experimentName);
                runsList.push(experiment.getRun(r.runUuid));
            }
            if (TENSORBOARD != null) {
                TENSORBOARD.stop();
            }
            TENSORBOARD = new tensorboard_1.Tensorboard(runsList);
            try {
                yield TENSORBOARD.start();
                return 'http://localhost:6006';
            }
            catch (e) {
                TENSORBOARD = null;
                return '';
            }
        });
    }
    launchJupyter(experimentName, runUuid, analyticsTemplate) {
        return __awaiter(this, void 0, void 0, function* () {
            let experiment = yield cache_1.ExperimentsFactory.loadExperiment(experimentName);
            let run = experiment.getRun(runUuid);
            if (JUPYTER == null) {
                JUPYTER = new jupyter_1.Jupyter();
                try {
                    yield JUPYTER.start();
                }
                catch (e) {
                    JUPYTER = null;
                    return '';
                }
            }
            return yield JUPYTER.setupTemplate(run, analyticsTemplate);
        });
    }
    getAnalyticsTemplates(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(experimentName, runUuid);
            let templateNames = [];
            let lab = yield run.getLab();
            for (let k in lab.analyticsTemplates) {
                templateNames.push(k);
            }
            return templateNames;
        });
    }
    removeRun(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                let run = yield getRun(experimentName, runUuid);
                yield run.remove();
                cache_1.ExperimentsFactory.cacheReset(experimentName, runUuid);
            }
            catch (e) {
            }
        });
    }
    cleanupCheckpoints(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(experimentName, runUuid);
            yield run.cleanupCheckpoints();
            cache_1.ExperimentsFactory.cacheReset(experimentName, runUuid);
        });
    }
    updateRun(experimentName, runUuid, data) {
        return __awaiter(this, void 0, void 0, function* () {
            let run = yield getRun(experimentName, runUuid);
            yield run.update(data);
            cache_1.ExperimentsFactory.cacheReset(experimentName, runUuid);
        });
    }
    saveDashboard(name, cells) {
        return __awaiter(this, void 0, void 0, function* () {
            let path = PATH.join(consts_1.LAB.path, ".lab_dashboard.yaml");
            let dashboards;
            try {
                let contents = yield util_1.readFile(path);
                dashboards = YAML.parse(contents);
            }
            catch (e) {
                dashboards = {};
            }
            dashboards[name] = cells;
            yield util_1.writeFile(path, YAML.stringify(dashboards));
        });
    }
    loadDashboards() {
        return __awaiter(this, void 0, void 0, function* () {
            let path = PATH.join(consts_1.LAB.path, ".lab_dashboard.yaml");
            let dashboards;
            try {
                let contents = yield util_1.readFile(path);
                dashboards = YAML.parse(contents);
            }
            catch (e) {
                dashboards = {};
            }
            return dashboards;
        });
    }
}
exports.API = new ApiServer();
