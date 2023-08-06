define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    class RunsTree {
        constructor(allRuns, runs) {
            this.runs = runs;
            this.fullMap = RunsTree.getRunIndexes(allRuns);
            this.treeMap = {};
            this.tree = [];
        }
        static getRunIndexes(runs) {
            let indexes = {};
            for (let runUI of runs) {
                let r = runUI.run;
                if (indexes[r.experimentName] == null) {
                    indexes[r.experimentName] = {};
                }
                indexes[r.experimentName][r.info.uuid] = runUI;
            }
            return indexes;
        }
        getList() {
            this.buildTree();
            let runs = [];
            for (let node of this.tree) {
                runs = runs.concat(this.nodeToList(node));
            }
            return runs;
        }
        getParent(run) {
            let uuid = run.run.info.load_run;
            if (uuid == null) {
                return null;
            }
            return this.fullMap[run.run.experimentName][uuid];
        }
        addRun(run) {
            let exp = run.run.experimentName;
            let uuid = run.run.info.uuid;
            if (this.treeMap[exp] != null && this.treeMap[exp][uuid] != null) {
                return;
            }
            let parentRun = this.getParent(run);
            let node = { run: run, children: [] };
            if (parentRun == null) {
                run.generations = 0;
                this.tree.push(node);
            }
            else {
                run.generations = parentRun.generations + 1;
                parentRun.children++;
                this.addRun(parentRun);
                this.treeMap[parentRun.run.experimentName][parentRun.run.info.uuid].children.push(node);
            }
            if (this.treeMap[exp] == null) {
                this.treeMap[exp] = {};
            }
            this.treeMap[exp][uuid] = node;
        }
        buildTree() {
            for (let run of this.runs) {
                this.addRun(run);
            }
        }
        nodeToList(node) {
            let runs = [node.run];
            for (let r of node.children) {
                runs = runs.concat(this.nodeToList(r));
            }
            return runs;
        }
    }
    exports.RunsTree = RunsTree;
});
