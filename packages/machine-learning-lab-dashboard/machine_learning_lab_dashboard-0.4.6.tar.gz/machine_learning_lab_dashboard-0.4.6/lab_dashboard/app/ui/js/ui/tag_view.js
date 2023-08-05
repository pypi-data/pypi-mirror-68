var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
define(["require", "exports", "./app", "../lib/weya/weya", "./cache", "./experiment_view"], function (require, exports, app_1, weya_1, cache_1, experiment_view_1) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class TagView {
        constructor(name) {
            this.name = name;
        }
        render() {
            this.elem = weya_1.Weya('div.container', $ => {
                this.experimentView = $('div.tag_runs', '');
            });
            this.renderTagRuns().then();
            return this.elem;
        }
        renderTagRuns() {
            return __awaiter(this, void 0, void 0, function* () {
                this.runs = (yield cache_1.getExperiments()).getByTag(this.name);
                this.experimentView.append(weya_1.Weya('div.info', $ => {
                    $('h1', this.name);
                }));
                this.runsView = new experiment_view_1.RunsView(this.runs, true);
                this.runsView.render(this.experimentView).then();
            });
        }
    }
    class TagHandler {
        constructor() {
            this.handleTag = (name) => {
                app_1.SCREEN.setView(new TagView(name));
            };
            app_1.ROUTER.route('tag/:name', [this.handleTag]);
        }
    }
    exports.TagHandler = TagHandler;
});
