const logger = require('../../utils/logger');
const { stopXPFarming } = require('./xpbot');
const { stopAutosell } = require('./autosell');

module.exports = {
  name: 'stopfarm',
  aliases: ['stop', 'stopbot'],
  description: 'Stop XP farming and autosell sessions',
  usage: 'stopfarm [xp|autosell|all]',
  execute(bot, args) {
    const target = args[0] ? args[0].toLowerCase() : 'all';

    let stopped = false;

    if (target === 'xp' || target === 'all') {
      if (stopXPFarming(bot)) {
        stopped = true;
      }
    }

    if (target === 'autosell' || target === 'sell' || target === 'all') {
      if (stopAutosell(bot)) {
        stopped = true;
      }
    }

    if (!stopped) {
      logger.warn(`[${bot.botId}] No active farming sessions to stop`);
    } else {
      logger.success(`[${bot.botId}] Farming sessions stopped`);
    }

    logger.botAction(bot.botId, 'stopfarm', target);
  },
};