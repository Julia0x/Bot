# XP Farm AFK Bot

A sophisticated Minecraft bot system with XP farming and autoselling capabilities built with Mineflayer.

## Features

### 🗡️ XP Farming
- **AFK XP Farming**: Automatically attacks mobs in range without moving
- **Configurable Mob Types**: Target specific mobs (blaze, skeleton, zombie, spider, creeper, enderman)
- **Cooldown System**: Configurable attack cooldown for optimal farming
- **Smart Targeting**: Attacks mobs within 4 blocks range
- **Statistics Tracking**: Real-time stats on mobs hit and farming rate

### 💰 Autoselling
- **Automatic Selling**: Sells items when inventory is full (30+ slots)
- **Smart Item Management**: Temporarily switches to sell item, executes `/sell hand`, then switches back
- **Configurable Items**: Specify which items to sell (blaze_rod, rotten_flesh, etc.)
- **Inventory Monitoring**: Continuous inventory tracking with configurable check intervals
- **Safe Slot Management**: Reserves slots to prevent complete inventory fill

### 🤖 Bot Management
- **Multi-bot Support**: Manage multiple bots simultaneously
- **Real-time Status**: Check farming status and statistics
- **Easy Control**: Start/stop farming sessions individually or all at once
- **Persistent Sessions**: Farming continues until manually stopped

## Quick Start

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Configure Bot**:
   Edit `config.json` with your server details:
   ```json
   {
     "host": "your-server.com",
     "port": 25565,
     "username": "YourBot",
     "auth": "offline",
     "version": "1.20.1"
   }
   ```

3. **Run the Bot**:
   ```bash
   node index.js
   ```

4. **Start Farming**:
   ```
   xpbot blaze 1000
   autosell blaze_rod 5000
   ```

## Commands

### XP Farming Commands

#### `xpbot <mob_type> [cooldown_ms]`
Start XP farming for specified mob type with optional cooldown.

**Examples:**
```
xpbot blaze 1000         # Farm blazes with 1 second cooldown
xpbot skeleton 500       # Farm skeletons with 0.5 second cooldown
xpbot zombie 1500        # Farm zombies with 1.5 second cooldown
```

**Available Mob Types:**
- `blaze` - Nether blazes
- `skeleton` - Skeletons
- `zombie` - Zombies
- `spider` - Spiders
- `creeper` - Creepers
- `enderman` - Endermen

### Autoselling Commands

#### `autosell <item_type> [check_interval_ms]`
Start autoselling for specified item type with optional check interval.

**Examples:**
```
autosell blaze_rod 5000      # Sell blaze rods every 5 seconds
autosell rotten_flesh 3000   # Sell rotten flesh every 3 seconds
autosell bone 10000          # Sell bones every 10 seconds
```

**Common Items:**
- `blaze_rod` - Blaze rods from blazes
- `rotten_flesh` - Rotten flesh from zombies
- `bone` - Bones from skeletons
- `string` - String from spiders
- `gunpowder` - Gunpowder from creepers

### Control Commands

#### `farmstatus`
Display current farming status including:
- Active XP farming sessions
- Autosell sessions
- Statistics (mobs hit, sells completed, rates)
- Inventory usage

#### `stopfarm [target]`
Stop farming sessions.

**Examples:**
```
stopfarm all         # Stop all farming sessions
stopfarm xp          # Stop only XP farming
stopfarm autosell    # Stop only autoselling
```

### Bot Management Commands

#### `bot create <username>`
Create a new bot instance.

#### `bot list`
List all active bots.

#### `bot switch <username>`
Switch to a different bot.

#### `bot all <command>`
Execute command on all bots.

## Advanced Usage

### Optimal Farming Setup

1. **Position your bot** in an AFK farm where mobs spawn within 4 blocks
2. **Start XP farming** with appropriate cooldown for your farm type
3. **Enable autoselling** to prevent inventory overflow
4. **Monitor status** periodically to ensure optimal performance

### Example AFK Farm Session
```
# Start the bot
node index.js

# Create a bot (if needed)
bot create MyFarmBot

# Start farming blazes in a blaze farm
xpbot blaze 1000

# Start autoselling blaze rods when inventory fills
autosell blaze_rod 5000

# Check status
farmstatus

# Stop when done
stopfarm all
```

### Multi-Bot Farming
```
# Create multiple bots
bot create FarmBot1
bot create FarmBot2

# Start farming on all bots
bot all xpbot blaze 1000
bot all autosell blaze_rod 5000

# Check status of all bots
bot list
```

## Configuration

### Attack Range
- Default: 4 blocks
- Mobs must be within this range to be attacked

### Inventory Management
- Total slots: 36 (standard Minecraft inventory)
- Autosell threshold: 30 slots (keeps 6 slots free)
- Safe slot management prevents complete inventory fill

### Cooldown Settings
- Minimum cooldown: 100ms
- Recommended: 500-2000ms depending on farm type
- Higher cooldowns reduce server load

### Check Intervals
- Minimum autosell check: 1000ms (1 second)
- Recommended: 3000-10000ms (3-10 seconds)
- More frequent checks use more resources

## Troubleshooting

### Bot Not Attacking
- Check if mobs are within 4 blocks range
- Verify mob type matches command parameter
- Ensure cooldown isn't too high

### Autosell Not Working
- Verify item name matches inventory item
- Check if `/sell hand` command works on your server
- Ensure inventory has enough items to trigger threshold

### Performance Issues
- Increase cooldown times
- Increase autosell check intervals
- Reduce number of active bots

## Technical Details

### Dependencies
- `mineflayer`: Minecraft bot framework
- `mineflayer-pathfinder`: Pathfinding (used for positioning)
- `chalk`: Terminal colors for logging

### Architecture
- **Command System**: Modular command loading with categories
- **Event Handling**: Comprehensive event management
- **Multi-Bot Support**: Manage multiple bot instances
- **Session Management**: Persistent farming sessions with statistics
- **Logging**: Comprehensive logging with different levels

### File Structure
```
/app/
├── commands/
│   ├── farming/
│   │   ├── xpbot.js      # XP farming command
│   │   ├── autosell.js   # Autoselling command
│   │   ├── farmstatus.js # Status command
│   │   └── stopfarm.js   # Stop command
│   ├── utility/
│   └── control/
├── handlers/
├── utils/
├── config.json
└── index.js
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Support

For support and questions, please open an issue in the project repository.