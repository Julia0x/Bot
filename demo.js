#!/usr/bin/env node

/**
 * XP Farm AFK Bot Demo
 * 
 * This script demonstrates the XP farming and autosell functionality.
 * 
 * Commands available:
 * - xpbot <mob_type> [cooldown_ms] - Start XP farming
 * - autosell <item_type> [check_interval_ms] - Start autoselling
 * - farmstatus - Check farming status
 * - stopfarm [xp|autosell|all] - Stop farming sessions
 * 
 * Examples:
 * xpbot blaze 1000
 * autosell blaze_rod 5000
 * farmstatus
 * stopfarm all
 */

const { botManager } = require('./utils/botManager');
const { loadCommands } = require('./handlers/commandHandler');
const { loadEvents } = require('./handlers/eventHandler');
const logger = require('./utils/logger');
const config = require('./config.json');
const readline = require('readline');

// Show demo instructions
console.log('\n🎮 XP Farm AFK Bot Demo\n');
console.log('📋 Available Commands:');
console.log('   xpbot <mob_type> [cooldown_ms]    - Start XP farming');
console.log('   autosell <item_type> [interval]   - Start autoselling');
console.log('   farmstatus                        - Check farming status');
console.log('   stopfarm [xp|autosell|all]        - Stop farming sessions');
console.log('');
console.log('🎯 Example Usage:');
console.log('   xpbot blaze 1000                  - Farm blazes with 1s cooldown');
console.log('   autosell blaze_rod 5000           - Sell blaze rods every 5s');
console.log('   farmstatus                        - Check current status');
console.log('   stopfarm all                      - Stop all farming');
console.log('');
console.log('⚙️  Configuration:');
console.log('   • Mob types: blaze, skeleton, zombie, spider, creeper, enderman');
console.log('   • Autosell triggers when inventory reaches 30+ slots');
console.log('   • Attack range: 4 blocks');
console.log('   • Inventory management: automatic item swapping');
console.log('');
console.log('🚀 Starting bot system...\n');

// Create and initialize main bot
const mainBot = botManager.createBot(config);
loadCommands(mainBot);
loadEvents(mainBot);

// Setup command line interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: '> '
});

// Update prompt to show current bot status
function updatePrompt() {
  const activeBot = botManager.getActiveBotId();
  const botCount = botManager.getBotCount();
  const connectedCount = botManager.getAllBots().filter(bot => !bot.ended).length;
  
  if (activeBot) {
    rl.setPrompt(`[${activeBot}] (${connectedCount}/${botCount}) > `);
  } else {
    rl.setPrompt(`[no-bot] (0/0) > `);
  }
}

// Show initial prompt
updatePrompt();
rl.prompt();

// Handle command line input
rl.on('line', (input) => {
  const trimmedInput = input.trim();
  
  if (!trimmedInput) {
    rl.prompt();
    return;
  }

  // Handle built-in commands
  if (trimmedInput === 'exit' || trimmedInput === 'quit') {
    logger.info('Shutting down...');
    botManager.disconnectAll();
    process.exit(0);
  }

  if (trimmedInput === 'help') {
    console.log('\n🎮 XP Farm AFK Bot - Available Commands:');
    console.log('');
    console.log('  XP Farming:');
    console.log('    xpbot <mob_type> [cooldown_ms]  - Start XP farming');
    console.log('    xpbot blaze 1000                - Farm blazes with 1s cooldown');
    console.log('    xpbot skeleton 500              - Farm skeletons with 0.5s cooldown');
    console.log('');
    console.log('  Autosell:');
    console.log('    autosell <item_type> [interval] - Start autoselling');
    console.log('    autosell blaze_rod 5000         - Sell blaze rods every 5s');
    console.log('    autosell rotten_flesh 3000      - Sell rotten flesh every 3s');
    console.log('');
    console.log('  Control:');
    console.log('    farmstatus                      - Show farming status');
    console.log('    stopfarm [xp|autosell|all]      - Stop farming sessions');
    console.log('    stopfarm all                    - Stop all farming');
    console.log('');
    console.log('  System:');
    console.log('    help                            - Show this help');
    console.log('    exit/quit                       - Exit bot');
    console.log('    bot create <username>           - Create new bot');
    console.log('    bot list                        - List all bots');
    console.log('');
    updatePrompt();
    rl.prompt();
    return;
  }

  // Parse and execute regular commands
  const [cmd, ...args] = trimmedInput.split(' ');
  
  // Get the active bot
  const activeBot = botManager.getActiveBot();
  
  if (!activeBot) {
    logger.warn('❌ No active bot available. Create a bot first with "bot create <username>"');
    updatePrompt();
    rl.prompt();
    return;
  }

  const command = activeBot.commands.get(cmd) || activeBot.aliases.get(cmd);
  
  if (command) {
    try {
      const botId = botManager.getActiveBotId();
      logger.command(botId, cmd, args);
      command.execute(activeBot, args);
    } catch (error) {
      logger.error(`Error executing command '${cmd}': ${error.message}`);
    }
  } else {
    logger.warn(`❓ Unknown command: ${cmd}. Type "help" for available commands.`);
  }

  updatePrompt();
  rl.prompt();
});

// Update prompt periodically
setInterval(() => {
  updatePrompt();
}, 3000);

// Handle process termination gracefully
process.on('SIGINT', () => {
  logger.info('\n🛑 Received SIGINT, shutting down gracefully...');
  botManager.disconnectAll();
  rl.close();
  process.exit(0);
});

process.on('SIGTERM', () => {
  logger.info('Received SIGTERM, shutting down gracefully...');
  botManager.disconnectAll();
  rl.close();
  process.exit(0);
});