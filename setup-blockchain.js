// Decentralized Academic Plagiarism Checker - Blockchain Setup Script
// This script helps with setting up the Aptos blockchain integration

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Check if Aptos CLI is installed
function checkAptosCLI() {
  try {
    console.log('Checking for Aptos CLI...');
    const version = execSync('aptos --version').toString().trim();
    console.log(`✅ Aptos CLI found: ${version}`);
    return true;
  } catch (error) {
    console.log('❌ Aptos CLI not found');
    console.log('Please install Aptos CLI: https://aptos.dev/tools/aptos-cli/');
    return false;
  }
}

// Create a new Aptos account
function createAptosAccount() {
  console.log('\n📝 Creating a new Aptos account...');
  try {
    // Create a new profile
    execSync('aptos init --profile plagiarism-checker --network testnet');
    
    // Get the account address
    const configPath = path.join(process.env.HOME || process.env.USERPROFILE, '.aptos', 'config.yaml');
    const config = fs.readFileSync(configPath, 'utf8');
    
    // Extract address using regex
    const addressMatch = config.match(/account: ([a-f0-9]+)/);
    const privateKeyMatch = config.match(/private_key: "([a-f0-9]+)"/);
    
    if (addressMatch && privateKeyMatch) {
      const address = `0x${addressMatch[1]}`;
      const privateKey = privateKeyMatch[1];
      
      console.log(`✅ Account created successfully!`);
      console.log(`📋 Account Address: ${address}`);
      console.log(`🔑 Private Key: ${privateKey}`);
      
      // Update .env file
      updateEnvFile(address, privateKey);
      
      return { address, privateKey };
    } else {
      throw new Error('Failed to extract account information');
    }
  } catch (error) {
    console.error('❌ Error creating Aptos account:', error.message);
    return null;
  }
}

// Fund the account with testnet tokens
function fundAccount(address) {
  console.log(`\n💰 Funding account ${address} with testnet tokens...`);
  try {
    console.log('Please visit the Aptos Faucet to get testnet tokens:');
    console.log(`https://aptoslabs.com/testnet-faucet?address=${address}`);
    
    return new Promise((resolve) => {
      rl.question('Press Enter once you have funded your account...', () => {
        console.log('✅ Account funding acknowledged');
        resolve(true);
      });
    });
  } catch (error) {
    console.error('❌ Error funding account:', error.message);
    return false;
  }
}

// Deploy the contract
function deployContract(address) {
  console.log('\n🚀 Deploying the AcademicNFT contract...');
  try {
    // Change to contracts directory
    process.chdir(path.join(__dirname, 'contracts'));
    
    // Deploy the contract
    execSync(`aptos move publish --named-addresses AcademicNFT=${address} --profile plagiarism-checker`);
    
    console.log('✅ Contract deployed successfully!');
    
    // Update .env file with contract address (same as account address for this contract)
    updateEnvFileWithContractAddress(address);
    
    return true;
  } catch (error) {
    console.error('❌ Error deploying contract:', error.message);
    return false;
  }
}

// Update .env file with account information
function updateEnvFile(address, privateKey) {
  console.log('\n📝 Updating .env file with account information...');
  try {
    const envPath = path.join(__dirname, '.env');
    let envContent = '';
    
    if (fs.existsSync(envPath)) {
      envContent = fs.readFileSync(envPath, 'utf8');
    }
    
    // Update or add APTOS_NODE_URL
    if (envContent.includes('APTOS_NODE_URL=')) {
      envContent = envContent.replace(/APTOS_NODE_URL=.*/, 'APTOS_NODE_URL=https://fullnode.testnet.aptoslabs.com/v1');
    } else {
      envContent += 'APTOS_NODE_URL=https://fullnode.testnet.aptoslabs.com/v1\n';
    }
    
    // Update or add APTOS_PRIVATE_KEY
    if (envContent.includes('APTOS_PRIVATE_KEY=')) {
      envContent = envContent.replace(/APTOS_PRIVATE_KEY=.*/, `APTOS_PRIVATE_KEY=${privateKey}`);
    } else {
      envContent += `APTOS_PRIVATE_KEY=${privateKey}\n`;
    }
    
    fs.writeFileSync(envPath, envContent);
    console.log('✅ .env file updated with account information');
    return true;
  } catch (error) {
    console.error('❌ Error updating .env file:', error.message);
    return false;
  }
}

// Update .env file with contract address
function updateEnvFileWithContractAddress(address) {
  console.log('\n📝 Updating .env file with contract address...');
  try {
    const envPath = path.join(__dirname, '.env');
    let envContent = '';
    
    if (fs.existsSync(envPath)) {
      envContent = fs.readFileSync(envPath, 'utf8');
    }
    
    // Update or add CONTRACT_ADDRESS
    if (envContent.includes('CONTRACT_ADDRESS=')) {
      envContent = envContent.replace(/CONTRACT_ADDRESS=.*/, `CONTRACT_ADDRESS=${address}`);
    } else {
      envContent += `CONTRACT_ADDRESS=${address}\n`;
    }
    
    fs.writeFileSync(envPath, envContent);
    console.log('✅ .env file updated with contract address');
    return true;
  } catch (error) {
    console.error('❌ Error updating .env file:', error.message);
    return false;
  }
}

// Get NFT.Storage API key
function getNFTStorageAPIKey() {
  console.log('\n🔑 Setting up NFT.Storage API key...');
  return new Promise((resolve) => {
    rl.question('Enter your NFT.Storage API key (or press Enter to skip): ', (apiKey) => {
      if (apiKey) {
        try {
          const envPath = path.join(__dirname, '.env');
          let envContent = '';
          
          if (fs.existsSync(envPath)) {
            envContent = fs.readFileSync(envPath, 'utf8');
          }
          
          // Update or add NFT_STORAGE_API_KEY
          if (envContent.includes('NFT_STORAGE_API_KEY=')) {
            envContent = envContent.replace(/NFT_STORAGE_API_KEY=.*/, `NFT_STORAGE_API_KEY=${apiKey}`);
          } else {
            envContent += `NFT_STORAGE_API_KEY=${apiKey}\n`;
          }
          
          fs.writeFileSync(envPath, envContent);
          console.log('✅ .env file updated with NFT.Storage API key');
        } catch (error) {
          console.error('❌ Error updating .env file:', error.message);
        }
      } else {
        console.log('⚠️ Skipping NFT.Storage API key setup. Mock IPFS uploads will be used.');
      }
      resolve(true);
    });
  });
}

// Main function
async function main() {
  console.log('=== Decentralized Academic Plagiarism Checker - Blockchain Setup ===\n');
  
  // Check if Aptos CLI is installed
  if (!checkAptosCLI()) {
    rl.close();
    return;
  }
  
  // Create a new Aptos account
  const account = createAptosAccount();
  if (!account) {
    rl.close();
    return;
  }
  
  // Fund the account with testnet tokens
  await fundAccount(account.address);
  
  // Deploy the contract
  deployContract(account.address);
  
  // Get NFT.Storage API key
  await getNFTStorageAPIKey();
  
  console.log('\n✅ Blockchain setup complete!');
  console.log('\nNext steps:');
  console.log('1. Start the backend server: python -m uvicorn backend.main:app --reload');
  console.log('2. Open the frontend in your browser: frontend/index.html');
  console.log('3. Connect your wallet (Petra or Martian) and start using the app!');
  
  rl.close();
}

main(); 