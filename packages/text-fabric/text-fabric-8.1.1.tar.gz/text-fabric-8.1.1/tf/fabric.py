import os

"""Defined the main class.

Also lists the precomputation steps.
"""

import collections
from .parameters import VERSION, NAME, APIREF, LOCATIONS
from .core.data import Data, WARP, WARP2_DEFAULT, MEM_MSG
from .core.helpers import (
    itemize,
    setDir,
    expandDir,
    collectFormats,
    cleanName,
    check32,
    console,
    makeExamples,
)
from .core.timestamp import Timestamp
from .core.prepare import (
    levels,
    order,
    rank,
    levUp,
    levDown,
    boundary,
    sections,
    structure,
)
from .core.api import (
    Api,
    NodeFeature,
    EdgeFeature,
    OtypeFeature,
    OslotsFeature,
    Computed,
    addSortKey,
    addOtype,
    addLocality,
    addRank,
    addText,
    addSearch,
)
from .convert.mql import MQL, tfFromMql


PRECOMPUTE = (
    (False, "__levels__", levels, WARP),
    (False, "__order__", order, WARP[0:2] + ("__levels__",)),
    (False, "__rank__", rank, (WARP[0], "__order__")),
    (False, "__levUp__", levUp, WARP[0:2] + ("__rank__",)),
    (False, "__levDown__", levDown, (WARP[0], "__levUp__", "__rank__")),
    (False, "__boundary__", boundary, WARP[0:2] + ("__rank__",)),
    (True, "__sections__", sections, WARP + ("__levUp__", "__levels__")),
    (True, "__structure__", structure, WARP + ("__rank__", "__levUp__",)),
)
"""Precomputation steps.

Each step corresponds to a precomputation task.

A task is specified by a tuple containing:

Parameters
----------
dep: boolean
    Whether the step is dependent on the presence of additional features.
    Only relevant for the precomputation of section structure:
    that should only happen if there are section features.
name: string
    The name of the result of a precomputed task.
    The result is a blob of data that can be loaded and compressed just as ordinary features.
function: function
    The function that performs the precomputation task.
    These functions are defined in `tf.core.prepare`.
dependencies: strings
    The remaining parts of the tuple are the names of precomputed features
    that must be coomputed before and whose results are passed as argument
    to the function that executes the precomputation.

For a description of what the steps are for, see the functions
in `tf.core.prepare`.
"""
KIND = dict(__sections__="section", __structure__="structure")


class Fabric(object):
    """Main class of the TF package.

    Top level management of

    *   locating tf feature files
    *   loading and saving feature data
    *   precomputing auxiliary data
    *   caching precomputed and compressed data
    """

    def __init__(self, locations=None, modules=None, silent=False):
        self.silent = silent
        self.tm = Timestamp()
        self.tm.setSilent(silent)
        self.banner = f"This is {NAME} {VERSION}"
        self.version = VERSION
        (on32, warn, msg) = check32()
        if on32:
            self.tm.info(warn, tm=False)
        if msg:
            self.tm.info(msg, tm=False)
        self.tm.info(
            f"""{self.banner}
Api reference : {APIREF}
""",
            tm=False,
        )
        self.good = True

        if modules is None:
            modules = [""]
        if type(modules) is str:
            modules = [x.strip() for x in itemize(modules, "\n")]
        self.modules = modules

        if locations is None:
            locations = LOCATIONS
        if type(locations) is str:
            locations = [x.strip() for x in itemize(locations, "\n")]
        setDir(self)
        self.locations = []
        for loc in locations:
            self.locations.append(expandDir(self, loc))

        self.locationRep = "\n\t".join(
            "\n\t".join(f"{l}/{f}" for f in self.modules) for l in self.locations
        )
        self.featuresRequested = []
        self._makeIndex()

    def load(self, features, add=False, silent=None):
        if silent is not None:
            wasSilent = self.tm.isSilent()
            self.tm.setSilent(silent)
        self.tm.indent(level=0, reset=True)
        self.tm.info("loading features ...")
        self.sectionsOK = True
        self.structureOK = True
        self.good = True
        if self.good:
            featuresRequested = (
                itemize(features) if type(features) is str else sorted(features)
            )
            if add:
                self.featuresRequested += featuresRequested
            else:
                self.featuresRequested = featuresRequested
            for fName in list(WARP):
                self._loadFeature(fName, optional=fName == WARP[2])
        if self.good:
            self.textFeatures = set()
            if WARP[2] in self.features:
                otextMeta = self.features[WARP[2]].metaData
                for otextMod in self.features:
                    if otextMod.startswith(WARP[2] + "@"):
                        self._loadFeature(otextMod)
                        otextMeta.update(self.features[otextMod].metaData)
                self.sectionFeats = itemize(otextMeta.get("sectionFeatures", ""), ",")
                self.sectionTypes = itemize(otextMeta.get("sectionTypes", ""), ",")
                self.structureFeats = itemize(
                    otextMeta.get("structureFeatures", ""), ","
                )
                self.structureTypes = itemize(otextMeta.get("structureTypes", ""), ",")
                (self.cformats, self.formatFeats) = collectFormats(otextMeta)
                if not (0 < len(self.sectionTypes) <= 3) or not (
                    0 < len(self.sectionFeats) <= 3
                ):
                    if not add:
                        self.tm.warning(
                            f"Dataset without sections in {WARP[2]}:"
                            f"no section functions in the T-API"
                        )
                    self.sectionsOK = False
                else:
                    self.textFeatures |= set(self.sectionFeats)
                    self.sectionFeatsWithLanguage = tuple(
                        f
                        for f in self.features
                        if f == self.sectionFeats[0]
                        or f.startswith(f"{self.sectionFeats[0]}@")
                    )
                    self.textFeatures |= set(self.sectionFeatsWithLanguage)
                if not self.structureTypes or not self.structureFeats:
                    if not add:
                        self.tm.warning(
                            f"Dataset without structure sections in {WARP[2]}:"
                            f"no structure functions in the T-API"
                        )
                    self.structureOK = False
                else:
                    self.textFeatures |= set(self.structureFeats)

                self.textFeatures |= set(self.formatFeats)

                for fName in self.textFeatures:
                    self._loadFeature(fName)

            else:
                self.sectionsOK = False
                self.structureOK = False

        if self.good:
            self._precompute()
        if self.good:
            for fName in self.featuresRequested:
                self._loadFeature(fName)
        if not self.good:
            self.tm.indent(level=0)
            self.tm.error("Not all features could be loaded/computed")
            self.tm.cache()
            result = False
        elif add:
            try:
                self._updateApi()
            except MemoryError:
                console(MEM_MSG)
                result = False
        else:
            try:
                result = self._makeApi()
            except MemoryError:
                console(MEM_MSG)
                result = False
        if silent is not None:
            self.tm.setSilent(wasSilent)
        if not add:
            return result

    def explore(self, silent=None, show=True):
        if silent is not None:
            wasSilent = self.tm.isSilent()
            self.tm.setSilent(silent)
        nodes = set()
        edges = set()
        configs = set()
        computeds = set()
        for (fName, fObj) in self.features.items():
            fObj.load(metaOnly=True)
            dest = None
            if fObj.method:
                dest = computeds
            elif fObj.isConfig:
                dest = configs
            elif fObj.isEdge:
                dest = edges
            else:
                dest = nodes
            dest.add(fName)
        self.tm.info(
            "Feature overview: {} for nodes; {} for edges; {} configs; {} computed".format(
                len(nodes), len(edges), len(configs), len(computeds),
            )
        )
        self.featureSets = dict(
            nodes=nodes, edges=edges, configs=configs, computeds=computeds
        )
        if silent is not None:
            self.tm.setSilent(wasSilent)
        if show:
            return dict(
                (kind, tuple(sorted(kindSet)))
                for (kind, kindSet) in sorted(
                    self.featureSets.items(), key=lambda x: x[0]
                )
            )

    def loadAll(self, silent=None):
        api = self.load("", silent=silent)
        allFeatures = self.explore(silent=silent or True, show=True)
        loadableFeatures = allFeatures["nodes"] + allFeatures["edges"]
        self.load(loadableFeatures, add=True, silent=silent)
        return api

    def clearCache(self):
        for (fName, fObj) in self.features.items():
            fObj.cleanDataBin()

    def save(
        self,
        nodeFeatures={},
        edgeFeatures={},
        metaData={},
        location=None,
        module=None,
        silent=None,
    ):
        good = True
        if silent is not None:
            wasSilent = self.tm.isSilent()
            self.tm.setSilent(silent)
        self.tm.indent(level=0, reset=True)
        self._getWriteLoc(location=location, module=module)
        configFeatures = dict(
            f
            for f in metaData.items()
            if f[0] != "" and f[0] not in nodeFeatures and f[0] not in edgeFeatures
        )
        self.tm.info(
            "Exporting {} node and {} edge and {} config features to {}:".format(
                len(nodeFeatures),
                len(edgeFeatures),
                len(configFeatures),
                self.writeDir,
            )
        )
        todo = []
        for (fName, data) in sorted(nodeFeatures.items()):
            todo.append((fName, data, False, False))
        for (fName, data) in sorted(edgeFeatures.items()):
            todo.append((fName, data, True, False))
        for (fName, data) in sorted(configFeatures.items()):
            todo.append((fName, data, None, True))
        total = collections.Counter()
        failed = collections.Counter()
        maxSlot = None
        maxNode = None
        slotType = None
        if WARP[0] in nodeFeatures:
            self.tm.info(f"VALIDATING {WARP[1]} feature")
            otypeData = nodeFeatures[WARP[0]]
            if type(otypeData) is tuple:
                (otypeData, slotType, maxSlot, maxNode) = otypeData
            elif 1 in otypeData:
                slotType = otypeData[1]
                maxSlot = max(n for n in otypeData if otypeData[n] == slotType)
                maxNode = max(otypeData)
        if WARP[1] in edgeFeatures:
            self.tm.info(f"VALIDATING {WARP[1]} feature")
            oslotsData = edgeFeatures[WARP[1]]
            if type(oslotsData) is tuple:
                (oslotsData, maxSlot, maxNode) = oslotsData
            if maxSlot is None or maxNode is None:
                self.tm.error(f"ERROR: cannot check validity of {WARP[1]} feature")
                good = False
            else:
                self.tm.info(f"maxSlot={maxSlot:>11}")
                self.tm.info(f"maxNode={maxNode:>11}")
                maxNodeInData = max(oslotsData)
                minNodeInData = min(oslotsData)

                mappedSlotNodes = []
                unmappedNodes = []
                fakeNodes = []

                start = min((maxSlot + 1, minNodeInData))
                end = max((maxNode, maxNodeInData))
                for n in range(start, end + 1):
                    if n in oslotsData:
                        if n <= maxSlot:
                            mappedSlotNodes.append(n)
                        elif n > maxNode:
                            fakeNodes.append(n)
                    else:
                        if maxSlot < n <= maxNode:
                            unmappedNodes.append(n)

                if mappedSlotNodes:
                    self.tm.error(f"ERROR: {WARP[1]} maps slot nodes")
                    self.tm.error(makeExamples(mappedSlotNodes), tm=False)
                    good = False
                if fakeNodes:
                    self.tm.error(
                        f"ERROR: {WARP[1]} maps nodes that are not in {WARP[0]}"
                    )
                    self.tm.error(makeExamples(fakeNodes), tm=False)
                    good = False
                if unmappedNodes:
                    self.tm.error(f"ERROR: {WARP[1]} fails to map nodes:")
                    unmappedByType = {}
                    for n in unmappedNodes:
                        unmappedByType.setdefault(
                            otypeData.get(n, "_UNKNOWN_"), []
                        ).append(n)
                    for (nType, nodes) in sorted(
                        unmappedByType.items(), key=lambda x: (-len(x[1]), x[0]),
                    ):
                        self.tm.error(
                            f"--- unmapped {nType:<10} : {makeExamples(nodes)}"
                        )
                    good = False

            if good:
                self.tm.info(f"OK: {WARP[1]} is valid")

        for (fName, data, isEdge, isConfig) in todo:
            edgeValues = False
            fMeta = {}
            fMeta.update(metaData.get("", {}))
            fMeta.update(metaData.get(fName, {}))
            if fMeta.get("edgeValues", False):
                edgeValues = True
            if "edgeValues" in fMeta:
                del fMeta["edgeValues"]
            fObj = Data(
                f"{self.writeDir}/{fName}.tf",
                self.tm,
                data=data,
                metaData=fMeta,
                isEdge=isEdge,
                isConfig=isConfig,
                edgeValues=edgeValues,
            )
            tag = "config" if isConfig else "edge" if isEdge else "node"
            if fObj.save(nodeRanges=fName == WARP[0], overwrite=True):
                total[tag] += 1
            else:
                failed[tag] += 1
        self.tm.indent(level=0)
        self.tm.info(
            f"""Exported {total["node"]} node features"""
            f""" and {total["edge"]} edge features"""
            f""" and {total["config"]} config features"""
            f""" to {self.writeDir}"""
        )
        if len(failed):
            for (tag, nf) in sorted(failed.items()):
                self.tm.error(f"Failed to export {nf} {tag} features")
            good = False

        if silent is not None:
            self.tm.setSilent(wasSilent)
        return good

    def exportMQL(self, mqlName, mqlDir):
        self.tm.indent(level=0, reset=True)
        mqlDir = expandDir(self, mqlDir)

        mqlNameClean = cleanName(mqlName)
        mql = MQL(mqlDir, mqlNameClean, self.features, self.tm)
        mql.write()

    def importMQL(self, mqlFile, slotType=None, otext=None, meta=None):
        self.tm.indent(level=0, reset=True)
        (good, nodeFeatures, edgeFeatures, metaData) = tfFromMql(
            mqlFile, self.tm, slotType=slotType, otext=otext, meta=meta
        )
        if good:
            self.save(
                nodeFeatures=nodeFeatures, edgeFeatures=edgeFeatures, metaData=metaData
            )

    def _loadFeature(self, fName, optional=False):
        if not self.good:
            return False
        silent = self.tm.isSilent()
        if fName not in self.features:
            if not optional:
                self.tm.error(f'Feature "{fName}" not available in\n{self.locationRep}')
                self.good = False
        else:
            # if not self.features[fName].load(silent=silent or (fName not in self.featuresRequested)):
            if not self.features[fName].load(silent=silent):
                self.good = False

    def _makeIndex(self):
        self.features = {}
        self.featuresIgnored = {}
        tfFiles = {}
        for loc in self.locations:
            for mod in self.modules:
                dirF = f"{loc}/{mod}"
                if not os.path.exists(dirF):
                    continue
                with os.scandir(dirF) as sd:
                    files = tuple(
                        e.name for e in sd if e.is_file() and e.name.endswith(".tf")
                    )
                for fileF in files:
                    (fName, ext) = os.path.splitext(fileF)
                    tfFiles.setdefault(fName, []).append(f"{dirF}/{fileF}")
        for (fName, featurePaths) in sorted(tfFiles.items()):
            chosenFPath = featurePaths[-1]
            for featurePath in sorted(set(featurePaths[0:-1])):
                if featurePath != chosenFPath:
                    self.featuresIgnored.setdefault(fName, []).append(featurePath)
            self.features[fName] = Data(chosenFPath, self.tm)
        self._getWriteLoc()
        self.tm.info(
            "{} features found and {} ignored".format(
                len(tfFiles), sum(len(x) for x in self.featuresIgnored.values()),
            ),
            tm=False,
        )

        good = True
        for fName in WARP:
            if fName not in self.features:
                if fName == WARP[2]:
                    self.tm.info(
                        (
                            f'Warp feature "{WARP[2]}" not found. Working without Text-API\n'
                        )
                    )
                    self.features[WARP[2]] = Data(
                        f"{WARP[2]}.tf", self.tm, isConfig=True, metaData=WARP2_DEFAULT,
                    )
                    self.features[WARP[2]].dataLoaded = True
                else:
                    self.tm.info(
                        f'Warp feature "{fName}" not found in\n{self.locationRep}'
                    )
                    good = False
            elif fName == WARP[2]:
                self._loadFeature(fName, optional=True)
        if not good:
            return False
        self.warpDir = self.features[WARP[0]].dirName
        self.precomputeList = []
        for (dep2, fName, method, dependencies) in PRECOMPUTE:
            thisGood = True
            if dep2 and WARP[2] not in self.features:
                continue
            if dep2:
                otextMeta = self.features[WARP[2]].metaData
                sFeatures = f"{KIND[fName]}Features"
                sFeats = tuple(itemize(otextMeta.get(sFeatures, ""), ","))
                dependencies = dependencies + sFeats
            for dep in dependencies:
                if dep not in self.features:
                    self.tm.info(
                        f'Missing dependency for computed data feature "{fName}": "{dep}"'
                    )
                    thisGood = False
            if not thisGood:
                good = False
            self.features[fName] = Data(
                f"{self.warpDir}/{fName}.x",
                self.tm,
                method=method,
                dependencies=[self.features.get(dep, None) for dep in dependencies],
            )
            self.precomputeList.append((fName, dep2))
        self.good = good

    def _getWriteLoc(self, location=None, module=None):
        writeLoc = (
            os.path.expanduser(location)
            if location is not None
            else ""
            if len(self.locations) == 0
            else self.locations[-1]
        )
        writeMod = (
            module
            if module is not None
            else ""
            if len(self.modules) == 0
            else self.modules[-1]
        )
        self.writeDir = (
            f"{writeLoc}{writeMod}"
            if writeLoc == "" or writeMod == ""
            else f"{writeLoc}/{writeMod}"
        )

    def _precompute(self):
        good = True
        for (fName, dep2) in self.precomputeList:
            ok = getattr(self, f'{fName.strip("_")}OK', False)
            if dep2 and not ok:
                continue
            if not self.features[fName].load():
                good = False
                break
        self.good = good

    def _makeApi(self):
        if not self.good:
            return None

        silent = self.tm.isSilent()
        api = Api(self)

        w0info = self.features[WARP[0]]
        w1info = self.features[WARP[1]]

        setattr(api.F, WARP[0], OtypeFeature(api, w0info.metaData, w0info.data))
        setattr(api.E, WARP[1], OslotsFeature(api, w1info.metaData, w1info.data))

        requestedSet = set(self.featuresRequested)

        for fName in self.features:
            fObj = self.features[fName]
            if fObj.dataLoaded and not fObj.isConfig:
                if fObj.method:
                    feat = fName.strip("_")
                    ok = getattr(self, f"{feat}OK", False)
                    ap = api.C
                    if fName in [x[0] for x in self.precomputeList if not x[1] or ok]:
                        setattr(ap, feat, Computed(api, fObj.data))
                    else:
                        fObj.unload()
                        if hasattr(ap, feat):
                            delattr(api.C, feat)
                else:
                    if fName in requestedSet | self.textFeatures:
                        if fName in WARP:
                            continue
                        elif fObj.isEdge:
                            setattr(
                                api.E,
                                fName,
                                EdgeFeature(
                                    api, fObj.metaData, fObj.data, fObj.edgeValues
                                ),
                            )
                        else:
                            setattr(
                                api.F, fName, NodeFeature(api, fObj.metaData, fObj.data)
                            )
                    else:
                        if fName in WARP or fName in self.textFeatures:
                            continue
                        elif fObj.isEdge:
                            if hasattr(api.E, fName):
                                delattr(api.E, fName)
                        else:
                            if hasattr(api.F, fName):
                                delattr(api.F, fName)
                        fObj.unload()
        addSortKey(api)
        addOtype(api)
        addLocality(api)
        addRank(api)
        addText(api)
        addSearch(api, silent)
        self.tm.indent(level=0)
        self.tm.info("All features loaded/computed - for details use loadLog()")
        self.api = api
        return api

    def _updateApi(self):
        if not self.good:
            return None
        api = self.api

        requestedSet = set(self.featuresRequested)

        for fName in self.features:
            fObj = self.features[fName]
            if fObj.dataLoaded and not fObj.isConfig:
                if not fObj.method:
                    if fName in requestedSet | self.textFeatures:
                        if fName in WARP:
                            continue
                        elif fObj.isEdge:
                            if not hasattr(api.E, fName):
                                setattr(
                                    api.E,
                                    fName,
                                    EdgeFeature(
                                        api, fObj.metaData, fObj.data, fObj.edgeValues
                                    ),
                                )
                        else:
                            if not hasattr(api.F, fName):
                                setattr(
                                    api.F,
                                    fName,
                                    NodeFeature(api, fObj.metaData, fObj.data),
                                )
                    else:
                        if fName in WARP or fName in self.textFeatures:
                            continue
                        elif fObj.isEdge:
                            if hasattr(api.E, fName):
                                delattr(api.E, fName)
                        else:
                            if hasattr(api.F, fName):
                                delattr(api.F, fName)
                        fObj.unload()
        self.tm.indent(level=0)
        self.tm.info("All additional features loaded - for details use loadLog()")
