

class General(object):
    """ General(stockManager: IStockManager, passwordHasher: IPasswordHasher, documentQueue: IDocumentQueue) """
    def AddOrUpdateErpLock(self, lock):
        """ AddOrUpdateErpLock(self: General, lock: ErpLock) -> int """
        pass

    def AddOrUpdateErpLockDirect(self, lock):
        """ AddOrUpdateErpLockDirect(self: General, lock: ErpLock) -> int """
        pass

    def AddTaskAutoDisposeTask(self):
        """ AddTaskAutoDisposeTask(self: General) """
        pass

    def AddTaskCacheBackgroundTasks(self):
        """ AddTaskCacheBackgroundTasks(self: General) """
        pass

    def AddTaskErpLockingTask(self):
        """ AddTaskErpLockingTask(self: General) """
        pass

    def AddTaskLogCleanupTask(self):
        """ AddTaskLogCleanupTask(self: General) """
        pass

    def AddTaskMessageQueueCleanupTask(self):
        """ AddTaskMessageQueueCleanupTask(self: General) """
        pass

    def AddTaskNotificationCleanupTask(self):
        """ AddTaskNotificationCleanupTask(self: General) """
        pass

    def AddTaskStockStreamTask(self):
        """ AddTaskStockStreamTask(self: General) """
        pass

    def AddUserToZone(self, zone, user):
        """ AddUserToZone(self: General, zone: Zone, user: User) -> bool """
        pass

    def AttachClient(self, endPoint):
        """ AttachClient(self: General, endPoint: str) """
        pass

    def AuthenticateUser(self, args, barcodeSettings):
        """ AuthenticateUser(self: General, args: AuthenticationArgs) -> (RemotingIdentity, BarcodeTypes) """
        pass

    def AuthenticateUserForDefaultZone(self, remId):
        """ AuthenticateUserForDefaultZone(self: General) -> (bool, RemotingIdentity) """
        pass

    def AuthenticateUserForFirstAvailableZone(self, remId):
        """ AuthenticateUserForFirstAvailableZone(self: General) -> (bool, RemotingIdentity) """
        pass

    def AuthenticateUserForZone(self, selectedZone, remId):
        """ AuthenticateUserForZone(self: General, selectedZone: Zone) -> (bool, RemotingIdentity) """
        pass

    def BeepContinuous(self, endPoint):
        """ BeepContinuous(self: General, endPoint: str) """
        pass

    def CheckHookVersions(self):
        """ CheckHookVersions(self: General) -> bool """
        pass

    def CheckLicenseFile(self, xml, errors, license):
        """ CheckLicenseFile(self: General, xml: str) -> (bool, List[str], License) """
        pass

    def CheckServerHealth(self):
        """ CheckServerHealth(self: General) -> ServerHealthEnum """
        pass

    def CheckZoneRightAddReferenceOnTransfer(self, warehouseTransferKey):
        """ CheckZoneRightAddReferenceOnTransfer(self: General, warehouseTransferKey: CacheKey) -> bool """
        pass

    def CleanupCacheHistory(self):
        """ CleanupCacheHistory(self: General) """
        pass

    def CleanupUserCacheData(self):
        """ CleanupUserCacheData(self: General) """
        pass

    def ClearResourceCache(self):
        """ ClearResourceCache(self: General) """
        pass

    def CompileScript(self, script):
        """ CompileScript(self: General, script: str) -> List[PythonError] """
        pass

    def ConvertToUsersByZone(self, oZonesUsersProxy):
        """ ConvertToUsersByZone(self: General, oZonesUsersProxy: ViewUsersInZone) -> Users """
        pass

    def CreateColliPreset(self, arg):
        """ CreateColliPreset(self: General, arg: DataFlowObject[ColliPreset]) -> DataFlowObject[ColliPreset] """
        pass

    def CreateDatabase(self, message):
        """ CreateDatabase(self: General) -> (bool, str) """
        pass

    def CreateDevice(self, arg):
        """ CreateDevice(self: General, arg: DataFlowObject[Device]) -> DataFlowObject[Device] """
        pass

    def CreateLocationClassification(self, arg):
        """ CreateLocationClassification(self: General, arg: DataFlowObject[LocationClassification]) -> DataFlowObject[LocationClassification] """
        pass

    def CreateModule(self, arg):
        """ CreateModule(self: General, arg: ModuleArgs) -> bool """
        pass

    def CreateOrUpdateBackgroundAgent(self, arg):
        """ CreateOrUpdateBackgroundAgent(self: General, arg: DataFlowObject[BackgroundAgent]) -> DataFlowObject[BackgroundAgent] """
        pass

    def CreatePrintLabel(self, arg):
        """ CreatePrintLabel(self: General, arg: DataFlowObject[PrintLabel]) -> DataFlowObject[PrintLabel] """
        pass

    def CreateScript(self, arg):
        """ CreateScript(self: General, arg: DataFlowObject[ZoneScript]) -> DataFlowObject[ZoneScript] """
        pass

    def CreateScriptTask(self, arg):
        """ CreateScriptTask(self: General, arg: DataFlowObject[ScriptTask]) -> DataFlowObject[ScriptTask] """
        pass

    def CreateShipperServiceLink(self, arg):
        """ CreateShipperServiceLink(self: General, arg: DataFlowObject[ShipperServiceLink]) -> DataFlowObject[ShipperServiceLink] """
        pass

    def CreateSnippetModule(self, arg):
        """ CreateSnippetModule(self: General, arg: ModuleArgs) -> bool """
        pass

    def CreateStorageAssignmentClassification(self, arg):
        """ CreateStorageAssignmentClassification(self: General, arg: DataFlowObject[StorageAssignmentClassification]) -> DataFlowObject[StorageAssignmentClassification] """
        pass

    def CreateTag(self, arg):
        """ CreateTag(self: General, arg: DataFlowObject[Tag]) -> DataFlowObject[Tag] """
        pass

    def CreateUser(self, arg):
        """ CreateUser(self: General, arg: DataFlowObject[User]) -> DataFlowObject[User] """
        pass

    def CreateWarehouseLayoutSetting(self, arg):
        """ CreateWarehouseLayoutSetting(self: General, arg: DataFlowObject[WarehouseLayoutSetting]) -> DataFlowObject[WarehouseLayoutSetting] """
        pass

    def CreateZone(self, arg):
        """ CreateZone(self: General, arg: DataFlowObject[Zone]) -> DataFlowObject[Zone] """
        pass

    def DeleteBackgroundAgent(self, arg):
        """ DeleteBackgroundAgent(self: General, arg: DataFlowObject[BackgroundAgent]) -> DataFlowObject[BackgroundAgent] """
        pass

    def DeleteColliPreset(self, arg):
        """ DeleteColliPreset(self: General, arg: DataFlowObject[ColliPreset]) -> DataFlowObject[ColliPreset] """
        pass

    def DeleteDevice(self, arg):
        """ DeleteDevice(self: General, arg: DataFlowObject[Device]) -> DataFlowObject[Device] """
        pass

    def DeleteErpLock(self, lock):
        """ DeleteErpLock(self: General, lock: ErpLock) """
        pass

    def DeleteLocationClassification(self, arg):
        """ DeleteLocationClassification(self: General, arg: DataFlowObject[LocationClassification]) -> DataFlowObject[LocationClassification] """
        pass

    def DeleteModule(self, arg):
        """ DeleteModule(self: General, arg: ModuleArgs) -> bool """
        pass

    def DeletePrintLabel(self, arg):
        """ DeletePrintLabel(self: General, arg: DataFlowObject[PrintLabel]) -> DataFlowObject[PrintLabel] """
        pass

    def DeleteScript(self, arg):
        """ DeleteScript(self: General, arg: DataFlowObject[ZoneScript]) -> DataFlowObject[ZoneScript] """
        pass

    def DeleteScriptTask(self, arg):
        """ DeleteScriptTask(self: General, arg: DataFlowObject[ScriptTask]) -> DataFlowObject[ScriptTask] """
        pass

    def DeleteShipperServiceLink(self, arg):
        """ DeleteShipperServiceLink(self: General, arg: DataFlowObject[ShipperServiceLink]) -> DataFlowObject[ShipperServiceLink] """
        pass

    def DeleteStorageAssignmentClassification(self, arg):
        """ DeleteStorageAssignmentClassification(self: General, arg: DataFlowObject[StorageAssignmentClassification]) -> DataFlowObject[StorageAssignmentClassification] """
        pass

    def DeleteTag(self, arg):
        """ DeleteTag(self: General, arg: DataFlowObject[Tag]) -> DataFlowObject[Tag] """
        pass

    def DeleteUser(self, arg):
        """ DeleteUser(self: General, arg: DataFlowObject[User]) -> DataFlowObject[User] """
        pass

    def DeleteWarehouseLayoutSetting(self, arg):
        """ DeleteWarehouseLayoutSetting(self: General, arg: DataFlowObject[WarehouseLayoutSetting]) -> DataFlowObject[WarehouseLayoutSetting] """
        pass

    def DeleteZone(self, arg):
        """ DeleteZone(self: General, arg: DataFlowObject[Zone]) -> DataFlowObject[Zone] """
        pass

    def DiscardPrintLines(self, key):
        """ DiscardPrintLines(self: General, key: CacheKey) """
        pass

    def DisposeCachedObject(self, hashCode):
        """ DisposeCachedObject(self: General, hashCode: int) -> DataFlowObject[object] """
        pass

    def DisposeCachedObjects(self):
        """ DisposeCachedObjects(self: General) """
        pass

    def DisposeCachedObjectWhenUnchanged(self, key):
        """ DisposeCachedObjectWhenUnchanged(self: General, key: CacheKey) """
        pass

    def ExecuteCommand(self, command):
        """ ExecuteCommand(self: General, command: str) -> str """
        pass

    def ExecuteScript(self, script):
        """ ExecuteScript(self: General, script: str) -> object """
        pass

    def ExecuteScriptTaskOnce(self, id):
        """ ExecuteScriptTaskOnce(self: General, id: int) -> object """
        pass

    def ExecuteScriptWithCacheObjectScope(self, script, cacheKey):
        """ ExecuteScriptWithCacheObjectScope(self: General, script: str, cacheKey: int) -> object """
        pass

    def ExecuteScriptWithScope(self, script, scope):
        """ ExecuteScriptWithScope(self: General, script: str, scope: Dictionary[str, object]) -> object """
        pass

    def FinishUploadModule(self, arg):
        """ FinishUploadModule(self: General, arg: ModuleArgs) -> bool """
        pass

    def GenerateSerialNumbers(self, dfObject, numbersGenerated):
        """ GenerateSerialNumbers(self: General, dfObject: DataFlowObject[ItemIdGenerateArgs]) -> (DataFlowObject[ItemIdGenerateArgs], List[str]) """
        pass

    def GetActiveColliPresets(self, colliPresets):
        """ GetActiveColliPresets(self: General) -> (int, ColliPresets) """
        pass

    def GetAppDomainList(self):
        """ GetAppDomainList(self: General) -> List[AppDomainInformation] """
        pass

    def GetBackgroundAgentById(self, id, agent):
        """ GetBackgroundAgentById(self: General, id: str) -> (bool, BackgroundAgent) """
        pass

    def GetBackgroundAgentsAll(self, agents):
        """ GetBackgroundAgentsAll(self: General) -> (int, BackgroundAgents) """
        pass

    def GetBackgroundAgentsByType(self, type, agents):
        """ GetBackgroundAgentsByType(self: General, type: BackgroundAgentType) -> (int, BackgroundAgents) """
        pass

    def GetBackgroundAgentStatusByType(self, type):
        """ GetBackgroundAgentStatusByType(self: General, type: BackgroundAgentType) -> BackgroundAgentStatus """
        pass

    def GetBarcodeSettingsAll(self, types):
        """ GetBarcodeSettingsAll(self: General) -> (int, BarcodeTypes) """
        pass

    def GetCacheObject(self, hashCode):
        """ GetCacheObject(self: General, hashCode: int) -> ICachable """
        pass

    def GetCacheObjectAsXml(self, hashCode):
        """ GetCacheObjectAsXml(self: General, hashCode: int) -> str """
        pass

    def GetChacheStatus(self):
        """ GetChacheStatus(self: General) -> str """
        pass

    def GetColliPresetById(self, id, colliPreset):
        """ GetColliPresetById(self: General, id: int) -> (bool, ColliPreset) """
        pass

    def GetColliPresetsAll(self, colliPresets):
        """ GetColliPresetsAll(self: General) -> (int, ColliPresets) """
        pass

    def GetColliPresetSpecificationCodes(self, searchText, colliSpecificationCodes):
        """ GetColliPresetSpecificationCodes(self: General, searchText: str) -> (int, List[str]) """
        pass

    def GetCopyOfCache(self):
        """ GetCopyOfCache(self: General) -> List[ICachable] """
        pass

    def GetCountriesActive(self, countries):
        """ GetCountriesActive(self: General) -> (int, Countries) """
        pass

    def GetCurrentIdentity(self):
        """ GetCurrentIdentity(self: General) -> RemotingIdentity """
        pass

    def GetDefaultColliPreset(self, colliPreset):
        """ GetDefaultColliPreset(self: General) -> (bool, ColliPreset) """
        pass

    def GetDefaultInboundLocations(self, warehouseCode, locations):
        """ GetDefaultInboundLocations(self: General, warehouseCode: str) -> (bool, Locations) """
        pass

    def GetDeviceById(self, id, device):
        """ GetDeviceById(self: General, id: int) -> (bool, Device) """
        pass

    def GetDeviceByMacAddress(self, macAddress, device):
        """ GetDeviceByMacAddress(self: General, macAddress: str) -> (bool, Device) """
        pass

    def GetDeviceByName(self, name, device):
        """ GetDeviceByName(self: General, name: str) -> (bool, Device) """
        pass

    def GetDeviceInformation(self, endPoint, deviceInfo):
        """ GetDeviceInformation(self: General, endPoint: str) -> (bool, DeviceInformation) """
        pass

    def GetDevicesAll(self, devices):
        """ GetDevicesAll(self: General) -> (int, Devices) """
        pass

    def GetErpLocks(self, locks):
        """ GetErpLocks(self: General) -> (int, List[ErpLock]) """
        pass

    def GetErpName(self):
        """ GetErpName(self: General) -> str """
        pass

    def GetErpSettings(self):
        """ GetErpSettings(self: General) -> SystemSettings """
        pass

    def GetErpSettingsTable(self):
        """ GetErpSettingsTable(self: General) -> SystemSettingsTable """
        pass

    def GetExecutionContexts(self):
        """ GetExecutionContexts(self: General) -> List[SafeRpcExecutionContext] """
        pass

    def GetGeneratedScriptComment(self, script):
        """ GetGeneratedScriptComment(self: General, script: ZoneScript) -> str """
        pass

    def GetImplementedMethods(self):
        """ GetImplementedMethods(self: General) -> ImplementedFunctionalities """
        pass

    def GetItem(self, itemCode, item):
        """ GetItem(self: General, itemCode: str) -> (bool, Item) """
        pass

    def GetItemDescription(self, itemCode):
        """ GetItemDescription(self: General, itemCode: str) -> str """
        pass

    def GetItemExists(self, itemCode):
        """ GetItemExists(self: General, itemCode: str) -> bool """
        pass

    def GetItemExistsOnDefaultInboundLocation(self, itemCode, warehouseCode, item):
        """ GetItemExistsOnDefaultInboundLocation(self: General, itemCode: str, warehouseCode: str) -> (bool, LocationItem) """
        pass

    def GetItemExistsOnLocation(self, itemCode, warehouseCode, warehouseLocationCode, item):
        """ GetItemExistsOnLocation(self: General, itemCode: str, warehouseCode: str, warehouseLocationCode: str) -> (bool, LocationItem) """
        pass

    def GetItemIdentificationExists(self, itemCode, itemId):
        """ GetItemIdentificationExists(self: General, itemCode: str, itemId: str) -> bool """
        pass

    def GetItemIdentificationExistsMulti(self, itemCode, itemIds):
        """ GetItemIdentificationExistsMulti(self: General, itemCode: str, itemIds: List[str]) -> bool """
        pass

    def GetItemIdentifications(self, args, selected, itemIdentifications):
        """ GetItemIdentifications(self: General, args: GetItemIdentificationArgs, selected: ItemIdentifications) -> (int, ItemIdentifications) """
        pass

    def GetItemIdentificationsAvailable(self, args, itemIds):
        """ GetItemIdentificationsAvailable(self: General, args: GetItemIdentificationArgs) -> (int, ItemIdentifications) """
        pass

    def GetItemIdentificationsAvailableIncludingBatches(self, cacheKeyOfBatch, args, itemIds):
        """ GetItemIdentificationsAvailableIncludingBatches(self: General, cacheKeyOfBatch: CacheKey, args: GetItemIdentificationArgs) -> (int, ItemIdentifications) """
        pass

    def GetItemImageFromErp(self, itemCode):
        """ GetItemImageFromErp(self: General, itemCode: str) -> Array[Byte] """
        pass

    def GetItemImageLarge(self, itemCode):
        """ GetItemImageLarge(self: General, itemCode: str) -> Array[Byte] """
        pass

    def GetItemImageSmall(self, itemCode):
        """ GetItemImageSmall(self: General, itemCode: str) -> Array[Byte] """
        pass

    def GetItemLocationDefault(self, args, location):
        """ GetItemLocationDefault(self: General, args: GetItemLocationsArgs) -> (bool, ItemLocation) """
        pass

    def GetItemLocations(self, args, locations):
        """ GetItemLocations(self: General, args: GetItemLocationsArgs) -> (int, ItemLocations) """
        pass

    def GetItems(self, args, paging, items):
        """ GetItems(self: General, args: GetItemsArgs, paging: PagingParams) -> (int, Items) """
        pass

    def GetItemsAll(self, args, items):
        """ GetItemsAll(self: General, args: GetItemsOnLocationArgs) -> (int, LocationItems) """
        pass

    def GetItemsOnDefaultInboundLocation(self, warehouseCode, filter, items):
        """ GetItemsOnDefaultInboundLocation(self: General, warehouseCode: str, filter: str) -> (int, LocationItems) """
        pass

    def GetItemsOnLocation(self, args, items):
        """ GetItemsOnLocation(self: General, args: GetItemsOnLocationArgs) -> (int, LocationItems) """
        pass

    def GetItemsOnTransportLocation(self, filter, items):
        """ GetItemsOnTransportLocation(self: General, filter: str) -> (int, LocationItems) """
        pass

    def GetItemStockAvailableIncludingBatches(self, cacheKeyOfBatch, args, itemStock):
        """ GetItemStockAvailableIncludingBatches(self: General, cacheKeyOfBatch: CacheKey, args: GetItemStockListArgs) -> (int, List[ItemStock]) """
        pass

    def GetItemStockList(self, args, itemStockLocationList):
        """ GetItemStockList(self: General, args: GetItemStockListArgs) -> (int, ItemStockLocationList) """
        pass

    def GetItemStockTotals(self, args, totals):
        """ GetItemStockTotals(self: General, args: GetItemStockTotalsArgs) -> (bool, ItemStockTotals) """
        pass

    def GetLibContent(self, arg, contents):
        """ GetLibContent(self: General, arg: GetLibArgs) -> (int, LibContents) """
        pass

    @staticmethod
    def GetLibRoot():
        """ GetLibRoot() -> str """
        pass

    def GetLocationClassificationById(self, id, locationClassification):
        """ GetLocationClassificationById(self: General, id: int) -> (bool, LocationClassification) """
        pass

    def GetLocationClassifications(self, filterBy, locationClassifications):
        """ GetLocationClassifications(self: General, filterBy: LocationClassificationsFilter) -> (int, LocationClassifications) """
        pass

    def GetLocationsByCountGroup(self, countGroup, locations):
        """ GetLocationsByCountGroup(self: General, countGroup: CountGroup) -> (int, Locations) """
        pass

    def GetLocationsByLocationClassification(self, locationClassification, locations):
        """ GetLocationsByLocationClassification(self: General, locationClassification: LocationClassification) -> (int, Locations) """
        pass

    def GetLocationsByStorageAssignmentClassification(self, storageAssignmentClassification, locations):
        """ GetLocationsByStorageAssignmentClassification(self: General, storageAssignmentClassification: StorageAssignmentClassification) -> (int, Locations) """
        pass

    def GetLogLines(self, args):
        """ GetLogLines(self: General, args: GetLogLinesArgs) -> PagedList[LogLine] """
        pass

    def GetMacAddress(self):
        """ GetMacAddress(self: General) -> str """
        pass

    def GetModule(self, arg, module):
        """ GetModule(self: General, arg: ModuleArgs) -> (bool, PythonModule) """
        pass

    def GetPendingPrintLineCount(self, key):
        """ GetPendingPrintLineCount(self: General, key: CacheKey) -> int """
        pass

    def GetPrintDatasetInstance(self, datasetFullTypeName, dataset):
        """ GetPrintDatasetInstance(self: General, datasetFullTypeName: str) -> (bool, PrintDatasetBase) """
        pass

    def GetPrintDatasets(self, datasets):
        """ GetPrintDatasets(self: General) -> (int, List[PrintDatasetBase]) """
        pass

    def GetPrintersTable(self):
        """ GetPrintersTable(self: General) -> Hashtable """
        pass

    def GetPrintLabelByName(self, name, label):
        """ GetPrintLabelByName(self: General, name: str) -> (bool, PrintLabel) """
        pass

    def GetPrintLabelImage(self, labelId):
        """ GetPrintLabelImage(self: General, labelId: str) -> Array[Byte] """
        pass

    def GetPrintLabelMappings(self, labelId, mappings):
        """ GetPrintLabelMappings(self: General, labelId: int) -> (bool, Mappings[str, str, str]) """
        pass

    def GetPrintLabels(self, labels):
        """ GetPrintLabels(self: General) -> (int, PrintLabels) """
        pass

    def GetPrintLabelsOfDataset(self, datasetTypeFullName, labels):
        """ GetPrintLabelsOfDataset(self: General, datasetTypeFullName: str) -> (int, PrintLabels) """
        pass

    def GetPrintLabelsOfPrintLines(self, printsLinesTypes, labels):
        """ GetPrintLabelsOfPrintLines(self: General, printsLinesTypes: IEnumerable[Type]) -> (int, PrintLabels) """
        pass

    def GetProfilingLogEntries(self, userKey, previousMethod, endTime, elapsedMiliSeconds, entries):
        """ GetProfilingLogEntries(self: General, userKey: int, previousMethod: int, endTime: Nullable[DateTime], elapsedMiliSeconds: int) -> (int, ProfilingLogEntries) """
        pass

    def GetProfilingUserNodes(self, userNodes):
        """ GetProfilingUserNodes(self: General) -> (int, ProfilingUserNodes) """
        pass

    def GetProgressOfActivity(self, args, activity):
        """ GetProgressOfActivity(self: General, args: GetActivityProgressArgs) -> (bool, Activity) """
        pass

    def GetProgressUpdate(self, args, progress):
        """ GetProgressUpdate(self: General, args: GetActivityProgressArgs) -> (bool, Progress) """
        pass

    def GetResourcesOfTranslation(self, resourceSet, culture, translation):
        """ GetResourcesOfTranslation(self: General, resourceSet: str, culture: str) -> (bool, Translation) """
        pass

    def GetScreenshot(self, accessId):
        """ GetScreenshot(self: General, accessId: str) -> Array[Byte] """
        pass

    def GetScriptIntellisenseOptions(self, hint):
        """ GetScriptIntellisenseOptions(self: General, hint: str) -> Array[str] """
        pass

    def GetScripts(self, arg, scripts):
        """ GetScripts(self: General, arg: GetScriptArgs) -> (int, ZoneScripts) """
        pass

    def GetScriptsAll(self, scripts):
        """ GetScriptsAll(self: General) -> (int, ZoneScripts) """
        pass

    def GetScriptSnippets(self, snippets):
        """ GetScriptSnippets(self: General) -> (int, List[ScriptSnippet]) """
        pass

    def GetScriptTaskById(self, id, task):
        """ GetScriptTaskById(self: General, id: int) -> (bool, ScriptTask) """
        pass

    def GetScriptTaskByName(self, name, task):
        """ GetScriptTaskByName(self: General, name: str) -> (bool, ScriptTask) """
        pass

    def GetScriptTaskProjectedSchedule(self, id, schedule, firstOccurrence):
        """ GetScriptTaskProjectedSchedule(self: General, id: int) -> (bool, Array[DateTime], DateTime) """
        pass

    def GetScriptTasksActive(self, tasks):
        """ GetScriptTasksActive(self: General) -> (int, ScriptTasks) """
        pass

    def GetScriptTasksAll(self, tasks):
        """ GetScriptTasksAll(self: General) -> (int, ScriptTasks) """
        pass

    def GetScriptTasksInActive(self, tasks):
        """ GetScriptTasksInActive(self: General) -> (int, ScriptTasks) """
        pass

    def GetServerDate(self):
        """ GetServerDate(self: General) -> DateTime """
        pass

    def GetSessions(self, sessions):
        """ GetSessions(self: General) -> (int, Sessions) """
        pass

    def GetSettings(self):
        """ GetSettings(self: General) -> SystemSettings """
        pass

    def GetSettingsTable(self):
        """ GetSettingsTable(self: General) -> SystemSettingsTable """
        pass

    def GetShipperServiceLinkByErpDeliveryMethodCode(self, erpDeliveryMethodCode, shipperServiceLink):
        """ GetShipperServiceLinkByErpDeliveryMethodCode(self: General, erpDeliveryMethodCode: str) -> (bool, ShipperServiceLink) """
        pass

    def GetShipperServiceLinksAll(self, shipperServiceLinks):
        """ GetShipperServiceLinksAll(self: General) -> (int, ShipperServiceLinks) """
        pass

    @staticmethod
    def GetSnippetRoot():
        """ GetSnippetRoot() -> str """
        pass

    def GetSortedItemLocations(self, args, filterOptions, locations):
        """ GetSortedItemLocations(self: General, args: GetItemLocationsArgs, filterOptions: FilterOptions) -> (int, ItemLocations) """
        pass

    @staticmethod
    def GetStdLibRoot(path):
        """ GetStdLibRoot() -> (bool, str) """
        pass

    def GetStorageAssignmentClassificationById(self, id, storageAssignmentClassification):
        """ GetStorageAssignmentClassificationById(self: General, id: int) -> (bool, StorageAssignmentClassification) """
        pass

    def GetStorageAssignmentClassifications(self, filterBy, storageAssignmentClassifications):
        """ GetStorageAssignmentClassifications(self: General, filterBy: StorageAssignmentClassificationsFilter) -> (int, StorageAssignmentClassifications) """
        pass

    def GetTagById(self, id, tag):
        """ GetTagById(self: General, id: int) -> (bool, Tag) """
        pass

    def GetTagsAll(self, tags):
        """ GetTagsAll(self: General) -> (int, Tags) """
        pass

    def GetTagsByDescription(self, filter, tags):
        """ GetTagsByDescription(self: General, filter: str) -> (int, Tags) """
        pass

    def GetTagsByType(self, target, tags):
        """ GetTagsByType(self: General, target: TagTarget) -> (int, Tags) """
        pass

    def GetTranslationsAvailable(self, translations):
        """ GetTranslationsAvailable(self: General) -> (int, Translations) """
        pass

    def GetTranslationsAvailablePerSet(self, resourseSet, translations):
        """ GetTranslationsAvailablePerSet(self: General, resourseSet: str) -> (int, Translations) """
        pass

    def GetUserByUserId(self, userId, user):
        """ GetUserByUserId(self: General, userId: int) -> (bool, User) """
        pass

    def GetUserByUserName(self, username, user):
        """ GetUserByUserName(self: General, username: str) -> (bool, User) """
        pass

    def GetUserCacheData(self, tag):
        """ GetUserCacheData(self: General, tag: str) -> str """
        pass

    def GetUsersActive(self, users):
        """ GetUsersActive(self: General) -> (int, Users) """
        pass

    def GetUsersAll(self, users):
        """ GetUsersAll(self: General) -> (int, Users) """
        pass

    def GetUsersInactive(self, users):
        """ GetUsersInactive(self: General) -> (int, Users) """
        pass

    def GetUsersInZone(self, zoneId, users):
        """ GetUsersInZone(self: General, zoneId: int) -> (int, Users) """
        pass

    def GetVersion(self):
        """ GetVersion(self: General) -> str """
        pass

    def GetWarehouseByCode(self, warehouseCode, warehouse):
        """ GetWarehouseByCode(self: General, warehouseCode: str) -> (bool, Warehouse) """
        pass

    def GetWarehouseExists(self, warehouseCode):
        """ GetWarehouseExists(self: General, warehouseCode: str) -> bool """
        pass

    def GetWarehouseLayoutBySetting(self, warehouseLocation, warehouseLayoutSetting, warehouseLayout):
        """ GetWarehouseLayoutBySetting(self: General, warehouseLocation: str, warehouseLayoutSetting: WarehouseLayoutSetting) -> (bool, WarehouseLayout) """
        pass

    def GetWarehouseLayoutsBySetting(self, warehouseLayoutSetting, warehouseLayouts):
        """ GetWarehouseLayoutsBySetting(self: General, warehouseLayoutSetting: WarehouseLayoutSetting) -> (int, WarehouseLayouts) """
        pass

    def GetWarehouseLayoutSettingById(self, id, warehouseLayoutSetting):
        """ GetWarehouseLayoutSettingById(self: General, id: int) -> (bool, WarehouseLayoutSetting) """
        pass

    def GetWarehouseLayoutSettings(self, filterBy, warehouseLayoutSettings):
        """ GetWarehouseLayoutSettings(self: General, filterBy: WarehouseLayoutSettingFilter) -> (int, WarehouseLayoutSettings) """
        pass

    def GetWarehouseLocationExists(self, warehouseCode, warehouseLocationCode):
        """ GetWarehouseLocationExists(self: General, warehouseCode: str, warehouseLocationCode: str) -> bool """
        pass

    def GetWarehouseLocationFromStockThenErp(self, warehouseCode, warehouseLocationCode):
        """ GetWarehouseLocationFromStockThenErp(self: General, warehouseCode: str, warehouseLocationCode: str) -> Location """
        pass

    def GetWarehouseLocationIfExists(self, warehouseCode, warehouseLocationCode, location):
        """ GetWarehouseLocationIfExists(self: General, warehouseCode: str, warehouseLocationCode: str) -> (bool, Location) """
        pass

    def GetWarehouseLocations(self, args, locations):
        """ GetWarehouseLocations(self: General, args: GetWarehouseLocationsArgs) -> (int, Locations) """
        pass

    def GetWarehousesActive(self, warehouses):
        """ GetWarehousesActive(self: General) -> (int, Warehouses) """
        pass

    def GetWarehousesActiveByLocation(self, warehouseLocationCode, warehouses):
        """ GetWarehousesActiveByLocation(self: General, warehouseLocationCode: str) -> (int, Warehouses) """
        pass

    def GetWarehousesActiveWithDefaultInboundLocation(self, warehouses):
        """ GetWarehousesActiveWithDefaultInboundLocation(self: General) -> (int, Warehouses) """
        pass

    def GetWarehousesAll(self, warehouses):
        """ GetWarehousesAll(self: General) -> (int, Warehouses) """
        pass

    def GetWarehousesInactive(self, warehouses):
        """ GetWarehousesInactive(self: General) -> (int, Warehouses) """
        pass

    def GetZoneById(self, id, zone):
        """ GetZoneById(self: General, id: int) -> (bool, Zone) """
        pass

    def GetZoneByName(self, name, zone):
        """ GetZoneByName(self: General, name: str) -> (bool, Zone) """
        pass

    def GetZoneRightsOfZone(self, zoneId, zoneRights):
        """ GetZoneRightsOfZone(self: General, zoneId: int) -> (bool, ZoneRights) """
        pass

    def GetZonesActive(self, active, zones):
        """ GetZonesActive(self: General, active: bool) -> (int, Zones) """
        pass

    def GetZonesActiveOfCurrentUser(self, zones):
        """ GetZonesActiveOfCurrentUser(self: General) -> (int, Zones) """
        pass

    def GetZonesActiveOfUser(self, user, zones):
        """ GetZonesActiveOfUser(self: General, user: User) -> (int, Zones) """
        pass

    def GetZonesAll(self, zones):
        """ GetZonesAll(self: General) -> (int, Zones) """
        pass

    def GetZoneScriptHook(self, arg, script):
        """ GetZoneScriptHook(self: General, arg: GetScriptArgs) -> (bool, ZoneScript) """
        pass

    def GetZoneScripts(self, arg, scripts):
        """ GetZoneScripts(self: General, arg: GetScriptArgs) -> (int, ZoneScripts) """
        pass

    def GetZoneScriptsOrphan(self, arg, scripts):
        """ GetZoneScriptsOrphan(self: General, arg: GetScriptArgs) -> (int, ZoneScripts) """
        pass

    def GetZonesOfUser(self, user, addActiveOnly, zones):
        """ GetZonesOfUser(self: General, user: User, addActiveOnly: bool) -> (int, Zones) """
        pass

    def GetZoneUsers(self, zoneId, zoneUsers):
        """ GetZoneUsers(self: General, zoneId: int) -> (int, ZoneUsers) """
        pass

    def InitializeLifetimeService(self):
        """ InitializeLifetimeService(self: General) -> object """
        pass

    def IsProfilerRunning(self):
        """ IsProfilerRunning(self: General) -> bool """
        pass

    def KillAppDomain(self, *__args):
        """
        KillAppDomain(self: General, arg: DataFlowObject[AppDomainInformation]) -> DataFlowObject[AppDomainInformation]

        KillAppDomain(self: General, filter: str)
        """
        pass

    def LoadCache(self):
        """ LoadCache(self: General) """
        pass

    def LoadSettings(self, *__args):
        """ LoadSettings(self: General, unsafe: bool)LoadSettings(self: General, settingsObject: SystemSettings) """
        pass

    def Logout(self, disconnectClient):
        """ Logout(self: General, disconnectClient: bool) """
        pass

    def MemberwiseClone(self, *args): #cannot find CLR method
        """
        MemberwiseClone(self: MarshalByRefObject, cloneIdentity: bool) -> MarshalByRefObject

        MemberwiseClone(self: object) -> object
        """
        pass

    def MoveModuleOrDirectory(self, isFile, name, fromDir, toDir):
        """ MoveModuleOrDirectory(self: General, isFile: bool, name: str, fromDir: str, toDir: str) -> bool """
        pass

    def OnPythonEngineBooted(self):
        """ OnPythonEngineBooted(self: General) """
        pass

    def OutputCacheStatusToLog(self):
        """ OutputCacheStatusToLog(self: General) """
        pass

    def PrintPrintLine(self, line, label):
        """ PrintPrintLine(self: General, line: PrintLineBase, label: PrintLabel) -> bool """
        pass

    def PrintPrintLineByObjectAndPrinter(self, line, label, printArgs):
        """ PrintPrintLineByObjectAndPrinter(self: General, line: PrintLineBase, label: PrintLabel, printArgs: PrintBaseArgs) -> bool """
        pass

    def PrintPrintLines(self, key, label):
        """ PrintPrintLines(self: General, key: CacheKey, label: PrintLabel) -> bool """
        pass

    def PrintPrintLinesByObject(self, lines, label):
        """ PrintPrintLinesByObject(self: General, lines: PrintLinesBase, label: PrintLabel) -> bool """
        pass

    def PrintPrintLinesByObjectAndPrinter(self, lines, label, printArgs):
        """ PrintPrintLinesByObjectAndPrinter(self: General, lines: PrintLinesBase, label: PrintLabel, printArgs: PrintBaseArgs) -> bool """
        pass

    def PrintTestLabel(self, labelId, testRun):
        """ PrintTestLabel(self: General, labelId: int, testRun: bool) """
        pass

    def PurgeProfilingLog(self):
        """ PurgeProfilingLog(self: General) """
        pass

    def RegisterBackgroundAgentLastSeen(self, agent):
        """ RegisterBackgroundAgentLastSeen(self: General, agent: BackgroundAgent) """
        pass

    def RemoveUserFromZone(self, zone, user):
        """ RemoveUserFromZone(self: General, zone: Zone, user: User) -> bool """
        pass

    def ResetBarcodeSettingsToDefault(self):
        """ ResetBarcodeSettingsToDefault(self: General) -> bool """
        pass

    def ResetPrintLines(self, key, printLines):
        """ ResetPrintLines(self: General, key: CacheKey) -> (bool, PrintLinesBase) """
        pass

    def RestartScriptEngine(self):
        """ RestartScriptEngine(self: General) """
        pass

    def SaveCache(self):
        """ SaveCache(self: General) """
        pass

    def SaveDefaultInboundLocation(self, warehouse):
        """ SaveDefaultInboundLocation(self: General, warehouse: DataFlowObject[Warehouse]) -> DataFlowObject[Warehouse] """
        pass

    def SaveErpSetting(self, memberName, value):
        """ SaveErpSetting(self: General, memberName: str, value: object) """
        pass

    def SaveModule(self, module):
        """ SaveModule(self: General, module: PythonModule) -> bool """
        pass

    def SavePrintLabelMappings(self, labelId, mappings):
        """ SavePrintLabelMappings(self: General, labelId: int, mappings: Mappings[str, str, str]) -> bool """
        pass

    def SaveSetting(self, memberName, value):
        """ SaveSetting(self: General, memberName: str, value: object) """
        pass

    def SaveTranslations(self, translations):
        """ SaveTranslations(self: General, *translations: Array[SaveTranslationArgs]) """
        pass

    def ScheduleScriptTasks(self):
        """ ScheduleScriptTasks(self: General) """
        pass

    def SendBroadcastMessage(self, message):
        """ SendBroadcastMessage(self: General, message: str) """
        pass

    def SendBroadcastQuestion(self, question, possibleAnswers):
        """ SendBroadcastQuestion(self: General, question: str, possibleAnswers: int) -> Answers """
        pass

    def SendKey(self, endPoint, key):
        """ SendKey(self: General, endPoint: str, key: str) """
        pass

    def SendMessage(self, endPoint, message):
        """ SendMessage(self: General, endPoint: str, message: str) """
        pass

    def SendMouseClick(self, endPoint, x, y):
        """ SendMouseClick(self: General, endPoint: str, x: int, y: int) """
        pass

    def SetPrintLinesQuantitiesAtMax(self, key, printLines):
        """ SetPrintLinesQuantitiesAtMax(self: General, key: CacheKey) -> (bool, PrintLinesBase) """
        pass

    def SetSessionTimeout(self):
        """ SetSessionTimeout(self: General) """
        pass

    def SetUserCacheData(self, tag, data):
        """ SetUserCacheData(self: General, tag: str, data: str) """
        pass

    def SetZoneRightsOfZone(self, zoneId, zoneRights):
        """ SetZoneRightsOfZone(self: General, zoneId: int, zoneRights: ZoneRightViews) -> bool """
        pass

    def Sleep(self, seconds):
        """ Sleep(self: General, seconds: int) -> str """
        pass

    def StartDiscoveryServer(self, tcpPortNumber=None, unsafe=None):
        """ StartDiscoveryServer(self: General)StartDiscoveryServer(self: General, tcpPortNumber: int, unsafe: bool) """
        pass

    def StartProfiler(self):
        """ StartProfiler(self: General) """
        pass

    def StopDiscoveryServer(self, unsafe=None):
        """ StopDiscoveryServer(self: General)StopDiscoveryServer(self: General, unsafe: bool) """
        pass

    def StopMarshalledObjectFactories(self):
        """ StopMarshalledObjectFactories(self: General) """
        pass

    def StopProfiler(self):
        """ StopProfiler(self: General) """
        pass

    def TouchGetSortedItemLocations(self, args, filterOptions, locations):
        """ TouchGetSortedItemLocations(self: General, args: GetItemLocationsArgs, filterOptions: FilterOptions) -> (int, ItemLocations) """
        pass

    def UpdateBarcodeSettings(self, dfObject):
        """ UpdateBarcodeSettings(self: General, dfObject: DataFlowObject[BarcodeTypes]) -> DataFlowObject[BarcodeTypes] """
        pass

    def UpdateCultureOfUserSession(self):
        """ UpdateCultureOfUserSession(self: General) """
        pass

    def UpdateDatabase(self, message):
        """ UpdateDatabase(self: General) -> (bool, str) """
        pass

    def UpdatePrintLine(self, key, line):
        """ UpdatePrintLine(self: General, key: CacheKey, line: PrintLineBase) -> bool """
        pass

    def UploadModule(self, arg):
        """ UploadModule(self: General, arg: AddModuleArgs) -> bool """
        pass

    def UploadNewLicense(self, xml, license):
        """ UploadNewLicense(self: General, xml: str) -> (bool, License) """
        pass

    def ValidateColliReferences(self, dfObject):
        """ ValidateColliReferences(self: General, dfObject: DataFlowObject[ValidateColliReferencesArgs]) -> DataFlowObject[ValidateColliReferencesArgs] """
        pass

    def ValidateColliReferenceScan(self, barcode, result):
        """ ValidateColliReferenceScan(self: General, barcode: str) -> (bool, ColliBarcodeResult) """
        pass

    def ValidateItemIdentification(self, itemCode, itemId, isBatchNumber, errorMessage):
        """ ValidateItemIdentification(self: General, itemCode: str, itemId: str, isBatchNumber: bool) -> (bool, str) """
        pass

    def ValidateItemIdentificationForDelivery(self, dfObject):
        """ ValidateItemIdentificationForDelivery(self: General, dfObject: DataFlowObject[ValidateItemIdentificationArgs]) -> DataFlowObject[ValidateItemIdentificationArgs] """
        pass

    def ValidateOrder(self, orderNumber, orderType):
        """ ValidateOrder(self: General, orderNumber: str, orderType: OrderTypeEnum) -> OrderValidationResult """
        pass

    def ValidateTransportPackageScan(self, barcode, result):
        """ ValidateTransportPackageScan(self: General, barcode: str) -> (bool, TransportPackageScanResult) """
        pass

    def __getitem__(self, *args): #cannot find CLR method
        """ x.__getitem__(y) <==> x[y] """
        pass

    def __init__(self, *args): #cannot find CLR method
        """ x.__init__(...) initializes x; see x.__class__.__doc__ for signaturex.__init__(...) initializes x; see x.__class__.__doc__ for signaturex.__init__(...) initializes x; see x.__class__.__doc__ for signature """
        pass

    @staticmethod # known case of __new__
    def __new__(self):
        """ __new__(cls: type, stockManager: IStockManager, passwordHasher: IPasswordHasher, documentQueue: IDocumentQueue) """
        pass

    CachedSettings = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Get: CachedSettings(self: General) -> SystemSettings



"""

    CurrentLicense = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
    """Get: CurrentLicense(self: General) -> License



Set: CurrentLicense(self: General) = value

"""

    DocumentQueue = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    StockManager = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default


