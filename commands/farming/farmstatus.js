const logger = require('../../utils/logger');

module.exports = {
  name: 'farmstatus',
  aliases: ['status', 'fs'],
  description: 'Show status of active farming sessions',
  usage: 'farmstatus',
  execute(bot, args) {
    logger.separator();
    logger.status(`Farming Status for ${bot.botId}`);
    
    let hasActiveSessions = false;

    // Check XP farming status
    if (bot.xpFarmingSession && bot.xpFarmingSession.isActive) {
      const session = bot.xpFarmingSession;
      const runtime = Math.floor((Date.now() - session.startTime) / 1000);
      const mobsPerMinute = session.mobsHit > 0 ? Math.round((session.mobsHit / runtime) * 60) : 0;
      
      console.log(`  🗡️  XP Farming: ${session.mobType.toUpperCase()}`);
      console.log(`     • Mobs Hit: ${session.mobsHit}`);
      console.log(`     • Runtime: ${runtime}s`);
      console.log(`     • Rate: ${mobsPerMinute} mobs/min`);
      console.log(`     • Cooldown: ${session.cooldown}ms`);
      
      hasActiveSessions = true;
    }

    // Check autosell status
    if (bot.autosellSession && bot.autosellSession.isActive) {
      const session = bot.autosellSession;
      const runtime = Math.floor((Date.now() - session.startTime) / 1000);
      const sellsPerHour = session.sellCount > 0 ? Math.round((session.sellCount / runtime) * 3600) : 0;
      
      console.log(`  💰 Autosell: ${session.sellItem.toUpperCase()}`);
      console.log(`     • Sells: ${session.sellCount}`);
      console.log(`     • Runtime: ${runtime}s`);
      console.log(`     • Rate: ${sellsPerHour} sells/hour`);
      console.log(`     • Check Interval: ${session.checkInterval}ms`);
      console.log(`     • Slots Threshold: ${session.maxSlots - session.reservedSlots}`);
      
      hasActiveSessions = true;
    }

    if (!hasActiveSessions) {
      console.log('  ❌ No active farming sessions');
    }

    // Show inventory status
    const usedSlots = getUsedInventorySlots(bot);
    console.log(`  🎒 Inventory: ${usedSlots}/36 slots used`);
    
    logger.separator();
    logger.botAction(bot.botId, 'farmstatus', 'checked');
  },
};

function getUsedInventorySlots(bot) {
  let usedSlots = 0;
  
  // Check main inventory (slots 9-44 in window)
  for (let i = 9; i <= 44; i++) {
    const slot = bot.inventory.slots[i];
    if (slot) {
      usedSlots++;
    }
  }
  
  return usedSlots;
}