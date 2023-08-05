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
const sqlite3 = require("sqlite3");
const experiments_1 = require("../common/experiments");
const PATH = require("path");
const YAML = require("yaml");
const consts_1 = require("./consts");
const util_1 = require("./util");
const UPDATABLE_KEYS = new Set(['comment', 'notes', 'tags']);
const USE_CACHE = true;
const USE_VALUES_CACHE = false;
class RunNodeJS {
    constructor(run) {
        this.run = run;
    }
    static create(run) {
        return new RunNodeJS(run);
    }
    loadDatabase() {
        if (this.db != null) {
            return new Promise(resolve => {
                resolve();
            });
        }
        let path = PATH.join(consts_1.LAB.experiments, this.run.experimentName, this.run.info.uuid, 'sqlite.db');
        return new Promise((resolve, reject) => {
            util_1.exists(path).then((isExists) => {
                if (!isExists) {
                    return reject(false);
                }
                this.db = new sqlite3.Database(path, sqlite3.OPEN_READONLY, err => {
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve();
                    }
                });
            });
        });
    }
    getLastValue() {
        return new Promise((resolve, reject) => {
            this.db.all(`SELECT a.* FROM scalars AS a
            INNER JOIN (
                SELECT indicator, MAX(step) AS step 
                FROM scalars
                GROUP BY indicator
            ) b ON a.indicator = b.indicator AND a.step = b.step`, (err, rows) => {
                if (err) {
                    reject(err);
                }
                else {
                    let values = {};
                    for (let row of rows) {
                        values[row.indicator] = row;
                    }
                    resolve(values);
                }
            });
        });
    }
    getIndicators() {
        return __awaiter(this, void 0, void 0, function* () {
            // TODO: Caching
            if (!USE_CACHE || this.indicators == null) {
                let contents = yield util_1.readFile(PATH.join(consts_1.LAB.experiments, this.run.experimentName, this.run.info.uuid, 'indicators.yaml'));
                this.indicators = new experiments_1.Indicators(YAML.parse(contents));
            }
            return this.indicators;
        });
    }
    getConfigs() {
        return __awaiter(this, void 0, void 0, function* () {
            if (!USE_CACHE || this.configs == null) {
                try {
                    let contents = yield util_1.readFile(PATH.join(consts_1.LAB.experiments, this.run.experimentName, this.run.info.uuid, 'configs.yaml'));
                    this.configs = new experiments_1.Configs(YAML.parse(contents));
                }
                catch (e) {
                    return new experiments_1.Configs({});
                }
            }
            return this.configs;
        });
    }
    getDiff() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield util_1.readFile(PATH.join(consts_1.LAB.experiments, this.run.experimentName, this.run.info.uuid, 'source.diff'));
        });
    }
    getValues() {
        return __awaiter(this, void 0, void 0, function* () {
            if (USE_VALUES_CACHE && this.values != null) {
                return this.values;
            }
            // console.log("loading values")
            try {
                yield this.loadDatabase();
            }
            catch (e) {
                this.db = null;
                if (e === false) {
                    // console.log(
                    //     `SQLite db is missing ${this.run.experimentName} : ${this.run.info.uuid}`)
                }
                else {
                    console.log(`SQLite connect failed ${this.run.experimentName} : ${this.run.info.uuid}`, e);
                }
                return {};
            }
            let indicators = yield this.getIndicators();
            // console.log(indicators)
            let values = {};
            try {
                values = yield this.getLastValue();
            }
            catch (e) {
                console.log('Couldnt read from SQLite db', this.run.experimentName, this.run.info.uuid, e);
                return {};
            }
            for (let [k, ind] of Object.entries(indicators.indicators)) {
                if (ind.class_name == null) {
                    continue;
                }
                let key = ind.class_name.indexOf('Scalar') !== -1
                    ? ind.name
                    : `${ind.name}.mean`;
                if (!ind.is_print) {
                    delete values[key];
                }
            }
            this.values = values;
            return values;
        });
    }
    getLab() {
        return __awaiter(this, void 0, void 0, function* () {
            // let lab = new Lab(this.run.info.python_file)
            // await lab.load()
            //
            // return lab
            return consts_1.LAB;
        });
    }
    remove() {
        return __awaiter(this, void 0, void 0, function* () {
            let path = PATH.join(consts_1.LAB.experiments, this.run.experimentName, this.run.info.uuid);
            yield util_1.rmtree(path);
            let analytics = PATH.join(consts_1.LAB.analytics, this.run.experimentName, this.run.info.uuid);
            yield util_1.rmtree(analytics);
        });
    }
    update(data) {
        return __awaiter(this, void 0, void 0, function* () {
            for (let k in data) {
                if (!UPDATABLE_KEYS.has(k)) {
                    return;
                }
            }
            let path = PATH.join(consts_1.LAB.experiments, this.run.experimentName, this.run.info.uuid, 'run.yaml');
            let contents = yield util_1.readFile(path);
            let run = YAML.parse(contents);
            run = experiments_1.Run.fixRunModel(this.run.experimentName, run);
            for (let k in data) {
                run[k] = data[k];
            }
            yield util_1.writeFile(path, YAML.stringify(run));
        });
    }
    cleanupCheckpoints() {
        return __awaiter(this, void 0, void 0, function* () {
            let path = PATH.join(consts_1.LAB.experiments, this.run.experimentName, this.run.info.uuid, 'checkpoints');
            if (!(yield util_1.exists(path))) {
                return;
            }
            let checkpoints = yield util_1.readdir(path);
            if (checkpoints.length == 0) {
                return;
            }
            let last = parseInt(checkpoints[0]);
            for (let c of checkpoints) {
                if (last < parseInt(c)) {
                    last = parseInt(c);
                }
            }
            for (let c of checkpoints) {
                if (last !== parseInt(c)) {
                    yield util_1.rmtree(PATH.join(path, c));
                }
            }
        });
    }
}
exports.RunNodeJS = RunNodeJS;
