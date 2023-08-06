# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan import g
from suanpan.api.requests import affinity


def listComponents(limit=9999):
    return affinity.post("/component/list", json={"limit": limit})["list"]


def shareComponent(componentId, userId, name):
    return affinity.post(
        "/component/share",
        json={"id": componentId, "targetUserId": userId, "name": name},
    )


def exportModel(portId, name, appId=None, nodeId=None, overwrite=False):
    return affinity.post(
        "/component/export/model",
        json={
            "id": appId or g.appId,
            "nodeId": nodeId or g.nodeId,
            "portId": portId,
            "name": name,
            "overwrite": overwrite,
        },
    )


def checkAppStatus(appId=None):
    return affinity.post("/app/status", json={"id": appId or g.appId})


# mode: runStart, runStop, runStartStop
def runApp(nodeId, appId=None, mode="runStart"):
    return affinity.post(
        "/app/run", json={"id": appId or g.appId, "nodeId": nodeId, "type": mode}
    )


def startAppCron(
    period, mode, startEffectTime, endEffectTime, nodeId, config, appId=None
):
    return affinity.post(
        "/app/cron/start",
        json={
            "id": appId or g.appId,
            "cronConfig": {
                "period": period,
                "runType": mode,
                "startEffectTime": startEffectTime,
                "endEffectTime": endEffectTime,
                "nodeId": nodeId,
                "config": config,
            },
        },
    )


def stopAppCron(appId=None):
    return affinity.post("/app/cron/stop", json={"id": appId or g.appId})


def createApp(appName, appType, dirId=None):
    return affinity.post(
        "/app/create", json={"name": appName, "dir": dirId, "type": appType}
    )


def deleteApp(appId=None):
    return affinity.post("/app/del", json={"id": appId or g.appId})


def copyApp(name, appType, appId=None, withData=False, description=None, dirId=None):
    return affinity.post(
        "/app/duplicate",
        json={
            "id": appId or g.appId,
            "name": name,
            "dir": dirId,
            "type": appType,
            "withData": withData,
            "description": description,
        },
    )
