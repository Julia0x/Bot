const logger = require('../../utils/logger');

module.exports = {
  name: 'xpbot',
  aliases: ['xp', 'farm'],
  description: 'Start AFK XP farming for specific mob type',
  usage: 'xpbot <mob_type> [cooldown_ms]',
  execute(bot, args) {
    if (!args[0]) {
      logger.warn('Usage: xpbot <mob_type> [cooldown_ms]');
      logger.info('Example: xpbot blaze 1000');
      logger.info('Available mobs: blaze, skeleton, zombie, spider, creeper, enderman');
      return;
    }

    const mobType = args[0].toLowerCase();
    const cooldown = args[1] ? parseInt(args[1]) : 1000; // Default 1 second cooldown

    // Validate mob type
    const validMobs = ['blaze', 'skeleton', 'zombie', 'spider', 'creeper', 'enderman'];
    if (!validMobs.includes(mobType)) {
      logger.warn(`Invalid mob type: ${mobType}`);
      logger.info(`Available mobs: ${validMobs.join(', ')}`);
      return;
    }

    // Validate cooldown
    if (isNaN(cooldown) || cooldown < 100) {
      logger.warn('Cooldown must be a number >= 100ms');
      return;
    }

    // Stop existing farming session if active
    if (bot.xpFarmingSession) {
      logger.warn('Stopping existing XP farming session...');
      clearInterval(bot.xpFarmingSession.interval);
      bot.xpFarmingSession = null;
    }

    // Start new farming session
    startXPFarming(bot, mobType, cooldown);
  },
};

function startXPFarming(bot, mobType, cooldown) {
  logger.success(`[${bot.botId}] Starting XP farming for ${mobType} (cooldown: ${cooldown}ms)`);
  
  // Initialize farming session
  bot.xpFarmingSession = {
    mobType: mobType,
    cooldown: cooldown,
    isActive: true,
    mobsHit: 0,
    startTime: Date.now(),
    lastAttack: 0,
    interval: null
  };

  // Start the farming loop
  bot.xpFarmingSession.interval = setInterval(() => {
    if (!bot.xpFarmingSession || !bot.xpFarmingSession.isActive) {
      return;
    }

    // Check if we're ready to attack (cooldown)
    const now = Date.now();
    if (now - bot.xpFarmingSession.lastAttack < cooldown) {
      return;
    }

    // Find nearby mobs of specified type
    const targetMob = findNearestMob(bot, mobType);
    if (targetMob) {
      attackMob(bot, targetMob);
      bot.xpFarmingSession.lastAttack = now;
      bot.xpFarmingSession.mobsHit++;
    }
  }, 100); // Check every 100ms for responsive targeting

  // Log farming status periodically
  const statusInterval = setInterval(() => {
    if (!bot.xpFarmingSession || !bot.xpFarmingSession.isActive) {
      clearInterval(statusInterval);
      return;
    }

    const session = bot.xpFarmingSession;
    const runtime = Math.floor((Date.now() - session.startTime) / 1000);
    const mobsPerMinute = session.mobsHit > 0 ? Math.round((session.mobsHit / runtime) * 60) : 0;
    
    logger.info(`[${bot.botId}] XP Farm Status: ${session.mobsHit} mobs hit | ${runtime}s runtime | ${mobsPerMinute}/min`);
  }, 30000); // Status every 30 seconds

  logger.botAction(bot.botId, 'xpbot', `Started farming ${mobType}`);
}

function findNearestMob(bot, mobType) {
  const entities = Object.values(bot.entities);
  const mobs = entities.filter(entity => {
    if (!entity.mobType) return false;
    
    // Check if entity matches target mob type
    const entityType = entity.mobType.toLowerCase();
    if (entityType !== mobType) return false;
    
    // Check if entity is alive
    if (entity.health !== undefined && entity.health <= 0) return false;
    
    // Check distance (only attack mobs within 4 blocks)
    const distance = bot.entity.position.distanceTo(entity.position);
    return distance <= 4;
  });

  // Return the closest mob
  if (mobs.length > 0) {
    return mobs.reduce((closest, current) => {
      const closestDistance = bot.entity.position.distanceTo(closest.position);
      const currentDistance = bot.entity.position.distanceTo(current.position);
      return currentDistance < closestDistance ? current : closest;
    });
  }

  return null;
}

function attackMob(bot, mob) {
  try {
    // Attack the mob
    bot.attack(mob);
    
    const distance = Math.round(bot.entity.position.distanceTo(mob.position) * 10) / 10;
    logger.debug(`[${bot.botId}] Attacked ${mob.mobType} at distance ${distance}`);
  } catch (error) {
    logger.error(`[${bot.botId}] Attack failed: ${error.message}`);
  }
}

// Add a stop command helper
function stopXPFarming(bot) {
  if (bot.xpFarmingSession) {
    clearInterval(bot.xpFarmingSession.interval);
    const session = bot.xpFarmingSession;
    const runtime = Math.floor((Date.now() - session.startTime) / 1000);
    
    logger.success(`[${bot.botId}] XP farming stopped. Final stats: ${session.mobsHit} mobs hit in ${runtime}s`);
    bot.xpFarmingSession = null;
    return true;
  }
  return false;
}

// Export the stop function for use by other commands
module.exports.stopXPFarming = stopXPFarming;