
AVAILABLE_MAPS = [
    "TORO",
    "Trainyard",
    "Prison",
    "Tideway",
    "Tell",
    "PowerPlant",
    "Summit",
    "Refinery",
    "Precinct",
    "Outskirts",
    "Ministry",
    "Hillside",
    "Hideout",
    "LastLight",
    "Gap",
    "Farmhouse",
    "Crossing",
    "Citadel",
    "Bab"
]

AVAILABLE_BOT_PROPERTIES = {
    "AIDifficulty <Decimal> 0.0-1.0": "AIDifficulty",
    "MinimumEnemies <Integer> 0-100": "MinimumEnemies",
    "MaximumEnemies <Integer> 0-100": "MaximumEnemies",
    "MaxPlayersToScaleEnemyCount <Integer> 0-100": "MaxPlayersToScaleEnemyCount",
    "ObjectiveTotalEnemyRespawnMultiplierMin <Decimal> 0.0-10.0": "ObjectiveTotalEnemyRespawnMultiplierMin",
    "ObjectiveTotalEnemyRespawnMultiplierMax <Decimal> 0.0-10.0": "ObjectiveTotalEnemyRespawnMultiplierMax",
    "FinalCacheBotQuotaMultiplier <Integer> 0-20": "FinalCacheBotQuotaMultiplier",
    "RespawnDPR <Decimal> 0.0-1.0": "RespawnDPR",
    "RespawnDelay <Integer> 0-20": "RespawnDelay",
    "CounterAttackRespawnDPR <Decimal> 0.0-1.0": "CounterAttackRespawnDPR",
    "CounterAttackRespawnDelay <Integer> 0-20": "CounterAttackRespawnDelay",
    "bCounterAttackReinforce <Boolean> True/False": "bCounterAttackReinforce",
    "AlarmDuration <Integer> 0-100": "AlarmDuration",
    "bBotsUseHumanLoadouts <Boolean> True/False": "bBotsUseHumanLoadouts",
    "RetreatTimer <Integer> 0-20": "RetreatTimer",
    "PostCaptureRushTimer <Integer> 0-n": "PostCaptureRushTimer",
    "FriendlyBotQuota <Integer> 0-n (0)": "FriendlyBotQuota",
    "ObjectiveDefendDistance <Integer> 0-n (2000)": "ObjectiveDefendDistance",
    "BotMinimumSpawnRange <Integer> 0-n (3000)": "BotMinimumSpawnRange",
    "BotMaximumSpawnRange <Integer> 0-n (15000)": "BotMaximumSpawnRange",
    "BotRespawnDistance <Integer> 0-n (10000)": "BotRespawnDistance"
}

AVAILABLE_PLAYER_PROPERTIES = {
    "bDeadSay <Boolean> True/False": "bDeadSay",
    "bDeadSayTeam <Boolean> True/False": "bDeadSayTeam",
    "bVoiceAllowDeadChat <Boolean> True/False": "bVoiceAllowDeadChat",
    "TeamKillLimit <Integer> 0-n": "TeamKillLimit",
    "TeamKillGrace <Decimal> 0.0-10.0": "TeamKillGrace",
    "TeamKillReduceTime <Decimal> 0.0-10.0": "TeamKillReduceTime",
    "FriendlyFireModifier <Decimal> 0.0-1.0": "FriendlyFireModifier",
    "FriendlyFireReflect <Boolean> True/False": "FriendlyFireReflect"
}

AVAILABLE_ROUND_PROPERTIES = {
    "bMapVoting <Boolean> True/False": "bMapVoting",
    "RoundLimit <Integer> 0-n": "RoundLimit",
    "WinLimit <Integer> 0-n": "WinLimit",
    "RoundTime <Integer> 0-n": "RoundTime",
    "DefendTimer <Integer> 0-n": "DefendTimer",
    "DefendTimerFinal <Integer> 0-n": "DefendTimerFinal"
}

AVAILABLE_SURVIVAL_PROPERTIES = {
    "RoundTimeExtension <Integer> 0-n": "RoundTimeExtension",
    "NumWaves <Integer> 0-50": "NumWaves",
    "bEnableExtractionObjective <Boolean> True/False": "bEnableExtractionObjective",
    "ExtractionObjectiveHoldTime <Integer> 0-n": "ExtractionObjectiveHoldTime",
    "ExtractionSpawnStopTime <Integer> 0-n": "ExtractionSpawnStopTime",
    "BotDPRRespawnFinal <Decimal> 0.0-1.0": "BotDPRRespawnFinal",
    "BotDPRRespawnFirst <Decimal> 0.0-1.0": "BotDPRRespawnFirst",
    "MinimumBotsPerCompletedObjective <Decimal> 0.0-1.0": "MinimumBotsPerCompletedObjective",
    "MaximumBotsPerCompletedObjective <Decimal> 0.0-1.0": "MaximumBotsPerCompletedObjective",
    "bResetLoadoutOnNewRound <Boolean> True/False": "bResetLoadoutOnNewRound",
    "ObjectiveDefendDistance <Integer> 0-n": "ObjectiveDefendDistance",
    "BotMinimumSpawnRange <Integer> 0-n": "BotMinimumSpawnRange",
    "BotMaximumSpawnRange <Integer> 0-n": "BotMaximumSpawnRange",
    "BotRespawnDistance <Integer> 0-n": "BotRespawnDistance",
    "BotSpawnDelay <Integer> 0-n": "BotSpawnDelay",
    "BotRespawnDelay <Decimal> 0.0-10.0": "BotRespawnDelay",
    "BotRepositionDelay <Decimal> 0.0-10.0": "BotRepositionDelay",
    "bUseSpecialWaves <Boolean> True/False": "bUseSpecialWaves",
    "SpecialWaveFrequency <Integer> 0-n": "SpecialWaveFrequency",
    "DefaultReinforcementWaves <Integer> 0-n": "DefaultReinforcementWaves",
    "CaptureBonusWaves <Integer> 0-n": "CaptureBonusWaves",
}
