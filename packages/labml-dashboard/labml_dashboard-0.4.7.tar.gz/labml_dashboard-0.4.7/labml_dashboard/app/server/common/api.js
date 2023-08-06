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
class Api {
    getExperiments() {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    getIndicators(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    getConfigs(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    getDiff(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    getValues(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    launchTensorboard(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    launchTensorboards(runs) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    launchJupyter(experimentName, runUuid, analyticsTemplate) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    getAnalyticsTemplates(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    removeRun(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    cleanupCheckpoints(experimentName, runUuid) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    updateRun(experimentName, runUuid, data) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    saveDashboard(name, cells) {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
    loadDashboards() {
        return __awaiter(this, void 0, void 0, function* () {
            return null;
        });
    }
}
exports.Api = Api;
exports.API_SPEC = new Api();
