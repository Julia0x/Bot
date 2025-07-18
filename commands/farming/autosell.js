const logger = require('../../utils/logger');

module.exports = {
  name: 'autosell',
  aliases: ['sell', 'sellbot'],
  description: 'Auto-sell items when inventory is full',
  usage: 'autosell <item_type> [check_interval_ms]',
  execute(bot, args) {
    if (!args[0]) {
      logger.warn('Usage: autosell <item_type> [check_interval_ms]');
      logger.info('Example: autosell blaze_rod 5000');
      logger.info('Common items: blaze_rod, rotten_flesh, bone, string, gunpowder');
      return;
    }

    const sellItem = args[0].toLowerCase();
    const checkInterval = args[1] ? parseInt(args[1]) : 5000; // Default 5 second check

    // Validate check interval
    if (isNaN(checkInterval) || checkInterval < 1000) {
      logger.warn('Check interval must be a number >= 1000ms');
      return;
    }

    // Stop existing autosell session if active
    if (bot.autosellSession) {
      logger.warn('Stopping existing autosell session...');
      clearInterval(bot.autosellSession.interval);
      bot.autosellSession = null;
    }

    // Start new autosell session
    startAutosell(bot, sellItem, checkInterval);
  },
};

function startAutosell(bot, sellItem, checkInterval) {
  logger.success(`[${bot.botId}] Starting autosell for ${sellItem} (check every ${checkInterval}ms)`);
  
  // Initialize autosell session
  bot.autosellSession = {
    sellItem: sellItem,
    checkInterval: checkInterval,
    isActive: true,
    sellCount: 0,
    startTime: Date.now(),
    lastSell: 0,
    interval: null,
    maxSlots: 36, // Standard Minecraft inventory slots
    reservedSlots: 6 // Keep some slots free for safety
  };

  // Start the autosell loop
  bot.autosellSession.interval = setInterval(() => {
    if (!bot.autosellSession || !bot.autosellSession.isActive) {
      return;
    }

    checkAndSellItems(bot);
  }, checkInterval);

  // Log autosell status periodically
  const statusInterval = setInterval(() => {
    if (!bot.autosellSession || !bot.autosellSession.isActive) {
      clearInterval(statusInterval);
      return;
    }

    const session = bot.autosellSession;
    const runtime = Math.floor((Date.now() - session.startTime) / 1000);
    const sellsPerHour = session.sellCount > 0 ? Math.round((session.sellCount / runtime) * 3600) : 0;
    
    logger.info(`[${bot.botId}] Autosell Status: ${session.sellCount} sells | ${runtime}s runtime | ${sellsPerHour}/hour`);
  }, 60000); // Status every minute

  logger.botAction(bot.botId, 'autosell', `Started autosell for ${sellItem}`);
}

function checkAndSellItems(bot) {
  try {
    // Check if inventory is full enough to warrant selling
    const usedSlots = getUsedInventorySlots(bot);
    const session = bot.autosellSession;
    const thresholdSlots = session.maxSlots - session.reservedSlots;

    if (usedSlots < thresholdSlots) {
      return; // Not full enough
    }

    // Find the sell item in inventory
    const sellItemSlot = findItemInInventory(bot, session.sellItem);
    if (!sellItemSlot) {
      logger.warn(`[${bot.botId}] No ${session.sellItem} found in inventory to sell`);
      return;
    }

    // Remember current hand item
    const currentHandItem = bot.heldItem;
    
    // Execute sell sequence
    executeSellSequence(bot, sellItemSlot, currentHandItem);
    
  } catch (error) {
    logger.error(`[${bot.botId}] Autosell error: ${error.message}`);
  }
}

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

function findItemInInventory(bot, itemName) {
  // Check main inventory slots
  for (let i = 9; i <= 44; i++) {
    const slot = bot.inventory.slots[i];
    if (slot && slot.name && slot.name.toLowerCase().includes(itemName.toLowerCase())) {
      return slot;
    }
  }
  
  return null;
}

async function executeSellSequence(bot, sellItemSlot, previousHandItem) {
  try {
    logger.info(`[${bot.botId}] Executing sell sequence for ${sellItemSlot.name}`);
    
    // Step 1: Equip the sell item
    await equipItem(bot, sellItemSlot);
    
    // Small delay to ensure item is equipped
    await sleep(500);
    
    // Step 2: Execute sell command
    bot.chat('/sell hand');
    logger.botAction(bot.botId, 'sell', `Sold ${sellItemSlot.name} x${sellItemSlot.count}`);
    
    // Step 3: Wait for sell to complete
    await sleep(1000);
    
    // Step 4: Re-equip previous item if it existed
    if (previousHandItem) {
      const previousItem = findItemInInventory(bot, previousHandItem.name);
      if (previousItem) {
        await equipItem(bot, previousItem);
        await sleep(500);
      }
    }
    
    // Update statistics
    bot.autosellSession.sellCount++;
    bot.autosellSession.lastSell = Date.now();
    
  } catch (error) {
    logger.error(`[${bot.botId}] Sell sequence failed: ${error.message}`);
  }
}

function equipItem(bot, item) {
  return new Promise((resolve, reject) => {
    try {
      bot.equip(item, 'hand', (err) => {
        if (err) {
          reject(err);
        } else {
          resolve();
        }
      });
    } catch (error) {
      reject(error);
    }
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Add a stop command helper
function stopAutosell(bot) {
  if (bot.autosellSession) {
    clearInterval(bot.autosellSession.interval);
    const session = bot.autosellSession;
    const runtime = Math.floor((Date.now() - session.startTime) / 1000);
    
    logger.success(`[${bot.botId}] Autosell stopped. Final stats: ${session.sellCount} sells in ${runtime}s`);
    bot.autosellSession = null;
    return true;
  }
  return false;
}

// Export the stop function for use by other commands
module.exports.stopAutosell = stopAutosell;