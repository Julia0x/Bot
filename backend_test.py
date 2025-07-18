#!/usr/bin/env python3
"""
Comprehensive Test Suite for Minecraft XP Farm AFK Bot System
Tests all farming commands, bot management, and error handling
"""

import subprocess
import sys
import json
import time
import os
from datetime import datetime

class MinecraftBotTester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
    def run_test(self, name, test_func):
        """Run a single test and track results"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success = test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - {name}")
                self.test_results.append({"name": name, "status": "PASS", "error": None})
            else:
                print(f"❌ Failed - {name}")
                self.test_results.append({"name": name, "status": "FAIL", "error": "Test returned False"})
            return success
        except Exception as e:
            print(f"❌ Failed - {name}: {str(e)}")
            self.test_results.append({"name": name, "status": "ERROR", "error": str(e)})
            return False

    def test_project_structure(self):
        """Test that all required files exist"""
        required_files = [
            '/app/commands/farming/xpbot.js',
            '/app/commands/farming/autosell.js', 
            '/app/commands/farming/farmstatus.js',
            '/app/commands/farming/stopfarm.js',
            '/app/handlers/commandHandler.js',
            '/app/utils/logger.js',
            '/app/utils/botManager.js',
            '/app/index.js',
            '/app/config.json',
            '/app/package.json'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"Missing files: {missing_files}")
            return False
        
        print("All required files present")
        return True

    def test_package_dependencies(self):
        """Test that all required dependencies are installed"""
        try:
            with open('/app/package.json', 'r') as f:
                package_data = json.load(f)
            
            required_deps = ['mineflayer', 'chalk', 'mineflayer-pathfinder']
            dependencies = package_data.get('dependencies', {})
            
            missing_deps = []
            for dep in required_deps:
                if dep not in dependencies:
                    missing_deps.append(dep)
            
            if missing_deps:
                print(f"Missing dependencies: {missing_deps}")
                return False
                
            # Check if node_modules exists
            if not os.path.exists('/app/node_modules'):
                print("node_modules directory not found")
                return False
                
            print("All dependencies present")
            return True
        except Exception as e:
            print(f"Error checking dependencies: {e}")
            return False

    def test_command_loading(self):
        """Test command loading functionality"""
        try:
            # Create a test script to load commands
            test_script = '''
const { loadCommands } = require('./handlers/commandHandler');

// Mock bot object
const mockBot = {
    commands: new Map(),
    aliases: new Map()
};

try {
    loadCommands(mockBot);
    
    // Check if farming commands are loaded
    const expectedCommands = ['xpbot', 'autosell', 'farmstatus', 'stopfarm'];
    const loadedCommands = Array.from(mockBot.commands.keys());
    
    console.log('Loaded commands:', loadedCommands);
    
    let allFound = true;
    for (const cmd of expectedCommands) {
        if (!mockBot.commands.has(cmd)) {
            console.log('Missing command:', cmd);
            allFound = false;
        }
    }
    
    // Check aliases
    const expectedAliases = ['xp', 'farm', 'sell', 'sellbot', 'status', 'fs', 'stop', 'stopbot'];
    const loadedAliases = Array.from(mockBot.aliases.keys());
    
    console.log('Loaded aliases:', loadedAliases);
    
    for (const alias of expectedAliases) {
        if (!mockBot.aliases.has(alias)) {
            console.log('Missing alias:', alias);
            allFound = false;
        }
    }
    
    if (allFound) {
        console.log('SUCCESS: All commands and aliases loaded');
        process.exit(0);
    } else {
        console.log('FAIL: Some commands or aliases missing');
        process.exit(1);
    }
} catch (error) {
    console.log('ERROR:', error.message);
    process.exit(1);
}
'''
            
            with open('/app/test_command_loading.js', 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(['node', '/app/test_command_loading.js'], 
                                  capture_output=True, text=True, cwd='/app')
            
            os.remove('/app/test_command_loading.js')
            
            if result.returncode == 0:
                print("Command loading successful")
                print(result.stdout)
                return True
            else:
                print(f"Command loading failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error testing command loading: {e}")
            return False

    def test_xpbot_command(self):
        """Test XP bot command with various parameters"""
        try:
            test_script = '''
const xpbotCommand = require('./commands/farming/xpbot');

// Mock bot object
const mockBot = {
    botId: 'TestBot',
    xpFarmingSession: null,
    entities: {},
    entity: { position: { distanceTo: () => 3 } },
    attack: () => {}
};

// Mock logger to capture output
const originalConsoleLog = console.log;
const originalConsoleWarn = console.warn;
let logOutput = [];

console.log = (...args) => {
    logOutput.push(['log', args.join(' ')]);
};
console.warn = (...args) => {
    logOutput.push(['warn', args.join(' ')]);
};

try {
    // Test 1: Valid command with blaze
    console.log('Testing valid xpbot command...');
    xpbotCommand.execute(mockBot, ['blaze', '1000']);
    
    if (mockBot.xpFarmingSession && mockBot.xpFarmingSession.mobType === 'blaze') {
        console.log('SUCCESS: XP farming session started for blaze');
    } else {
        console.log('FAIL: XP farming session not started properly');
        process.exit(1);
    }
    
    // Test 2: Invalid mob type
    console.log('Testing invalid mob type...');
    xpbotCommand.execute(mockBot, ['invalidmob', '1000']);
    
    // Test 3: Invalid cooldown
    console.log('Testing invalid cooldown...');
    xpbotCommand.execute(mockBot, ['blaze', '50']);
    
    // Test 4: Missing parameters
    console.log('Testing missing parameters...');
    xpbotCommand.execute(mockBot, []);
    
    // Test 5: Default cooldown
    console.log('Testing default cooldown...');
    xpbotCommand.execute(mockBot, ['skeleton']);
    
    if (mockBot.xpFarmingSession && mockBot.xpFarmingSession.cooldown === 1000) {
        console.log('SUCCESS: Default cooldown applied');
    } else {
        console.log('FAIL: Default cooldown not applied');
        process.exit(1);
    }
    
    console.log('SUCCESS: All XP bot command tests passed');
    process.exit(0);
    
} catch (error) {
    console.log('ERROR:', error.message);
    process.exit(1);
} finally {
    console.log = originalConsoleLog;
    console.warn = originalConsoleWarn;
}
'''
            
            with open('/app/test_xpbot.js', 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(['node', '/app/test_xpbot.js'], 
                                  capture_output=True, text=True, cwd='/app')
            
            os.remove('/app/test_xpbot.js')
            
            if result.returncode == 0:
                print("XP bot command tests passed")
                print(result.stdout)
                return True
            else:
                print(f"XP bot command tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error testing XP bot command: {e}")
            return False

    def test_autosell_command(self):
        """Test autosell command with various parameters"""
        try:
            test_script = '''
const autosellCommand = require('./commands/farming/autosell');

// Mock bot object
const mockBot = {
    botId: 'TestBot',
    autosellSession: null,
    inventory: {
        slots: Array(45).fill(null)
    },
    heldItem: null,
    chat: () => {},
    equip: (item, slot, callback) => callback()
};

try {
    // Test 1: Valid autosell command
    console.log('Testing valid autosell command...');
    autosellCommand.execute(mockBot, ['blaze_rod', '5000']);
    
    if (mockBot.autosellSession && mockBot.autosellSession.sellItem === 'blaze_rod') {
        console.log('SUCCESS: Autosell session started for blaze_rod');
    } else {
        console.log('FAIL: Autosell session not started properly');
        process.exit(1);
    }
    
    // Test 2: Invalid check interval
    console.log('Testing invalid check interval...');
    autosellCommand.execute(mockBot, ['bone', '500']);
    
    // Test 3: Missing parameters
    console.log('Testing missing parameters...');
    autosellCommand.execute(mockBot, []);
    
    // Test 4: Default check interval
    console.log('Testing default check interval...');
    autosellCommand.execute(mockBot, ['rotten_flesh']);
    
    if (mockBot.autosellSession && mockBot.autosellSession.checkInterval === 5000) {
        console.log('SUCCESS: Default check interval applied');
    } else {
        console.log('FAIL: Default check interval not applied');
        process.exit(1);
    }
    
    console.log('SUCCESS: All autosell command tests passed');
    process.exit(0);
    
} catch (error) {
    console.log('ERROR:', error.message);
    process.exit(1);
}
'''
            
            with open('/app/test_autosell.js', 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(['node', '/app/test_autosell.js'], 
                                  capture_output=True, text=True, cwd='/app')
            
            os.remove('/app/test_autosell.js')
            
            if result.returncode == 0:
                print("Autosell command tests passed")
                print(result.stdout)
                return True
            else:
                print(f"Autosell command tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error testing autosell command: {e}")
            return False

    def test_farmstatus_command(self):
        """Test farm status command"""
        try:
            test_script = '''
const farmstatusCommand = require('./commands/farming/farmstatus');

// Mock bot object with active sessions
const mockBot = {
    botId: 'TestBot',
    xpFarmingSession: {
        isActive: true,
        mobType: 'blaze',
        mobsHit: 50,
        startTime: Date.now() - 60000, // 1 minute ago
        cooldown: 1000
    },
    autosellSession: {
        isActive: true,
        sellItem: 'blaze_rod',
        sellCount: 5,
        startTime: Date.now() - 120000, // 2 minutes ago
        checkInterval: 5000,
        maxSlots: 36,
        reservedSlots: 6
    },
    inventory: {
        slots: Array(45).fill(null).map((_, i) => i < 20 ? { name: 'test_item' } : null)
    }
};

try {
    console.log('Testing farm status command...');
    farmstatusCommand.execute(mockBot, []);
    
    console.log('SUCCESS: Farm status command executed without errors');
    process.exit(0);
    
} catch (error) {
    console.log('ERROR:', error.message);
    process.exit(1);
}
'''
            
            with open('/app/test_farmstatus.js', 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(['node', '/app/test_farmstatus.js'], 
                                  capture_output=True, text=True, cwd='/app')
            
            os.remove('/app/test_farmstatus.js')
            
            if result.returncode == 0:
                print("Farm status command tests passed")
                return True
            else:
                print(f"Farm status command tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error testing farm status command: {e}")
            return False

    def test_stopfarm_command(self):
        """Test stop farm command"""
        try:
            test_script = '''
const stopfarmCommand = require('./commands/farming/stopfarm');

// Mock bot object with active sessions
const mockBot = {
    botId: 'TestBot',
    xpFarmingSession: {
        isActive: true,
        mobType: 'blaze',
        mobsHit: 50,
        startTime: Date.now() - 60000,
        interval: setInterval(() => {}, 1000)
    },
    autosellSession: {
        isActive: true,
        sellItem: 'blaze_rod',
        sellCount: 5,
        startTime: Date.now() - 120000,
        interval: setInterval(() => {}, 5000)
    }
};

try {
    // Test 1: Stop XP farming only
    console.log('Testing stop XP farming...');
    stopfarmCommand.execute(mockBot, ['xp']);
    
    if (!mockBot.xpFarmingSession) {
        console.log('SUCCESS: XP farming session stopped');
    } else {
        console.log('FAIL: XP farming session not stopped');
        process.exit(1);
    }
    
    // Recreate sessions for next test
    mockBot.xpFarmingSession = {
        isActive: true,
        interval: setInterval(() => {}, 1000)
    };
    
    // Test 2: Stop all farming
    console.log('Testing stop all farming...');
    stopfarmCommand.execute(mockBot, ['all']);
    
    if (!mockBot.xpFarmingSession && !mockBot.autosellSession) {
        console.log('SUCCESS: All farming sessions stopped');
    } else {
        console.log('FAIL: Not all farming sessions stopped');
        process.exit(1);
    }
    
    // Test 3: Stop when no sessions active
    console.log('Testing stop with no active sessions...');
    stopfarmCommand.execute(mockBot, []);
    
    console.log('SUCCESS: All stop farm command tests passed');
    process.exit(0);
    
} catch (error) {
    console.log('ERROR:', error.message);
    process.exit(1);
}
'''
            
            with open('/app/test_stopfarm.js', 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(['node', '/app/test_stopfarm.js'], 
                                  capture_output=True, text=True, cwd='/app')
            
            os.remove('/app/test_stopfarm.js')
            
            if result.returncode == 0:
                print("Stop farm command tests passed")
                return True
            else:
                print(f"Stop farm command tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error testing stop farm command: {e}")
            return False

    def test_integration_scenarios(self):
        """Test integration between different commands"""
        try:
            test_script = '''
const xpbotCommand = require('./commands/farming/xpbot');
const autosellCommand = require('./commands/farming/autosell');
const farmstatusCommand = require('./commands/farming/farmstatus');
const stopfarmCommand = require('./commands/farming/stopfarm');

// Mock bot object
const mockBot = {
    botId: 'TestBot',
    xpFarmingSession: null,
    autosellSession: null,
    entities: {},
    entity: { position: { distanceTo: () => 3 } },
    attack: () => {},
    inventory: {
        slots: Array(45).fill(null)
    },
    heldItem: null,
    chat: () => {},
    equip: (item, slot, callback) => callback()
};

try {
    console.log('Testing integration scenario...');
    
    // Start both XP farming and autoselling
    xpbotCommand.execute(mockBot, ['blaze', '1000']);
    autosellCommand.execute(mockBot, ['blaze_rod', '5000']);
    
    // Check that both sessions are active
    if (mockBot.xpFarmingSession && mockBot.autosellSession) {
        console.log('SUCCESS: Both farming sessions started');
    } else {
        console.log('FAIL: Not both sessions started');
        process.exit(1);
    }
    
    // Check status
    farmstatusCommand.execute(mockBot, []);
    
    // Stop only XP farming
    stopfarmCommand.execute(mockBot, ['xp']);
    
    if (!mockBot.xpFarmingSession && mockBot.autosellSession) {
        console.log('SUCCESS: Only XP farming stopped, autosell still active');
    } else {
        console.log('FAIL: Incorrect session states after partial stop');
        process.exit(1);
    }
    
    // Stop all
    stopfarmCommand.execute(mockBot, ['all']);
    
    if (!mockBot.xpFarmingSession && !mockBot.autosellSession) {
        console.log('SUCCESS: All sessions stopped');
    } else {
        console.log('FAIL: Not all sessions stopped');
        process.exit(1);
    }
    
    console.log('SUCCESS: Integration tests passed');
    process.exit(0);
    
} catch (error) {
    console.log('ERROR:', error.message);
    process.exit(1);
}
'''
            
            with open('/app/test_integration.js', 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(['node', '/app/test_integration.js'], 
                                  capture_output=True, text=True, cwd='/app')
            
            os.remove('/app/test_integration.js')
            
            if result.returncode == 0:
                print("Integration tests passed")
                return True
            else:
                print(f"Integration tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error testing integration: {e}")
            return False

    def test_bot_manager(self):
        """Test bot manager functionality"""
        try:
            test_script = '''
const { BotManager } = require('./utils/botManager');

// Mock mineflayer
const mockMineflayer = {
    createBot: (config) => ({
        botId: config.username,
        config: config,
        loadPlugin: () => {},
        once: () => {},
        on: () => {},
        _client: { on: () => {} },
        ended: false,
        quit: function() { this.ended = true; }
    })
};

// Replace mineflayer temporarily
const originalRequire = require;
require = function(id) {
    if (id === 'mineflayer') {
        return mockMineflayer;
    }
    return originalRequire.apply(this, arguments);
};

try {
    const botManager = new BotManager();
    
    // Test bot creation
    const config = { host: 'test', port: 25565, username: 'TestBot', auth: 'offline', version: '1.20.1' };
    const bot = botManager.createBot(config);
    
    if (bot && bot.botId === 'TestBot') {
        console.log('SUCCESS: Bot created successfully');
    } else {
        console.log('FAIL: Bot not created properly');
        process.exit(1);
    }
    
    // Test bot retrieval
    const retrievedBot = botManager.getBot('TestBot');
    if (retrievedBot && retrievedBot.botId === 'TestBot') {
        console.log('SUCCESS: Bot retrieved successfully');
    } else {
        console.log('FAIL: Bot not retrieved properly');
        process.exit(1);
    }
    
    // Test active bot
    const activeBot = botManager.getActiveBot();
    if (activeBot && activeBot.botId === 'TestBot') {
        console.log('SUCCESS: Active bot set correctly');
    } else {
        console.log('FAIL: Active bot not set correctly');
        process.exit(1);
    }
    
    // Test bot count
    if (botManager.getBotCount() === 1) {
        console.log('SUCCESS: Bot count correct');
    } else {
        console.log('FAIL: Bot count incorrect');
        process.exit(1);
    }
    
    console.log('SUCCESS: Bot manager tests passed');
    process.exit(0);
    
} catch (error) {
    console.log('ERROR:', error.message);
    process.exit(1);
} finally {
    require = originalRequire;
}
'''
            
            with open('/app/test_botmanager.js', 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(['node', '/app/test_botmanager.js'], 
                                  capture_output=True, text=True, cwd='/app')
            
            os.remove('/app/test_botmanager.js')
            
            if result.returncode == 0:
                print("Bot manager tests passed")
                return True
            else:
                print(f"Bot manager tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error testing bot manager: {e}")
            return False

    def test_error_handling(self):
        """Test error handling in various scenarios"""
        try:
            test_script = '''
const xpbotCommand = require('./commands/farming/xpbot');
const autosellCommand = require('./commands/farming/autosell');

// Mock bot object
const mockBot = {
    botId: 'TestBot',
    xpFarmingSession: null,
    autosellSession: null
};

// Capture console output
let errorsCaught = 0;
const originalConsoleWarn = console.warn;
console.warn = (...args) => {
    errorsCaught++;
    originalConsoleWarn(...args);
};

try {
    // Test error handling for invalid parameters
    console.log('Testing error handling...');
    
    // Invalid mob type
    xpbotCommand.execute(mockBot, ['invalidmob']);
    
    // Invalid cooldown
    xpbotCommand.execute(mockBot, ['blaze', 'invalid']);
    
    // Missing parameters
    xpbotCommand.execute(mockBot, []);
    autosellCommand.execute(mockBot, []);
    
    // Invalid check interval
    autosellCommand.execute(mockBot, ['item', 'invalid']);
    
    if (errorsCaught >= 4) {
        console.log('SUCCESS: Error handling working correctly');
        process.exit(0);
    } else {
        console.log('FAIL: Not all errors were handled');
        process.exit(1);
    }
    
} catch (error) {
    console.log('ERROR:', error.message);
    process.exit(1);
} finally {
    console.warn = originalConsoleWarn;
}
'''
            
            with open('/app/test_errors.js', 'w') as f:
                f.write(test_script)
            
            result = subprocess.run(['node', '/app/test_errors.js'], 
                                  capture_output=True, text=True, cwd='/app')
            
            os.remove('/app/test_errors.js')
            
            if result.returncode == 0:
                print("Error handling tests passed")
                return True
            else:
                print(f"Error handling tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Error testing error handling: {e}")
            return False

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("🧪 MINECRAFT XP FARM BOT TEST SUMMARY")
        print("="*60)
        
        print(f"📊 Tests Run: {self.tests_run}")
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"  {status_icon} {result['name']}")
            if result["error"]:
                print(f"     Error: {result['error']}")
        
        print("\n" + "="*60)
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! The XP Farm Bot system is working correctly.")
            return 0
        else:
            print("⚠️  SOME TESTS FAILED! Please review the issues above.")
            return 1

def main():
    print("🚀 Starting Minecraft XP Farm AFK Bot System Tests...")
    print("="*60)
    
    tester = MinecraftBotTester()
    
    # Run all tests
    test_functions = [
        ("Project Structure", tester.test_project_structure),
        ("Package Dependencies", tester.test_package_dependencies),
        ("Command Loading", tester.test_command_loading),
        ("XP Bot Command", tester.test_xpbot_command),
        ("Autosell Command", tester.test_autosell_command),
        ("Farm Status Command", tester.test_farmstatus_command),
        ("Stop Farm Command", tester.test_stopfarm_command),
        ("Integration Scenarios", tester.test_integration_scenarios),
        ("Bot Manager", tester.test_bot_manager),
        ("Error Handling", tester.test_error_handling)
    ]
    
    for test_name, test_func in test_functions:
        tester.run_test(test_name, test_func)
    
    return tester.print_summary()

if __name__ == "__main__":
    sys.exit(main())